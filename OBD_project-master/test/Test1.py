#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: Test1.py

@time: 2019/5/22 18:00

@desc:

'''
import concurrent.futures
import time
def main():
    time.sleep(1)
    print(5)


if __name__ == "__main__":
    test = [1,2,3]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(main())