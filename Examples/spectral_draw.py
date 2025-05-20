#!/usr/bin/env python3
"""
Image to sound.
OpenCV is required to load the image.
"""

import sys
sys.path.append("..")
import fastwave3 as fw
import numpy as np
import time
import os
import fx
import cv2


input_file = sys.argv[1]

OUTPUT_PREFIX="spct_draw"


def draw(canvas, x, y, GRID_X):
	y=np.array(y)
	n=canvas.shape[0]
	x1=(n*x//GRID_X)
	x2=(n*(x+1)//GRID_X)
	to_draw=np.zeros(n)
	to_draw[x1:x2]=np.random.random(x2-x1)-0.5
	
	to_draw = np.fft.rfft(to_draw)
	
	scaled_y = y[np.arange(to_draw.shape[0])*y.shape[0]//to_draw.shape[0] ]
	to_draw *= scaled_y
	
	to_draw = np.fft.irfft(to_draw)
	
	if(GRID_X>=3):
		x4=(n*(x-1)//GRID_X)
		x5=(n*(x+2)//GRID_X)
		to_draw=np.roll(to_draw,-x4)
		
		to_draw[0:(x5-x4)] *= np.cos(np.linspace(-np.pi/2,np.pi/2,x5-x4,endpoint=False))
		to_draw[(x5-x4):] *= 0
		
		to_draw=np.roll(to_draw,+x4)
	
	
	
	
	
	canvas+=to_draw
	


img=cv2.imread(input_file).astype(np.float32)
b,g,r = cv2.split(img)
img = (r+g+b)/3.0

mn = np.min(img)
mx = np.max(img)
# normalize
img = (img - mn)/ (mx - mn)

avg = np.average(img)
if avg > 0.5:
    img = 1.0-img


GRID_X=img.shape[1]
GRID_Y=img.shape[0]
canvas=np.zeros(65536*4)

for x in range(0,GRID_X):
	print(x,"/",GRID_X)
	to_draw=img[::-1,x]
	
	draw(canvas,x,to_draw,GRID_X)











snd=canvas
snd=fx.normalized(snd)

filename = OUTPUT_PREFIX+"_"+"_"+str(int(time.time()*1000)) +".wav"
fw.writeWave(filename, snd, 44100,'float32')
	
	
	
	
	
	



