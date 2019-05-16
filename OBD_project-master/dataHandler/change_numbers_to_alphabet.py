#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: change_numbers_to_alphabet.py

@time: 2019/4/16 9:52

@desc:

'''
import xlrd
import numpy as np
from xlwt import Workbook


def change_number_label_to_alphabet():
    datamatrix = read_excel('ForLDA3.xlsx')
    write_excel(np.array(datamatrix), 'ForLDA3Alph.xls')


def read_excel(file):
    time_window = 40 * 1000
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    start = 0  # 开始的行
    # end = 164  # 结束的行
    end = 66  # 结束的行
    list_values = []
    end = len(table.col_values(0))  # from the first line to last line
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # orientation X,Y; acceleration X,Y, SMA X,Y; time
        for i in [0, 1, 2]:
            # print(value)
            values.append(row[i])
        if values[2] == 1:
            values[2] = "a"
        elif values[2] == 5:
            values[2] = "b"
        elif values[2] == 9:
            values[2] = "c"
        elif values[2] == 0:
            values[2] = "h"
        elif values[2] == 4:
            values[2] = "i"
        elif values[2] == 8:
            values[2] = "j"
        elif values[2] == 2:
            values[2] = "o"
        elif values[2] == 6:
            values[2] = "p"
        elif values[2] == 10:
            values[2] = "q"
        elif values[2] == 3:
            values[2] = "v"
        elif values[2] == 7:
            values[2] = "w"
        elif values[2] == 11:
            values[2] = "x"
        list_values.append(values)
    # print(list_values)
    return list_values


def write_data(dataTemp, table):
    # print(dataTemp)
    [h, l] = dataTemp.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            table.write(i, j, dataTemp[i][j])


def write_excel(data, file_name):
    file_w = Workbook()
    table = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
    write_data(data, table)
    file_w.save(file_name)


change_number_label_to_alphabet()
