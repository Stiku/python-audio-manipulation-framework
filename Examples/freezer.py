#!/usr/bin/env python3

"""
"Freeze" sound by randomizing spectral phases
"""
import sys
sys.path.append("..")
import fastwave3 as fw
import numpy as np
import time
import os
import fx



OUTPUT_PREFIX="freeze"

orginal_file_path = sys.argv[1]
orginal_file_path_splitted = os.path.split(orginal_file_path)

output_file_name = ".".join(orginal_file_path_splitted[1].split(".")[:-1]) + "_freeze_"+str(int(time.time()*1000)) +".wav"

output_file_path = os.path.join(orginal_file_path_splitted[0] , output_file_name )

print("input",orginal_file_path)
print("output",output_file_path)

f1=sys.argv[1]
output_name = os.path.splitext(os.path.basename(f1))[0]
print(output_name)

inp=fw.loadSound(f1)



s = np.fft.rfft(inp,axis=0)

a=np.random.uniform(0.0,np.pi*2.0,s.shape[0])

a=np.cos(a)-np.sin(a)*1j

a = fx.set_channels(a, fx.get_channels(s))


s*=a


out=np.fft.irfft(s,axis=0)



#filename = OUTPUT_PREFIX+"_"+output_name+"_"+str(int(time.time()*1000)) +".wav"
fw.writeWave(output_file_path, out, 44100,'float32', loop=True)









