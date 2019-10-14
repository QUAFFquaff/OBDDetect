import numpy as np
from xlrd import *
from xlutils.copy import copy
import random


notebook = "ahovbipwcjqx"
durationOverspeed = 0
duration = []
termList = []


def write_data(dataTemp, table, row):
    data = np.array(dataTemp)
    l = len(data)  # h为行数，l为列数
    for j in range(l):
        table.write(row, j, data[j])


def makeLevel0():
    length = int(random.gauss(2.5, 2))
    if length <= 0:
        return "!"
    term = ''
    eventTime = 0
    totalTime = 40
    average = totalTime / length
    if average >16:
        average = 10
    for i in range(length):
        if totalTime>1:
            threshold = random.randint(0, 99)
            if threshold != 9:
                index = random.randint(0, 3)
                term += notebook[index]
                termList.append(notebook[index])
            else:
                index = random.randint(4, 11)
                term += notebook[index]
                termList.append(notebook[index])
            eventTime = random.uniform(1,average)
            duration.append(eventTime)
            totalTime -= eventTime
        else:
            break
    return "'" + term + "'"


def makeLevel1():
    length = int(random.gauss(2.5, 2))
    if length <= 0:
        return "!"
    term = ''
    eventTime = 0
    totalTime = 40
    average = totalTime / length
    if average >16:
        average = 10
    for i in range(length):
        if totalTime > 1:
            threshold = random.randint(0, 99)
            if threshold < 30:
                index = random.randint(0, 3)
                term += notebook[index]
                termList.append(notebook[index])
            else:
                index = random.randint(4, 7)
                term += notebook[index]
                termList.append(notebook[index])
            eventTime = random.uniform(1, average)
            duration.append(eventTime)
            totalTime -= eventTime
        else:
            break
    return "'" + term + "'"

def makeLevel2():
    length = int(random.gauss(3.5, 1.5))
    if length <= 0:
        return "!"
    term = ''
    eventTime = 0
    totalTime = 40
    average = totalTime / length
    if average >16:   # ensure the event will not last too long
        average = 10
    for i in range(length):
        if totalTime > 1:
            threshold = random.randint(0, 99)
            if threshold < 10:
                index = random.randint(0, 7)
                term += notebook[index]
                termList.append(notebook[index])
            elif threshold > 75:
                index = random.randint(4, 11)
                term += notebook[index]
                termList.append(notebook[index])
            else:
                index = random.randint(4, 7)
                term += notebook[random.randint(4, 7)]
                termList.append(notebook[index])
            eventTime = random.uniform(1, average)
            duration.append(eventTime)
            totalTime -= eventTime
        else:
            break
    return "'" + term + "'"

def makeLevel3():
    length = int(random.gauss(3, 1.9))
    if length <= 0:
        return "!"
    term = ''
    eventTime = 0
    totalTime = 40
    average = totalTime / length
    if average >16:   # ensure the event will not last too long
        average = 10
    for i in range(length):
        if totalTime > 1:
            threshold = random.randint(0, 99)
            if threshold < 10:
                index = random.randint(4, 7)
                term += notebook[index]
                termList.append(notebook[index])
            else:
                index = random.randint(8, 11)
                term += notebook[index]
                termList.append(notebook[index])
            eventTime = random.uniform(1, average)
            duration.append(eventTime)
            totalTime -= eventTime
        else:
            break
    return "'" + term + "'"

def calculateSafe():
    totalEvent = len(termList)
    safeEvent = 0;
    for i in termList:
        if i=='a' or i=='h' or i=='o' or i == 'v':
            safeEvent+=1
    frequency = safeEvent/totalEvent
    return frequency

def calculateMedium():
    totalEvent = len(termList)
    mediumEvent = 0;
    for i in termList:
        if i=='b' or i=='i' or i=='p' or i == 'w':
            mediumEvent+=1
    frequency = mediumEvent/totalEvent
    return frequency

def calculateHigh():
    totalEvent = len(termList)
    highEvent = 0;
    for i in termList:
        if i=='c' or i=='j' or i=='q' or i == 'x':
            highEvent+=1
    frequency = highEvent/totalEvent
    return frequency

def calculateDensity():
    totalTime = 0
    time_high = 0
    for i in range(len(termList)):
        totalTime += duration[i]
        if termList[i] == 'c' or termList[i] == 'j' or termList[i] == 'q' or termList[i] == 'x':
            time_high += duration[i]
    density = time_high / totalTime
    return density

def calculateOverspeed():
    totalTime = 0
    time_overspeed = 0
    for i in range(len(termList)):
        totalTime += duration[i]
        if  termList[i] == 'j' or termList[i] == 'x':
            time_overspeed += duration[i]
            if i< len(termList):
                time_overspeed +=duration[i]
    over = time_overspeed / totalTime
    return over

def makeDocument(runNum):
    level0 = random.randint(20,70)  # range of first level
    level1 = random.randint(10,level0)  # range of second level
    level2 = random.randint(0,level1)  # range of third level
    if runNum > level0:
        temp = makeLevel0()
    elif runNum > level1:
        temp = makeLevel1()
    elif runNum >level2:
        temp = makeLevel2()
    else:
        temp = makeLevel3()
    return temp



def main():
    global duration
    global termList
    data = ""



    for j in range(500):
        totaltime = random.randint(50, 100)  # how many 40 sec in on trip, also the pattern
        document = '['
        for i in range(totaltime):
            runNum = random.uniform(0, 100)
            word = makeDocument(runNum)
            if word == '!': continue
            document += word + ","
        document += "]"

        frequency_Safe = calculateSafe()
        frequency_Medium = calculateMedium()
        frequency_high = calculateHigh()
        density_high = calculateDensity()
        durationOverspeed = calculateOverspeed()

        data += document + ",\n"


        print(document)
        print(termList)
        print(duration)
        print(frequency_Safe)
        print(frequency_Medium)
        print(frequency_high)
        print(density_high)
        print(durationOverspeed)

        oldwd = open_workbook('ForKMeans.xls', formatting_info=True)
        sheet = oldwd.sheet_by_index(0)
        rowNum = sheet.nrows
        newwb = copy(oldwd)
        newWs = newwb.get_sheet(0)
        write_data(np.array([frequency_Safe, frequency_Medium, frequency_high, density_high,durationOverspeed]), newWs, rowNum)
        newwb.save('ForKMeans.xls')

        duration = []
        termList = []
    write(data)

def write(data):
    try:
        with open('fakeData.txt', 'w') as f:
            f.write(data)
    finally:
        if f:
            f.close()

def write_data(dataTemp, table, row):
    data = np.array(dataTemp)
    l = len(data)  # h为行数，l为列数
    for j in range(l):
        table.write(row, j, data[j])

main()