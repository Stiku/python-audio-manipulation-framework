#!/usr/bin/env python3
"""
Sierpiński triangle spectral generator
"""

import sys
sys.path.append("..")
import fastwave3 as fw
import numpy as np
import time
import os
import fx



OUTPUT_PREFIX="sierp"


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
	
	

GRID_X=256
GRID_Y=256
canvas=np.zeros(65536*4)

for x in range(0,GRID_X):
	print(x)
	#to_draw=[ (((x-(y//2))&(y))==0)*1 for y in range(GRID_Y) ]
	to_draw=[ (((x)&(y))==0)*1 for y in range(GRID_Y) ]
	
	draw(canvas,x,to_draw,GRID_X)











snd=canvas
#snd_out=fx.normalized(snd_out)

filename = OUTPUT_PREFIX+"_"+"_"+str(int(time.time()*1000)) +".wav"
fw.writeWave(filename, snd, 44100,'float32')
	
	
	
	
	
	



