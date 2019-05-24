import serial
import time
import numpy as np
import queue
import GUI
import threading
from scipy import signal
import pymysql
import pymysql.cursors
import joblib
import sys
import multiprocessing

import concurrent.futures
sys.path.append('../dataHandler/')
from LDAForEvent import *
from change_numbers_to_alphabet import change_n_to_a
from xlrd import *
from xlutils.copy import copy

matrix = np.array([[0.9988042, 0.00E+00, -0.03458038],
                   [-0.026682913, 0.63608, -0.770697297],
                   [0.021995888, 0.77162, 0.635319376]])

# matrix = np.array([[0.079935974, 0.00E+00, -0.9968],
#                    [-0.993610238,0.079, -0.079680179],
#                    [0.079680205, 0.99687, 0.006389762]])

samplingRate = 0  # the sampling rate of the data reading
std_window = 0  # the time window for standard deviation

time_window = 30  # time window for a word in LDA
svm_label_buffer = ""  # the word in a time window
trip_svm_buffer = ""  # save the whole trip's SVm label
LDA_flag = True  # if False, there are a event holding a time window, we should waiting for the end of event
time_window_score = 50
trip_score = 50
GUI_flag = False

timestamp = 0
speed = 0
gpsLa = None
gpsLo = None

# lock = threading.Lock()
# eventQueue = queue.Queue()
SVMResultQueue = queue.Queue()
# dataQueue = queue.Queue()  # put data into dataQueue for databse
SVM_flag = 0  # if bigger than 0, there are overlapped events in queue
overlapNum = 0  # the number of overlapped events

xstdQueue = queue.Queue(maxsize=19)
ystdQueue = queue.Queue(maxsize=19)


def getSerial():
    ser = serial.Serial(port='/dev/rfcomm0', baudrate=57600, timeout=0.5)
    if not ser.is_open:
        ser.open()
    return ser


def connectDB():
    connection = pymysql.connect(host='35.197.95.95',
                                 user='root',
                                 password='obd12345',
                                 db='DRIVINGDB',
                                 port=3306,
                                 charset='utf8')
    return connection


# record the events detected
class Event(object):
    def __init__(self, starttime, type):
        self.start = starttime
        self.type = type
        self.vect = []

    def setEndtime(self, endtime):
        self.end = endtime

    def getDuration(self):
        duration = (self.end - self.start)
        return duration

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def addValue(self, data):
        temp = []
        temp = self.vect
        temp.append(data)
        self.vect = temp
        return self.vect

    def getValue(self):
        return self.vect

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type


# to get the result label from SVM
class SVMResult(object):
    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getLabel(self):
        return self.label


