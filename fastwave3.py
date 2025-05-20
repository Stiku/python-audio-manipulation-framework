#!/usr/bin/env python3

import numpy as np
import struct







def convert(data, to_t=np.float_):
    from_t=data.dtype
    to_t=np.dtype(to_t)
    if(from_t==to_t):
        return data;
    
    from_isfloat=from_t.kind == 'f'
    to_isfloat=to_t.kind == 'f'
    if from_isfloat and to_isfloat:
        return data.astype(to_t)
    
    elif from_isfloat and not to_isfloat:
        info = np.iinfo(to_t)
        mv = info.min
        rng = info.max-info.min
        fromto = rng/2.0
        
        data=(data+1.0)*fromto + mv
        return np.round(data).astype(to_t)
    
    elif not from_isfloat and to_isfloat:
        info = np.iinfo(from_t)
        mv = info.min
        rng = info.max-info.min
        fromto = 2.0/rng
        
        data=(data.astype(to_t)-mv)*fromto-1.0
        return data.astype(to_t)
        
    else:
        from_size=from_t.itemsize*8
        to_size=to_t.itemsize*8
        from_signed=from_t.kind=='i'
        to_signed=to_t.kind=='i'
        
        if not from_signed:
            #change_sign
            data=data^(1<<(from_size-1))
        
        if from_size<to_size:
            data=data.astype(to_t)<<(to_size-from_size)
        else:
            data=(data>>(from_size-to_size)).astype(to_t)
        
        if not to_signed:
            #change_sign
            data=data^(1<<(to_size-1))
        
        return data

    
def fastWriteWave(filename,arr,samplerate,convertTo=None,loop=None,cues=None):
    snd=Sound(samplerate, initData=arr)
    writeWave(filename,snd,convertTo,loop)
    
def writeWave(filename, arr, samplerate, convertTo=None, loop=None,cues=None):
    if not(convertTo is None):
        arr=convert(arr,convertTo)
    if len(arr.shape)==1:
        arr = np.reshape(arr,(arr.shape[0],1))
        

    
        
    print("save",filename)
    frames = arr.shape[0]
    channels = arr.shape[1]
    bits = arr.itemsize*8
    byte_rate = channels*samplerate*arr.itemsize
    data_size = channels * frames * arr.itemsize
    rate=samplerate
    audioformat=[1,3][arr.dtype.kind=='f']

    
    if(audioformat==1):
        if(bits==8):
            arr = convert(arr,'uint8')
        elif(bits==16):
            arr = convert(arr,'int16')
        elif(bits==32):
            arr = convert(arr,'int32')
        elif(bits==64):
            arr = convert(arr,'int64')

    
    # loop (smpl)
    if not(loop is None):
        if type(loop) is bool:
            if loop:
                loop=(0, (frames-1),0)
            else:
                loop=()
    else:
        loop=()
    

    if type(loop) is tuple and loop!=():
        # A4 - 57, C5 - 60
        smplchunk=struct.pack("4sIIIIIIIIIIIIIIII", b"smpl", 60, 0, 0, 1000000000//rate, 60-3 , 0, 0, 0, 1,0,     0, loop[2], loop[0], loop[1],0,0 )
        
        print("loop:",loop)
    else:
        smplchunk=b""
        print("noloop:")
        
    if not(cues is None) and len(cues) > 0:
        cuechunk = b"cue "
        ncues = len(cues)
        cuechunk += struct.pack("I",4 + 24*ncues)
        cuechunk += struct.pack("I",ncues)
        for i in range(ncues):
            cuechunk += struct.pack("I",i+1) # ID
            cuechunk += struct.pack("I",cues[i]) # position
            cuechunk += b"data" # data
            cuechunk += struct.pack("I",0) # chunk start
            cuechunk += struct.pack("I",cues[i] * channels*arr.itemsize) # block start
            cuechunk += struct.pack("I",cues[i] * channels*arr.itemsize) # sample start
            
    else:
        cuechunk=b""
    
    
    
    riff_header=struct.pack("4sI4s",b"RIFF",44+data_size+len(smplchunk)+len(cuechunk), b"WAVE")
    fmt_chunk=struct.pack("4sIHHIIHH", b"fmt ", 16, audioformat, channels, rate, byte_rate, channels*(bits>>3), bits)
    data_header=struct.pack("4sI",b"data", data_size)
    
    fd=open(filename,"wb")
    fd.write(riff_header)
    fd.write(smplchunk)
    fd.write(fmt_chunk)
    fd.write(data_header)
    fd.write(bytes(arr))
    fd.write(cuechunk)
    fd.close()
    
def loadSound(filename):
    return loadWave(filename)

def loadWave(filename):
    with open(filename,"rb") as fd:
        riff_header = fd.read(12)
        RIFFb,full_size, WAVEb = struct.unpack("4sI4s", riff_header)
        if RIFFb!=b"RIFF" or WAVEb != b"WAVE":
            return np.array([])
        
        fmt=b''
        data=b''
        
        rest = full_size
        while rest > 0:
            r = fd.read(8)
            if len(r)!=8:
                break;
            chunk_id, chunk_size = struct.unpack("4sI",r)
            print(chunk_id,chunk_size)
            chunk_data = fd.read(chunk_size)
            rest -= chunk_size
            if chunk_id == b'fmt ':
                fmt = chunk_data
            elif chunk_id == b'data':
                data = chunk_data
        
        
        r_format = None
        audio_format, channels, rate, byte_rate, block_align, bits_per_sample = struct.unpack("HHIIHH", fmt)
        if audio_format == 1:
            if bits_per_sample == 8:
                r_format = np.uint8
            elif bits_per_sample == 16:
                r_format = np.int16
            elif bits_per_sample == 32:
                r_format = np.int32
            elif bits_per_sample == 64:
                r_format = np.int64
        elif audio_format == 3:
            if bits_per_sample == 32:
                r_format = np.float32
            elif bits_per_sample == 64:
                r_format = np.float64
            
        print("format",r_format)
        if r_format == None:
            return np.array([])
            
        snd = np.frombuffer(data,dtype = r_format)
        snd = convert(snd)
        
        return np.reshape(snd, (snd.shape[0]//channels, channels))
        