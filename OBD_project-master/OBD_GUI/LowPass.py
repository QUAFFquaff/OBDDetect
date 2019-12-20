from numpy import *
import math


from scipy import signal

import numpy as np

import matplotlib.pyplot as pl

import matplotlib

import math

N = 0
n = []
fileObj = open("rawX.txt",'r')
for line in fileObj.readlines():
    rawx = double(line)
    n.append(rawx)
    N += 1

print("N is deal ",N)
axis_x = np.linspace(0,N,num = N)

x = n
pl.subplot(221)
pl.plot(axis_x,x)
pl.title(u'raw x data')
pl.axis('tight')

b,a = signal.butter(3,0.154,'low')
sf = signal.filtfilt(b,a,x)


pl.subplot(222)
pl.plot(axis_x,sf)
pl.title(u'Low Pass')
pl.axis('tight')
pl.show()

fileout = open('OutOBDX.txt','w')
for i in sf:
    fileout.write(str(i))
    fileout.write('\n')
fileout.close()

