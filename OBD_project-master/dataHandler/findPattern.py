#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: findPattern.py

@time: 2019/2/22 13:31

@desc:

'''
import numpy as np
import xlrd
# load raw data into workspace
from xlwt import Workbook


def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 58  # 结束的行

    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # orientation X,Y; acceleration X,Y, SMA X,Y; time
        for i in range(1, 4):
            values.append(row[i])
        list_values.append(values)
    print(list_values)
    # datamatrix = np.array(list_values)
    # print(datamatrix)
    return list_values


def write_data(dataTemp, table):
    print(dataTemp)
    h = len(dataTemp)
    l = len(dataTemp[0])
    # [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            table.write(i, j, dataTemp[i][j])


def write_excel(data):
    file_w = Workbook()
    sheet1 = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
    write_data(data, sheet1)
    file_w.save('data.xls')
    return 0


def checkMotion(dataMatrix, windowSize):
    flag = []
    startPoint = endPoint = 0
    while startPoint < len(dataMatrix):
        accF = braF = turnF = 0
        endPoint = startPoint
        while endPoint > 0 and (int(dataMatrix[startPoint][0]) - int(dataMatrix[endPoint][0])) <= windowSize:
            d = int(dataMatrix[startPoint][0]) - int(dataMatrix[endPoint][0])
            print(dataMatrix[startPoint][0])
            print(".--.", int(dataMatrix[endPoint][0]))
            print(".--.", int(dataMatrix[endPoint][0]))
            print(int(dataMatrix[startPoint][0]) - int(dataMatrix[endPoint][0]))
            if dataMatrix[endPoint][2] == 'speedup':
                accF += 1
            elif dataMatrix[endPoint][2] == 'swerve':
                turnF += 1
            elif dataMatrix[endPoint][2] == 'brake':
                braF += 1
            endPoint -= 1
        flag.append([accF, turnF, braF])
        startPoint += 1
    print(flag)
    print(len(flag))
    print(len(flag[0]))
    return flag


def main():
    data = read_excel('eventlogger.xlsx')
    flag = checkMotion(data, 100)
    write_excel(flag)


if __name__ == '__main__':
    main()
