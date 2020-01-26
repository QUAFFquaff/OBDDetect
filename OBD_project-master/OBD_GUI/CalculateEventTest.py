import re
import numpy as np
from xlrd import *
from xlutils.copy import copy

def write_data(dataTemp, table, row):  # write features in excel
    data = np.array(dataTemp)
    l = len(data)  # h为行数，l为列数
    for j in range(l):
        table.write(row, j, data[j])

def calculateSafe(termList):    # calculate the safe event frequency
    totalEvent = len(termList)
    safeEvent = 0
    for i in termList:
        if i=='a' or i=='h' or i=='o' or i == 'v':
            safeEvent+=1
    frequency = safeEvent/totalEvent
    return frequency


def calculateMedium(termList):  # calculate the medium risk event frequency
    totalEvent = len(termList)
    mediumEvent = 0
    for i in termList:
        if i=='b' or i=='i' or i=='p' or i == 'w':
            mediumEvent+=1
    frequency = mediumEvent/totalEvent
    return frequency


def calculateHigh(termList):  # calculate the high risk event frequency
    totalEvent = len(termList)
    highEvent = 0
    for i in termList:
        if i=='c' or i=='j' or i=='q' or i == 'x':
            highEvent+=1
    frequency = highEvent/totalEvent
    return frequency



def read_txt_pattern():
    with open('fakeData.txt', 'r') as f:
        lines = f.readlines()
    file_list = []
    for line in lines:
        pattern_list = []
        patterns = line.split("\'")
        for i in range(len(patterns)):
            if i % 2 != 0:
                pattern_list.append(patterns[i])
        file_list.append(pattern_list)
    return file_list

def main():
    data = read_txt_pattern()
    for d in data:
        temp = ''
        for a in d:
            temp += a
        print(calculateHigh(temp))
        print(calculateMedium(temp))
        print(calculateSafe(temp))
        frequency_Safe = calculateSafe(temp)
        frequency_Medium = calculateMedium(temp)
        frequency_high = calculateHigh(temp)
        oldwd = open_workbook('ForKMeans.xls', formatting_info=True)
        sheet = oldwd.sheet_by_index(0)
        rowNum = sheet.nrows
        newwb = copy(oldwd)
        newWs = newwb.get_sheet(0)
        write_data(np.array([frequency_Safe, frequency_Medium, frequency_high]), newWs, rowNum)
        newwb.save('ForKMeans.xls')



if __name__ == '__main__':
    main()
