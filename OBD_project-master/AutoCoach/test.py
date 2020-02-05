# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
# import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

#    whenever it is full.
win.nextRow()
p3 = win.addPlot()
# Use automatic downsampling and clipping to reduce the drawing load
p3.setDownsampling(mode='peak')
p3.setClipToView(True)
p3.setRange(xRange=[-100, 0])
p3.setLimits(xMax=0)
curve3 = p3.plot(pen='r')
curve1 = p3.plot(pen='y')


data3 = np.empty(10)
ptr3 = 0

def update2():
    global data3, ptr3, curve3, curve1
    if (ptr3 == 0):
        print(data3)
    data3[ptr3] = np.random.normal()
    if(ptr3==0):
        print(data3)
    ptr3 += 1
    if ptr3 >= data3.shape[0]:
        tmp = data3
        data3 = np.empty(data3.shape[0] * 2)
        data3[:tmp.shape[0]] = tmp
    if(ptr3%4==0):
        curve1.setData([0])
        curve1.setPos(-ptr3, 0)
        curve3.setData(data3[:ptr3])
        curve3.setPos(-ptr3, 0)
    else:
        curve3.setData([0])
        curve3.setPos(-ptr3, 0)
        curve1.setData(data3[:ptr3])
        curve1.setPos(-ptr3, 0)



# update all plots
def update():
    # update1()
    update2()
    # update3()
timer = pg.QtCore.QTimer()
timer.timeout.connect(update2)
timer.start(500)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()