class detectProcess(multiprocessing.Process):  # threading.Thread

    def __init__(self):
        multiprocessing.Process.__init__(self)

    def run(self):
        newrecord = 0

        global timestamp
        global speed
        # global gpsLa
        # global gpsLo
        global eventQueue
        global overlapNum
        global SVM_flag
        global LDA_flag
        global dataQueue

        lowpass = queue.Queue()
        BTserial = getSerial()
        obddata = ''
        obddata = obddata.encode('utf-8')

        lowpassCount = 0
        cutoff = 2 * (1 / samplingRate)  # cutoff frequency of low pass filter
        # low pass filter
        b, a = signal.butter(3, cutoff, 'low')

        while True:
            row = obddata + BTserial.readline()

            row = splitByte(row)
            if row != "":
                #print(row)
                timestamp = int(round(time.time() * 1000))
                speed = row[1]
                accy = row[2]
                accx = row[3]
                accz = row[4]
                gyox = row[5]
                gyoy = row[6]
                gyoz = row[7]
                acc = np.array([accy, accx, accz])
                acc = acc.astype(np.float64)

                # calibration
                acc = np.dot(matrix, acc)
                lowpass.put(acc)
                lowpassCount = lowpassCount + 1
                if (lowpassCount > 29):
                    accxsf = signal.filtfilt(b, a, self.getLowPass(lowpass, 'x'))
                    accysf = signal.filtfilt(b, a, self.getLowPass(lowpass, 'y'))
                    acczsf = signal.filtfilt(b, a, self.getLowPass(lowpass, 'z'))

                    print([speed,accxsf[-2],accysf[-2],acczsf[-2]])
                    # detect event
                    event = detectEvent(
                        [timestamp, speed, accysf[-2], accxsf[-2], acczsf[-2], gyox, gyoy, gyoz])
                    yevent = detectYEvent(
                        [timestamp, speed, accysf[-2], accxsf[-2], acczsf[-2], gyox, gyoy, gyoz])

                    # start a thread to store data into databse
                    dataQueue.put([row, timestamp])

                    # put the event into Queue
                    if not event is None:

                        if SVM_flag > 0:
                            overlapNum = overlapNum + 1
                        eventQueue.put(event)
                        SVM_flag = SVM_flag - 1
                        print("put acceleration or brake into svm")
                        LDA_flag = False
                    if not yevent is None:
                        data = yevent.getValue()
                        # max_gyo = max(max(data[:, 5:6]), abs(min(data[:, 5:6])))
                        # if max_gyo < 15:
                        #     yevent.setType(yevent.getType() + 2)
                        if SVM_flag > 0:
                            overlapNum = overlapNum + 1
                        eventQueue.put(yevent)
                        SVM_flag = SVM_flag - 1
                        print("put turn into svm")
                        LDA_flag = False

                    lowpass.get()
                    lowpassCount = lowpassCount - 1
            else:
                print("something wrong with bluetooth")

    def getLowPass(self, lowpass, opt):
        acc = []
        if opt == 'x':
            for i in range(lowpass.qsize()):
                temp = lowpass.get()
                lowpass.put(temp)
                acc.append(temp[1])
        if opt == 'y':
            for i in range(lowpass.qsize()):
                temp = lowpass.get()
                lowpass.put(temp)
                acc.append(temp[0])
        if opt == 'z':
            for i in range(lowpass.qsize()):
                temp = lowpass.get()
                lowpass.put(temp)
                acc.append(temp[2])

        return acc



class DataThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        global dataQueue
        while True:
            if dataQueue.qsize()>60:
                data = []
                while not dataQueue.empty():
                    data.append(dataQueue.get())
                try:
                    # 获取一个游标
                    connection = connectDB()
                    connection.autocommit(True)

                    if len(data) > 0:
                        for i in range(0, len(data)):
                            temp = data[i]
                            row = temp[0]
                            timestamp = temp[1]

                            mycursor = connection.cursor()
                            sql = "INSERT INTO STATUS(VIN,DEVICEID,TIME,SPEED,PARAM_1,PARAM_2,PARAM_3,LONGITUDE,LATITUDE,GYROX,GYROY,GYROZ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            val = (row[0], "zahraa", timestamp, row[1], row[2], row[3], row[4], "", "", row[5], row[6], row[7])
                            mycursor.execute(sql, val)
                            mycursor.close()
                finally:
                    connection.close()

    def stop(self):
        self.__running.clear()


