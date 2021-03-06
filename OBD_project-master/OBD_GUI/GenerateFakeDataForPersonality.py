import numpy as np
from xlrd import *
from xlutils.copy import copy
import random


notebook = "ahovbipwcjqx"
duration = []
termList = []  # put all the terms(event) in one trip


def write_data(dataTemp, table, row):  # write features in excel
    data = np.array(dataTemp)
    l = len(data)  # h为行数，l为列数
    for j in range(l):
        table.write(row, j, data[j])


def makeLevel0():  # this is for safe driver
    length = int(random.gauss(4, 1.2))
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
            if threshold >= 3:
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

# this is for anxious driver
def makeLevel1():
    length = int(random.gauss(7, 2.2))
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
            if threshold < 40:
                index = random.randint(0, 3)
                term += notebook[index]
                termList.append(notebook[index])
            elif threshold < 40:
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

# reckless_Prob = 20
# this is for reckless driver
def makeLevel2():
    # global  reckless_Prob
    length = int(random.gauss(5, 1.9))
    if length <= 0:
        return "!"
    term = ''
    eventTime = 0
    totalTime = 40
    average = totalTime / length
    if average >16:   # ensure the event will not last too long
        average = 10
    mood = -1
    for i in range(length):
        if totalTime > 1:
            threshold = random.randint(0, 99)
            if mood == -1:
                if threshold < 40:
                    index = random.randint(0, 7)
                    term += notebook[index]
                    termList.append(notebook[index])
                elif threshold <70:
                    index = random.randint(4, 11)
                    term += notebook[index]
                    termList.append(notebook[index])
                else:
                    index = random.randint(8, 11)
                    term += notebook[index]
                    termList.append(notebook[index])
                    mood = 1
            else:
                threshold = random.randint(0, 99)
                mood = -1
                if threshold < 60:
                    index = random.randint(0, 7)
                    term += notebook[index]
                    termList.append(notebook[index])
                elif threshold < 80:
                    index = random.randint(4, 11)
                    term += notebook[index]
                    termList.append(notebook[index])
                else:
                    index = random.randint(8, 11)
                    term += notebook[index]
                    termList.append(notebook[index])
                    mood = 1
                    # reckless_Prob+= 40
            eventTime = random.uniform(1, average)
            duration.append(eventTime)
            totalTime -= eventTime
        else:
            break
    return "'" + term + "'"

# this is for angry driver
def makeLevel3():
    length = int(random.gauss(5, 1.9))
    if length <= 0:
        return "!"
    term = ''
    eventTime = 0
    totalTime = 40
    average = totalTime / length
    if average >16:   # ensure the event will not last too long
        average = 10
    mood = -1
    for i in range(length):
        if totalTime > 1:
            if mood == -1:
                threshold = random.randint(0, 99)
                if threshold < 40:
                    index = random.randint(4, 7)
                    term += notebook[index]
                    termList.append(notebook[index])
                elif threshold < 60:
                    index = random.randint(0, 3)
                    term += notebook[index]
                    termList.append(notebook[index])
                else:
                    index = random.randint(8, 11)
                    term += notebook[index]
                    termList.append(notebook[index])
            else:
                mood = -1
                threshold = random.randint(0, 99)
                if threshold < 10:
                    index = random.randint(0, 7)
                    term += notebook[index]
                    termList.append(notebook[index])
                elif threshold < 40:
                    index = random.randint(4, 11)
                    term += notebook[index]
                    termList.append(notebook[index])
                else:
                    mood = 1
                    index = random.randint(8, 11)
                    term += notebook[index]
                    termList.append(notebook[index])
            eventTime = random.uniform(1, average)
            duration.append(eventTime)
            totalTime -= eventTime
        else:
            break
    return "'" + term + "'"


def calculateSafe():    # calculate the safe event frequency
    totalEvent = len(termList)
    safeEvent = 0
    for i in termList:
        if i=='a' or i=='h' or i=='o' or i == 'v':
            safeEvent+=1
    frequency = safeEvent/totalEvent
    return frequency


def calculateMedium():  # calculate the medium risk event frequency
    totalEvent = len(termList)
    mediumEvent = 0
    for i in termList:
        if i=='b' or i=='i' or i=='p' or i == 'w':
            mediumEvent+=1
    frequency = mediumEvent/totalEvent
    return frequency


def calculateHigh():  # calculate the high risk event frequency
    totalEvent = len(termList)
    highEvent = 0
    for i in termList:
        if i=='c' or i=='j' or i=='q' or i == 'x':
            highEvent+=1
    frequency = highEvent/totalEvent
    return frequency



def makeDocument(runNum,safe, anxious, reckless):  # random pick different level of pattern to compose the document
    if runNum > safe:
        temp = makeLevel0()
    elif runNum > anxious:
        temp = makeLevel1()
    elif runNum >reckless:
        temp = makeLevel2()
    else:
        temp = makeLevel3()
    return temp

def choosePersonality(data,safe, anxious, reckless):
    global duration
    global termList

    for j in range(100):  # generate 100 careful driver
        totaltime = random.randint(100, 200)  # how many 40 sec in on trip, also the pattern
        document = '['
        for i in range(totaltime):
            runNum = random.uniform(0, 100)
            word = makeDocument(runNum, safe, anxious, reckless)
            if word == '!': continue
            document += word + ","
        document += "]"

        frequency_Safe = calculateSafe()
        frequency_Medium = calculateMedium()
        frequency_high = calculateHigh()

        data += document + ",\n"

        print(document)
        print(termList)
        print(duration)
        print(frequency_Safe)
        print(frequency_Medium)
        print(frequency_high)

        numOfLowScore = 0
        numOfHighScore = 0
        for i in range(totaltime):
            score =3
            if score< 75:
                numOfLowScore = numOfLowScore + 1
            else:
                numOfHighScore = numOfHighScore + 1

        oldwd = open_workbook('ForKMeans.xls', formatting_info=True)
        sheet = oldwd.sheet_by_index(0)
        rowNum = sheet.nrows
        newwb = copy(oldwd)
        newWs = newwb.get_sheet(0)
        write_data(np.array([frequency_Safe, frequency_Medium, frequency_high]), newWs, rowNum)
        newwb.save('ForKMeans.xls')

        duration = []
        termList = []
    return data

def main():
    pass
    # data = ""
    # data = choosePersonality(data, 3, 2, 1)  # safe
    # data = choosePersonality(data, 15, 5, 2)
    # data = choosePersonality(data, 15, 12, 2)
    # data = choosePersonality(data, 15, 13, 10)
    # write(data)





def write_fakedata(data):
    try:
        with open('fakeDataForPersonality.txt', 'w') as f:
            f.write(data)
    finally:
        if f:
            f.close()


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


def read_txt_score():
    with open('scores00.txt', 'r') as f:
        lines = f.readlines()
    file_list = []
    for line in lines:
        pattern_list = []
        patterns = line.split(",")
        for i in range(len(patterns)):
            # if i % 2 != 0:
            pattern_list.append(patterns[i])
        file_list.append(pattern_list)
    return file_list

def read_txt_score1():
    with open('scores00.txt', 'r') as f:
        lines = f.readlines()
    file_list = []
    print(len(lines))
    for line in lines:

        line = line.split('[')[-1].split(']')[0]
        # print(line)
        pattern_list = []
        patterns = line.split(",")
        for i in range(len(patterns)):
            # if i % 2 != 0:
            pattern_list.append(patterns[i])
        file_list.append(pattern_list)
    return file_list

main()