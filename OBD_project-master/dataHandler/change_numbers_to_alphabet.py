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
    datamatrix = read_excel('ForLDA0415.xls')
    write_excel(np.array(datamatrix), 'ForLDA0415Alph.xls')


def change_n_to_a(temp):
    if temp == 1:
        temp = "a"
    elif temp == 5:
        temp = "b"
    elif temp == 9:
        temp = "c"
    elif temp == 0:
        temp = "h"
    elif temp == 4:
        temp = "i"
    elif temp == 8:
        temp = "j"
    elif temp == 2:
        temp = "o"
    elif temp == 6:
        temp = "p"
    elif temp == 10:
        temp = "q"
    elif temp == 3:
        temp = "v"
    elif temp == 7:
        temp = "w"
    elif temp == 11:
        temp = "x"
    return temp


def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    list_values = []
    end = len(table.col_values(0))  # from the first line to last line
    for x in range(end):
        values = []
        row = table.row_values(x)
        for i in [0, 1, 2]:
            values.append(row[i])
        values[2] = change_n_to_a(values[2])
        list_values.append(values)
    return list_values


def write_data(dataTemp, table):
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