# this thread for SVM classification
class SVMthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()
        self.score_queue = []

    def run(self):
        resultMatrix = []
        svm = joblib.load('svm.pkl')
        global overlapNum
        global eventQueue
        global SVMResultQueue
        global LDA_flag
        global svm_label_buffer

        while True:
            #  define type and intensity
            if SVM_flag==0:
                print("svm flag is 0")
            if (not eventQueue.empty()) and SVM_flag == 0:
                print("get event from detection")
                eventNum = overlapNum
                overlapNum = 0
                eventList = []
                for i in range(0, eventNum):
                    eventList.append(eventQueue.get())
                eventList = self.makeDecision(eventList)

                for i in range(0, eventNum):
                    if eventList[i] != None:
                        vect = np.array(eventList[i].getValue())
                        vect = vect.astype(np.float64)

                        # calculate the 23 features
                        vect = self.calcData(vect)
                        # nomaliz the 23 features
                        vect = self.nomalization(vect)

                        # predict the result
                        result = svm.predict([vect])  # result of SVM
                        score = svm.decision_function([vect])  # score of SVM for each tyeps
                        score = np.array(score[0])

                        if eventList[i].getType() >= 2:
                            index = np.argmax([score[2], score[3], score[6], score[7], score[10], score[11]])
                            if index == 0:
                                result = [2]
                            elif index == 1:
                                result = [3]
                            elif index == 2:
                                result = [6]
                            elif index == 3:
                                result = [7]
                            elif index == 4:
                                result = [10]
                            else:
                                result = [11]
                        elif eventList[i].getType() == 0:
                            index = np.argmax([score[0], score[4], score[8]])
                            if index == 0:
                                result = [0]
                            elif index == 1:
                                result = [4]
                            elif index == 2:
                                result = [8]
                        elif eventList[i].getType() == 1:
                            index = np.argmax([score[1], score[5], score[9]])
                            if index == 0:
                                result = [1]
                            elif index == 1:
                                result = [2]
                            elif index == 2:
                                result = [9]
                        SVMResultQueue.put(SVMResult(eventList[i].getStart(), eventList[i].getEnd(), result[0]))

                        self.saveResult(eventList[i].getStart(), eventList[i].getEnd(), result[0])
                        svm_label_buffer = svm_label_buffer + change_n_to_a(result[0])
                        LDA_flag = True

    def makeDecision(self, eventList):
        for i in range(0, len(eventList) - 2):
            if eventList[i]:
                factor1 = (eventList[i].getEnd() - eventList[i + 1].getStart()) / eventList[i].getDuration()
                factor2 = (eventList[i + 1].getEnd() - eventList[i].getEnd()) / eventList[i + 1].getDuration()
                if factor1 > 0.5 and factor2 < 0.5:
                    if eventList[i].getType() >= 2 > eventList[i + 1].getType():
                        eventList[i + 1] = None
                    elif eventList[i].getType() < 2 <= eventList[i + 1].getType():
                        eventList[i] = None
        return eventList

    def nomalization(self, vect):
        max = [0.619, 0.944, 0.546, 0.418, 0.208, 0.281, 6.075, 17.258, 0.286, 0.349, 3.901, 26.569, 22.12, 60.271,
               0.594,
               0.932, 0.097, 0.191, 90, 136,
               122.637, 29.291, 24.982]
        min = [0.034, 0.021, -0.302, -0.249, 0.009, 0.004, 0.325, 0.575, -0.312, -0.281, -3.816, -20.210, -0.061,
               -1.291,
               -0.063, -0.067, -0.539, -0.818, -76, 5,
               4.979, 0.408, 1.581]
        for i in range(len(vect)):
            vect[i] = (vect[i] - min[i]) / (max[i] - min[i])
        return vect

    def calcData(self, data):
        maxAX = max(data[:, 3])
        maxAY = max(data[:, 2])
        minAX = min(data[:, 3])
        minAY = min(data[:, 2])
        rangeAX = maxAX - minAX
        rangeAY = maxAY - minAY
        startAY = data[0, 3]
        endAY = data[-1, 3]
        varAX = np.std(data[:, 3])
        varAY = np.std(data[:, 2])
        varOX = np.std(data[:, 6])
        varOY = np.std(data[:, 5])
        meanAX = np.mean(data[:, 3])
        meanAY = np.mean(data[:, 2])
        meanOX = np.mean(data[:, 6])
        meanOY = np.mean(data[:, 5])
        maxOX = max(data[:, 6])
        maxOY = max(data[:, 5])
        t = (data[-1, 0] - data[0, 0]) / 1000
        meanSP = np.mean(data[:, 1])
        varSP = np.std(data[:, 1])
        differenceSP = data[-1, 2] - data[0, 2]
        maxSP = max(data[:, 2])
        return [rangeAX, rangeAY, startAY, endAY, varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY, maxOX,
                maxOY, maxAX, maxAY, minAX, minAY, differenceSP, maxSP, meanSP, varSP, t]

    def saveResult(self, start, end, result):
        oldwd = open_workbook('ForLDA.xls', formatting_info=True)
        sheet = oldwd.sheet_by_index(0)
        rowNum = sheet.nrows
        newwb = copy(oldwd)
        newWs = newwb.get_sheet(0)
        self.write_data([start, end, result], newWs, rowNum)
        newwb.save('ForLDA.xls')

    def write_data(self, dataTemp, table, row):
        # data = np.array(dataTemp)
        l = len(dataTemp)  # l is the number of column
        for j in range(l):
            table.write(row, j, dataTemp[j])

    def stop(self):
        self.__running.clear()


