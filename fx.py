#!/usr/bin/env python
import numpy as np

def mix_internal(arr1,arr2):
    ch1 = get_channels( arr1 ) 
    ch2 = get_channels( arr2 )
    if( ch1 != ch2 ):
        m = max( ch1, ch2 )
        arr1 = set_channels( arr1, m )
        arr2 = set_channels( arr2, m )
    
    if len(arr1.shape)==1:
        s1 = arr1.shape[0]
        s2 = arr2.shape[0]
        out=np.zeros(max(s1,s2))
        out[:s1]+=arr1[:]
        out[:s2]+=arr2[:]
        return out
    if len(arr.shape)==2:
        s1 = arr1.shape[0]
        s2 = arr2.shape[0]
        out=np.zeros((max(s1,s2),arr1.shape[1]))
        out[:s1,:]+=arr1[:,:]
        out[:s2,:]+=arr2[:,:]
        return out

def mix(*arrs):
    assert(len(arrs)>=1)
    out = arrs[0]
    for i in range(1,len(arrs)):
        out = mix_internal(out,arrs[i])
    return out

def set_channels(arr,to):
    assert(len(arr.shape)==1 or len(arr.shape)==2)
    if len(arr.shape)==1:
        arr_out=np.zeros((arr.shape[0],to),dtype=arr.dtype)
        for i in range(to):
            arr_out[:,i]=arr[:]
        return arr_out
        
    elif len(arr.shape)==2:
        if to!=arr.shape[1]:
            arr_out=np.zeros((arr.shape[0],to),dtype=arr.dtype)
            for i in range(to):
                arr_out[:,i]=arr[:,i%arr.shape[1]]
            return arr_out;
        else:
            return arr

def get_channels(arr):
    if len(arr.shape)==1:
        return 1;
    elif len(arr.shape)==2:
        return arr.shape[1];
        

def interpolate_sinc(arr, xs, wrap=False, window_width=1):
    #window_width|=1
    xi=np.floor(xs)
    xf=xs-xi
    xi=xi.astype('int')
    lng=arr.shape[0]
    
    out=np.zeros(xs.shape)
    
    if wrap:
        for i in range(-window_width+1, window_width):
            #print(i)
            out+= arr[(xi+i)%lng] * np.sinc((-xf+i))*np.sinc((-xf+i)/window_width)
    else:
        for i in range(-window_width+1, window_width):
            out+= arr[np.clip( xi+i,0, lng-1)] * np.sinc((-xf+i))*np.sinc((-xf+i)/window_width)
    
    return out

def interpolate_linear(arr, xs, wrap=False):
    xi=np.floor(xs)
    xf=xs-xi
    xi=xi.astype('int')
    
    lng = arr.shape[0]
    x1=xi
    x2=xi+1
    if wrap:
        x1=x1%lng
        x2=x2%lng
    else:
        x1=np.clip(x1,0,lng-1)
        x2=np.clip(x2,0,lng-1)
    out = arr[x1]*(1-xf) + arr[x2]*(xf)
    return out

def interpolate_cosine(arr, xs, wrap=False):
    xi=np.floor(xs)
    xf=xs-xi
    xi=xi.astype('int')
    
    lng = arr.shape[0]
    x1=xi
    x2=xi+1
    if wrap:
        x1=x1%lng
        x2=x2%lng
    else:
        x1=np.clip(x1,0,lng-1)
        x2=np.clip(x2,0,lng-1)
    out = arr[x1] + (arr[x2]-arr[x1]) * (1 - np.cos(xf*np.pi) )*0.5
    return out

def normalize(arr):
    mx=np.max(np.abs(arr))
    if mx!=0:
        mx=1/mx
        arr*=mx

def normalized(arr):
    mx=np.max(np.abs(arr))
    if mx!=0:
        mx=1/mx
        arr=arr*mx
        return arr
    return arr.copy()


