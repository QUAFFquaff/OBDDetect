#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: makeData.py

@time: 2019/6/3 2:41

@desc:

'''
import random

notebook = "ahovbipwcjqx"


def makeLevel0():
    length = int(random.gauss(2.5, 2))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 9)
        if threshold != 9:
            index = random.randint(0, 3)
            term += notebook[index]
        else:
            term += notebook[random.randint(3, 11)]
    print(term)
    return "'" + term + "'"


def makeLevel1():
    length = int(random.gauss(3.1, 2))
    if length <= 0:
        return
    term = ''
    for i in range(length):
        threshold = random.randint(0, 9)
        if threshold != 9:
            index = random.randint(0, 3)
            term += notebook[index]
        else:
            term += notebook[random.randint(3, 11)]
    print(term)


def makeDocument():
    document = '['
    for i in range(100):
        temp = makeLevel0()
        if temp == "!": continue
        document += temp + ", "
    return document + "]"

def main():
    data = ""
    for i in range(50):
        data += makeDocument()+",\n"
    print(data)
    write(data)

def write(data):
    try:
        with open('fakeData.txt', 'w') as f:
            f.write(data)
    finally:
        if f:
            f.close()

main()