# this thread for time-window monitor and LDA detection
class Thread_for_lda(threading.Thread):  # threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()
        self.score_queue = []
        self.type = 0

    # set driver type
    def setType(self, type=0):
        self.type = type

    # main function in the thread
    def run(self):
        global svm_label_buffer
        global trip_svm_buffer
        global time_window_score
        global trip_score
        global GUI_flag
        ldaforevent = LDAForEvent
        ldaforevent.LDALoad(ldaforevent)
        start_time = time.time()
        #  monitor time-window
        time.sleep(time_window)
        while True:
            if time.time() - start_time > time_window and LDA_flag:
                GUI_flag = True
                start_time = time.time()
                temp_word = svm_label_buffer
                trip_svm_buffer += temp_word
                svm_label_buffer = ""
                if temp_word != "":
                    result_time_window = ldaforevent.LDATest(ldaforevent, [temp_word])
                    result_trip = ldaforevent.LDATest(ldaforevent, [trip_svm_buffer])
                    print(result_trip)
                    trip_score = self.result_to_score(result_trip)
                    # self.renew_trip_score(self,ldaforevent)
                    self.score_queue.append(self.result_to_score(result_time_window))
                elif temp_word == "":
                    self.score_queue.append(100)

                if len(self.score_queue) > 6:
                    self.score_queue.pop()

                time_window_score = self.calc_window_socre()

    # change trip score
    def renew_trip_score(self, ldaforevent):
        global trip_score
        result_trip = ldaforevent.LDATest(ldaforevent, [trip_svm_buffer])
        trip_score = self.result_to_score(self, result_trip)

    # calculate window score using LDA
    def calc_window_socre(self):
        weight = []
        temp_sum = 0
        if 0 == self.type:
            return np.average(self.score_queue)
        if 1 == self.type:
            weight = [0.1568819267, 0.1608039749, 0.1647235717, 0.1686358209, 0.1725358535, 0.1764188523]
        elif 2 == self.type:
            weight = [0.1041067243, 0.1238870019, 0.147190147, 0.1745471447, 0.2065300858, 0.2437388963]
        elif 3 == self.type:
            weight = [0.06684435423, 0.09224520883, 0.1265973246, 0.1724409706, 0.2325203058, 0.309351836]
        elif 4 == self.type:
            weight = [0.02485508984, 0.04823130184, 0.09134744503, 0.1651632657, 0.2743477661, 0.3960551315]
        for i in range(len(weight)):
            temp_sum += weight[i] * self.score_queue[i]
        return temp_sum

    # get a score by LDA topics
    def result_to_score(self, result):
        score = 0
        for node in result:
            score += (node[0] + 1) * 25 * node[1]
        return score

    def stop(self):
        self.__running.clear()


thresholdnum = 0
bthresholdnum = 0
sevent = Event(0, -1)
bevent = Event(0, -1)
sfault = 0  # number of noise that speedup can bear
bfault = 0


