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
            term += notebook[random.randint(4, 11)]
    return "'" + term + "'"


def makeLevel1():
    length = int(random.gauss(2.5, 2))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 99)
        if threshold < 35:
            index = random.randint(0, 3)
            term += notebook[index]
        elif threshold>90:
            term += notebook[random.randint(8, 11)]
        else:
            term += notebook[random.randint(4, 7)]
    return "'" + term + "'"

def makeLevel2():
    length = int(random.gauss(2.9, 1.9))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 99)
        if threshold < 20:
            index = random.randint(0, 3)
            term += notebook[index]
        elif threshold > 70:
            term += notebook[random.randint(8, 11)]
        else:
            term += notebook[random.randint(4, 7)]
    return "'" + term + "'"

def makeLevel3():
    length = int(random.gauss(3, 1.9))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 99)
        if threshold < 20:
            index = random.randint(0, 3)
            term += notebook[index]
        elif threshold > 40:
            term += notebook[random.randint(8, 11)]
        else:
            term += notebook[random.randint(4, 7)]
    return "'" + term + "'"




def makeDocument(level):
    document = '['
    for i in range(100):
        if level == 0:
            temp = makeLevel0()
        elif level == 1:
            temp = makeLevel1()
        elif level == 2:
            temp = makeLevel2()
        elif level == 3:
            temp = makeLevel3()
        if temp == "!": continue
        document += temp + ", "
    return document + "]"


def main():
    data = ""
    for j in range(4):
        for i in range(50):
            data += makeDocument(j) + ",\n"
    write(data)
    data1 = readText()
    print(readText())


def write(data):
    try:
        with open('fakeData.txt', 'w') as f:
            f.write(data)
    finally:
        if f:
            f.close()


def readText():
    try:
        f = open('fakeData.txt', 'r')  # 打开文件
        data = f.read()  # 读取文件内容
        print(data)
        # return data[0]
    finally:
        if f:
            f.close()
            return


main()
