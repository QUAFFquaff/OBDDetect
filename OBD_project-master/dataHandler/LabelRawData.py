#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: LabelRawData.py

@time: 2019/2/7 19:16

@desc:

'''
import numpy as np
import xlrd

from xlwt import *

file = 'STATUS.xlsx'
breakV = []
speedV = []


def calcSwerve(data):
    hflength = int(len(data) / 2)
    maxAX = max(data[:, 2])
    maxAY = max(data[:, 3])
    minAX = min(data[:, 2])
    minAY = min(data[:, 3])
    rangeAX = maxAX - minAX
    rangeAY = maxAY - minAY
    varAX = np.var(data[:, 2])
    varAY = np.var(data[:, 3])
    varOX = np.var(data[:, 0])
    varOY = np.var(data[:, 1])
    meanAX = np.mean(data[:, 2])
    meanAY = np.mean(data[:, 3])
    meanOX = np.mean(data[:, 0])
    meanOY = np.mean(data[:, 1])
    meanAX1 = np.mean(data[:hflength, 2])
    meanAX2 = np.mean(data[hflength:, 2])
    maxOX = max(data[:, 0])
    maxOY = max(data[:, 1])
    t = data[-1, -1] - data[0, -1]

    # return np.array([rangeAX,rangeAY,varAX,varAY,varOX,varOY,meanAX,meanAY,meanOX,meanOY,meanAX1,meanAX2,maxOX,maxOY,minAY,t])
    return [rangeAX, rangeAY, varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY, meanAX1, meanAX2, maxOX,
            maxOY, minAY, t]


def init():
    swerveV = []
    rawData = read_excel()
    rawData = rawData.astype(np.double)

    length = len(rawData)
    breakF = swerveF = speedF = 0
    # detect swerve
    for i in range(1, len(rawData)):
        if rawData[i, 5] > 0.025 or rawData[i, 5] < -0.025:
            swerveF += 1
        elif swerveF >= 4:
            swerveV.append(calcSwerve(rawData[i - swerveF:i, ]))
            swerveF = 0
        else:
            swerveF = 0

    # detect break
    for i in range(1, len(rawData)):
        if rawData[i, 4] < -0.1:
            breakF += 1
        elif breakF >= 4:
            breakV.append(calcSwerve(rawData[i - breakF:i, ]))
            breakF = 0
        else:
            breakF = 0;

        if rawData[i, 4] > 0.0025:
            speedF += 1
        elif speedF >= 6:
            speedV.append(calcSwerve(rawData[i - speedF:i, ]))
            speedF = 0
        else:
            speedF = 0;
    print("--------------")
    # print(swerveV)
    # normalization(swerveV)
    # data = np.array(swerveV)
    # print(data[0][0])
    # write_excel(swerveV,breakV,speedV)
    write_excel(normalization(swerveV), normalization(breakV), normalization(speedV))
    return


# load raw data into workspace
def read_excel():
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    # print(table)
    # nrows = table.nrows #行数
    # ncols = table.ncols #列数
    # c1=arange(0,nrows,1)
    # print(c1)

    start = 0  # 开始的行
    end = 35858  # 结束的行

    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # orientation X,Y; acceleration X,Y, SMA X,Y; time
        for i in [9, 10, 18, 19, 21, 22, 2]:
            # print(value)
            values.append(row[i])
        list_values.append(values)
    # print(list_values)
    datamatrix = np.array(list_values)
    # print(datamatrix)
    return datamatrix


def write_data(dataTemp, table):
    data = np.array(dataTemp)
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            table.write(i, j, data[i][j])


def write_excel(swerveData, breakData, speedData):
    file_w = Workbook()
    sheet1 = file_w.add_sheet(u'swerve Data', cell_overwrite_ok=True)  # 创建sheet
    sheet2 = file_w.add_sheet(u'break Data', cell_overwrite_ok=True)  # 创建sheet
    sheet3 = file_w.add_sheet(u'speed Data', cell_overwrite_ok=True)  # 创建sheet
    write_data(swerveData, sheet1)
    write_data(breakData, sheet2)
    write_data(speedData, sheet3)
    file_w.save('data.xls')
    return 0


def normalization(data):
    data = np.mat(data)
    height = len(data)
    width = 16
    maxi = 0
    for i in range(width):
        maxi = 0
        for j in range(height):
            if maxi < data[j, i]:
                maxi = data[j, i]
            elif maxi < abs(data[j, i]):
                maxi = abs(data[j, i])
        print("maxi:    ", maxi)
        for j in range(height):
            data[j, i] = data[j, i] / maxi
            if data[j, i] > 1:
                print(j, "--", i, "----", maxi)
                return
        print(j)

    # print(data[0])
    return data


# for i in range(2):
#     print(i)
init()
# read_excel()