#  detect event from acceleration x
def detectEvent(data):
    global thresholdnum
    global bthresholdnum
    global sevent
    global bevent
    global sfault
    global bfault
    global SVM_flag
    global LDA_flag
    sflag = False
    bflag = False
    xarray = []
    stdXArray = []  # use to get the smallest std, which will be the beginning of an event
    faultNum = int(2 * samplingRate / 5)
    minLength = int(samplingRate)

    xstdQueue.put(data)

    if xstdQueue.full():
        t = []  # transform the queue to array
        for i in range(xstdQueue.qsize()):
            temp = xstdQueue.get()
            t.append(temp[3])
            if i > std_window - 2:
                stdXArray.append(np.std(t[i - std_window + 1:i], ddof=1))
                xarray.append(temp)
                # x.append(temp[3])
            xstdQueue.put(temp)
        xstdQueue.get()

        stdX = stdXArray[-1]
        startIndex = stdXArray.index(max(stdXArray))

        accx = data[3]
        timestamp = data[0]

        if accx > 0.1 and max(stdXArray) > 0.02 and thresholdnum == 0:
            thresholdnum = thresholdnum + 1
            sevent = Event(xarray[startIndex][0], 0)
            for i in range(startIndex, len(xarray)):  # add the previous data to event
                sevent.addValue(xarray[i])
            sflag = True
            SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
            LDA_flag = False
            print("catch acceleration")
        elif accx > 0.05 and thresholdnum > 0:
            thresholdnum = thresholdnum + 1
            sfault = faultNum
            sflag = True
        elif accx <= 0.05 and sfault > 0 and thresholdnum > 0:
            sfault = sfault - 1
            thresholdnum = thresholdnum + 1
            sflag = True
        elif (accx <= 0.05 or stdX < 0.01) and thresholdnum > 0:
            if thresholdnum > minLength:
                sevent.setEndtime(timestamp)
                sfault = faultNum
                thresholdnum = 0
                sevent.addValue(data)
                return sevent
            else:
                thresholdnum = 0
                sfault = faultNum
                SVM_flag = SVM_flag - 1
                LDA_flag = True
                print("dismis the speedup")
        elif thresholdnum > 0:
            thresholdnum = thresholdnum + 1
            sflag = True

        if accx < -0.12 and max(stdXArray) > 0.02 and bthresholdnum == 0:
            bthresholdnum = bthresholdnum + 1
            bevent = Event(xarray[startIndex][0], 1)
            for i in range(startIndex, len(xarray)):  # add the previous data to event
                bevent.addValue(xarray[i])
            bflag = True
            SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
            LDA_flag = False
            print("catch a break")
        elif accx < -0.06 and bthresholdnum > 0:
            bthresholdnum = bthresholdnum + 1
            bfault = faultNum
            bflag = True
        elif accx >= -0.06 and bfault > 0 and bthresholdnum > 0:
            bfault = bfault - 1
            bthresholdnum = bthresholdnum + 1
            bflag = True
        elif (accx >= -0.06 or stdX < 0.01) and bthresholdnum > 0:
            if bthresholdnum > minLength:
                bevent.setEndtime(timestamp)
                bfault = faultNum
                bthresholdnum = 0
                bevent.addValue(data)
                return bevent
            else:
                bfault = faultNum
                bthresholdnum = 0
                SVM_flag = SVM_flag - 1
                LDA_flag = True
                print("dimiss the break")
        elif bthresholdnum > 0:
            bthresholdnum = bthresholdnum + 1
            bflag = True

    if sflag:
        sevent.addValue(data)
    if bflag:
        bevent.addValue(data)


tthresholdnum = 0
tevent = Event(0, -1)
tfault = 3
swerveFlag = False
positive = True
negative = True


# detect event from acceleration y
def detectYEvent(data):
    global tthresholdnum
    global tevent
    global tfault
    global positive
    global negative
    global SVM_flag
    global LDA_flag
    yarray = []
    stdYArray = []  # use to get the smallest std, which will be the beginning of an event
    tflag = False
    minLength = int(samplingRate * 1.2)
    maxLength = int(samplingRate * 14)
    faultNum = int(5 * samplingRate / 10)
    ystdQueue.put(data)

    if ystdQueue.full():
        t = []  # transform the queue to array
        for i in range(ystdQueue.qsize()):
            temp = ystdQueue.get()
            t.append(temp[2])
            if i > std_window - 2:  # calculate the standard deviation from list
                stdYArray.append(np.std(t[i - std_window + 1:i], ddof=1))
                yarray.append(temp)
            # y.append(temp[2])
            ystdQueue.put(temp)
        ystdQueue.get()
        stdY = stdYArray[-1]

        startIndex = stdYArray.index(max(stdYArray))

        accy = data[2]
        timestamp = data[0]

        if positive:
            if accy > 0.15 and max(stdYArray) > 0.015 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum + 1
                tevent = Event(yarray[startIndex][0], 2)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                negative = False
                SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
                LDA_flag = False
                print("catch turn")
            elif accy > 0.06 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = faultNum
                tflag = True
            elif accy <= 0.06 and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy <= 0.06 or stdY < 0.015) and tthresholdnum > 0:
                if minLength < tthresholdnum < maxLength:
                    tevent.setEndtime(timestamp)
                    tfault = faultNum
                    tthresholdnum = 0
                    negative = True
                    tevent.addValue(data)
                    return tevent
                else:
                    tfault = faultNum
                    tthresholdnum = 0
                    negative = True
                    SVM_flag = SVM_flag - 1
                    LDA_flag = True
                    print("dismiss the turn")
            elif tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tflag = True

        if negative:
            if accy < -0.15 and max(stdYArray) > 0.015 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum + 1
                tevent = Event(yarray[startIndex][0], 3)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                positive = False

                SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
                LDA_flag = False
                print("catch the turn")
            elif accy < -0.06 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = faultNum
                tflag = True
            elif accy >= -0.06 and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy >= -0.06 or stdY < 0.03) and tthresholdnum > 0:
                if minLength < tthresholdnum < maxLength:
                    tevent.setEndtime(timestamp)
                    tfault = faultNum
                    tthresholdnum = 0
                    positive = True
                    tevent.addValue(data)
                    return tevent
                else:
                    tfault = faultNum
                    tthresholdnum = 0
                    positive = True
                    SVM_flag = SVM_flag - 1
                    LDA_flag = True
                    print("dismiss the turn")
            elif tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tflag = True

    if tflag:
        tevent.addValue(data)


