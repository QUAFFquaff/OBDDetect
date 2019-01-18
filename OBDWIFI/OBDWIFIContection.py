#!/usr/bin/env python

# encoding: utf-8

'''

@author: Leo

@contact: 13032459912@163.com

@file: OBDWIFIContection.py

@time: 2019/1/6 20:46

@desc:

'''
import obd
import time


def getData():
    connection = obd.OBD()
    start = time.time()
    r = connection.query(obd.commands.SPEED) # returns the response from the car
    end = time.time()
    elapsed = end - start
    print(r)
    print(elapsed)

if __name__ == '__main__':
    getData()