def splitByte(obdData):
    row = obdData.split(b"\r")[0]
    row = row.split(b",")
    newrow = []
    if row != b"":
        if 9 > len(row) > 7:
            newrow.append(str(row[0], encoding="utf-8"))
            newrow.append(int(str(row[1], encoding="utf-8")))
            newrow.append(float(str(row[2], encoding="utf-8")))
            newrow.append(float(str(row[3], encoding="utf-8")))
            newrow.append(float(str(row[4], encoding="utf-8")))
            newrow.append(float(str(row[5], encoding="utf-8")))
            newrow.append(float(str(row[6], encoding="utf-8")))
            newrow.append(float(str(row[7], encoding="utf-8")))
        else:
            newrow = ""
    else:
        newrow = ""

    return newrow


def main():
    # initialize the sampling rate of the data reading
    global samplingRate
    global xstdQueue
    global ystdQueue
    global std_window
    global SVMResultQueue
    global GUI_flag

    BTserial = getSerial()
    countDown = 15
    obddata = ''
    obddata = obddata.encode('utf-8')
    timestamp = []
    while countDown > 0:
        row = obddata + BTserial.readline()
        row = splitByte(row)
        if row != "":
            timestamp.append(int(round(time.time()*1000)))
            countDown = countDown - 1
    # calculate the sampling rate of the car
    samplingRate = 14 / ((timestamp[-1] - timestamp[0]) / 1000)
    std_window = int(samplingRate + 0.5)
    xstdQueue = queue.Queue(maxsize=(2 * std_window - 1))
    ystdQueue = queue.Queue(maxsize=(2 * std_window - 1))

    print('samplingrate--' + str(samplingRate))
    print('std_window:', str(std_window))

    # start the data collection and event detection thread
    process1 = detectProcess()
    process1.start()

    # start the thread for SVM
    thread2 = SVMthread()
    thread2.start()

    # # save data into data base thread
    # data_thread = DataThread()
    # data_thread.start()

    # start lda thread
    lda_thread = Thread_for_lda()
    lda_thread.start()

    Panel = GUI.Panel()
    Panel.drawPanel()
    while True:
        Panel.refresh()
        if GUI_flag:
            GUI_flag = False
            Panel.change_score(time_window_score, trip_score)
        if not SVMResultQueue.empty():
            result = SVMResultQueue.get()
            time_local = time.localtime(float(result.getStart() / 1000))
            start = time.strftime("%H:%M:%S", time_local)
            time_local = time.localtime(float(result.getEnd() / 1000))
            end = time.strftime("%H:%M:%S", time_local)
            Panel.showEvent(start, end, result.getLabel())



if __name__ == "__main__":
    # main()
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.map(main())
    eventQueue = multiprocessing.Queue()
    dataQueue = multiprocessing.Queue()
    main()
