import numpy as np
import queue
import pymysql
import pymysql.cursors
from xlwt import *
from xlrd import *
from xlutils.copy import copy
from sklearn import svm
from sklearn.externals import joblib
from scipy import signal
from OBD_GUI.graphics import *
import threading
import time
from dataHandler.LDAForEvent import *
from OBD_GUI import GUI

matrix = np.array([[0.0649579822346719, 0, -0.997888],
                   [-0.140818558599268, 0.989992982850364, -0.00916664939131784],
                   [0.987902117670584, 0.141116596851819, 0.0643079465924438]])

samplingRate = 0  # the sampling rate of the data reading
std_window = 0  # the time window for standard deviation

time_window = 40  # time window for a word in LDA
svm_label_buffer = ""  # the word in a time window
LDA_flag = True  # if False, there are a event holding a time window, we should waiting for the end of event

timestamp = []
speed = []
gpsLa = None
gpsLo = None

#lock = threading.Lock()
eventQueue = queue.Queue()
SVMResultQueue = queue.Queue()
SVM_flag = 0  # if bigger than 0, there are overlapped events in queue
overlapNum = 0  # the number of overlapped events


def connectDB():
    connection = pymysql.connect(host='35.197.95.95',
                                 user='root',
                                 password='obd12345',
                                 db='DRIVINGDB',
                                 port=3306,
                                 charset='utf8')
    return connection

# to get the result label from SVM
class SVMResult(object):
    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.getEnd()
    def getLabel(self):
        return self.label

#record the events detected
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



class detectThread(threading.Thread):  # threading.Thread

    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        newrecord = 0

        global timestamp
        global speed
        global gpsLa
        global gpsLo
        global samplingRate
        global eventQueue
        global overlapNum

        while (True):
            isCatch = False
            lowpass = []
            timestamp = []
            speed = []
            accx = []
            accy = []
            accz = []
            gyox = []
            gyoy = []
            gyoz = []
            try:
                # 获取一个游标
                connection = connectDB()
                with connection.cursor() as cursor:
                    sql = 'select * from STATUS ORDER BY time DESC LIMIT 30'
                    count = cursor.execute(sql)

                    i = 0
                    for row in cursor.fetchall():
                        if i == 0:
                            if row[2] != newrecord:  # detect if catch the same data
                                isCatch = True
                                newrecord = row[2]
                        if isCatch:
                            timestamp.append(row[2])
                            speed.append(row[3])
                            accy.append(row[4])
                            accx.append(row[5])
                            accz.append(row[6])
                            gpsLa = row[7]
                            gpsLo = row[8]
                            gyox.append(row[9])
                            gyoy.append(row[10])
                            gyoz.append(row[11])
                            acc = np.array([row[4], row[5], row[6]])
                            acc = acc.astype(np.float64)

                            # calibration
                            acc = np.dot(matrix, acc)
                            accelerationx = acc[1]
                            accelerationy = acc[0]
                            accelerationz = acc[2]
                            # put data into lowpass list which is used to filtered
                            lowpass.append(acc)
                        i = i + 1
            finally:
                connection.close()
            if isCatch:
                cutoff = 2*(1/samplingRate)  # cutoff frequency of low pass filter

                # low pass filter
                lowpass = np.array(lowpass)
                b, a = signal.butter(3, cutoff, 'low')
                accxsf = signal.filtfilt(b, a, lowpass[:, 1])
                accysf = signal.filtfilt(b, a, lowpass[:, 0])
                acczsf = signal.filtfilt(b, a, lowpass[:, 2])

                # detect event
                event = detectEvent(
                    [timestamp[-2], speed[-2], accysf[-2], accxsf[-2], acczsf[-2], gyox[-2], gyoy[-2], gyoz[-2]])
                yevent = detectYEvent(
                    [timestamp[-2], speed[-2], accysf[-2], accxsf[-2], acczsf[-2], gyox[-2], gyoy[-2], gyoz[-2]])

                # put the event into Queue
                if not event is None:
                    if SVM_flag > 0:
                        overlapNum = overlapNum + 1
                    eventQueue.put(event)
                if not yevent is None:
                    data = yevent.getValue()
                    max_gyo = max(max(data[:, 5:6]), abs(min(data[:, 5:6])))
                    if max_gyo < 15:
                        yevent.setType(yevent.getType()+2)
                    if SVM_flag > 0:
                        overlapNum = overlapNum + 1
                    eventQueue.put(yevent)

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

        while True:
            #  define type and intensity
            if (not eventQueue.empty()) and SVM_flag == 0:
                eventNum = overlapNum
                overlapNum = 0
                eventList = []
                for i in range(0, eventNum):
                    eventList.append(eventQueue.get())
                eventList = self.makeDecision(eventList)

                for i in range(0, eventNum):
<<<<<<< HEAD
                    if eventList[i]:
                        pass
                #print(event.getType(), ' event: ', event.getStart(), '-', event.getEnd())

                vect = np.array(event.getValue())
                # print(vect)
                vect = vect.astype(np.float64)

                # calculate the features
                vect = calcData(vect)
                # normalize the features
                vect = nomalization(vect)

                # predict the result
                result = svm.predict([vect])
                print(result)
                if result < 4:
                    resultMatrix.append([event.getStart(), event.getEnd(), result[0]])

                    saveResult(event.getStart(), event.getEnd(), result[0])
=======
                    if eventList[i]!=None:
                        vect = np.array(eventList[i].getValue())
                        vect = vect.astype(np.float64)

                        # calculate the 23 features
                        vect = calcData(vect)
                        # nomaliz the 23 features
                        vect = nomalization(vect)

                        # predict the result
                        result = svm.predict([vect])  # result of SVM
                        score = svm.decision_function([vect])  # score of SVM for each tyeps
                        score = np.array(score[0])
                        print(result)

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
                        SVMResultQueue.put(SVMResult(eventList[i].getStart(),eventList[i].getEnd(),result[0]))
                        saveResult(eventList[i].getStart(),eventList[i].getEnd(), result[0])
>>>>>>> 7713d6fdb01fd71c4e9fcc0798b78fa40be0367c

    def makeDecision(self, eventList):
        for i in range(0, len(eventList)-2):
            if eventList[i]:
                factor1 = (eventList[i].getEnd() - eventList[i+1].getStart())/ eventList[i].getDuration()
                factor2 = (eventList[i+1].getEnd() - eventList[i].getEnd()) / eventList[i+1].getDuration()
                if factor1>0.5 and factor2<0.5:
                    if eventList[i].getType() > 2 >= eventList[i+1].getType():
                        eventList[i+1] = None
                    elif eventList[i].getType() <= 2 < eventList[i+1].getType():
                        eventList[i] = None
        return eventList

    def stop(self):
            self.__running.clear()


# this thread for time-window monitor and LDA detection
class thread_for_lda(threading.Thread):  # threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()
        self.score_queue = []
        self.type = 0

    def setType(self,type):
        self.type = type

    def run(self):
        global svm_label_buffer
        ldaforevent = LDAForEvent
        start_time = time.time()
        #  monitor time-window
        time.sleep(time_window)
        while True:
            if time.time()-start_time > time_window and LDA_flag:
                start_time = time.time()
                temp_word = svm_label_buffer
                svm_label_buffer = ""
                if temp_word != "":
                    result = ldaforevent.LDATest(ldaforevent, [temp_word])
                    self.score_queue.append(self.result_to_score(self,result))
                elif temp_word == "":
                    self.score_queue.append(100)

                if len(self.score_queue) > 6:
                    self.score_queue.pop()
                    self.trigger_feedback()


    def trigger_feedback(self):
        weight = []
        temp_sum = 0
        if 0 == self.type:
            return np.average(self.score_queue)
        if 1 == self.type:
            weight = [0.1568819267,0.1608039749,0.1647235717,0.1686358209,0.1725358535,0.1764188523]
        elif 2 == self.type:
            weight = [0.1041067243,0.1238870019,0.147190147,0.1745471447,0.2065300858,0.2437388963]
        elif 3 == self.type:
            weight = [0.06684435423,0.09224520883,0.1265973246,0.1724409706,0.2325203058,0.309351836]
        elif 4 == self.type:
            weight = [0.02485508984,0.04823130184,0.09134744503,0.1651632657,0.2743477661,0.3960551315]
        for i in range(len(weight)):
            temp_sum += weight[i]*self.score_queue[i]
        return temp_sum


    def result_to_score(self,result):
        score = 0
        for node in result:
            score += (node[0]+1) * 25 * node[1]
        return score

    def stop(self):
        self.__running.clear()


def write_data(dataTemp, table, row):
    data = np.array(dataTemp)
    l = len(data)  # l is the number of column
    for j in range(l):
        table.write(row, j, data[j])


xstdQueue = queue.Queue(maxsize=19)
ystdQueue = queue.Queue(maxsize=19)

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
    sflag = False
    bflag = False
    xarray = []
    # x = []
    stdXArray = []  # use to get the smallest std, which will be the beginning of an event
    minLength = int(samplingRate*1.5)  # the minimum length that the event should be
    faultNum = int(2*samplingRate/5)
    xstdQueue.put(data)

    if xstdQueue.full():
        t = []  # transform the queue to array
        for i in range(xstdQueue.qsize()):
            temp = xstdQueue.get()
            t.append(temp[3])
            if i > 8:
                stdXArray.append(np.std(t[i - 9:i]), ddof=1)
                xarray.append(temp)
                # x.append(temp[3])
            xstdQueue.put(temp)
        xstdQueue.get()
        stdX = np.std(xarray[:, 3], ddof=1)

        startIndex = stdXArray.index(min(stdXArray))

        accx = data[3]
        timestamp = data[0]

        if accx > 0.1 and stdX > 0.02 and thresholdnum == 0:
            thresholdnum = thresholdnum + 1
            sevent = Event(xarray[startIndex][0], 0)
            for i in range(startIndex, len(xarray)):  # add the previous data to event
                sevent.addValue(xarray[i])
            sflag = True
            SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
        elif accx > 0.05 and thresholdnum > 0:
            thresholdnum = thresholdnum + 1
            sfault = faultNum
            sflag = True
        elif accx < 0.05 and sfault > 0 and thresholdnum > 0:
            sfault = sfault - 1
            thresholdnum = thresholdnum + 1
            sflag = True
        elif (accx < 0.05 or stdX < 0.02) and thresholdnum > 0:
            SVM_flag = SVM_flag - 1
            if thresholdnum > minLength:
                sevent.setEndtime(timestamp)
                sfault = faultNum
                thresholdnum = 0
                return sevent
            thresholdnum = 0
            sfault = faultNum
        else:
            thresholdnum = thresholdnum + 1
            sflag = True


        if accx < -0.10 and stdX > 0.02 and bthresholdnum == 0:
            bthresholdnum = bthresholdnum + 1
            bevent = Event(xarray[startIndex][0], 1)
            for i in range(startIndex, len(xarray)):  # add the previous data to event
                bevent.addValue(xarray[i])
            bflag = True
            SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
        elif accx < -0.05 and bthresholdnum > 0:
            bthresholdnum = bthresholdnum + 1
            bfault = faultNum
            bflag = True
        elif accx > -0.05 and bfault > 0 and bthresholdnum > 0:
            bfault = bfault - 1
            bthresholdnum = bthresholdnum + 1
            bflag = True
        elif (accx > -0.05 or stdX < 0.02) and bthresholdnum > 0:
            SVM_flag = SVM_flag - 1
            if bthresholdnum > minLength:
                bevent.setEndtime(timestamp)
                bfault = faultNum
                bthresholdnum = 0
                return bevent
            bfault = faultNum
            bthresholdnum = 0
        else:
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
    global swerveFlag
    global positive
    global negative
    global SVM_flag
    yarray = []
    stdYArray = []  # use to get the smallest std, which will be the beginning of an event
    # y = []
    tflag = False
    minLength = int(samplingRate*1.5)
    maxLength = int(samplingRate*9.6)
    faultNum = int(8*samplingRate/15)
    ystdQueue.put(data)

    if ystdQueue.full():
        t = []  # transform the queue to array
        for i in range(ystdQueue.qsize()):
            temp = ystdQueue.get()
            t.append(temp[2])
            if i > std_window-2:  # calculate the standard deviation from list
                stdYArray.append(np.std(t[i - std_window+1:i]), ddof=1)
                yarray.append(temp)
            # y.append(temp[2])
            ystdQueue.put(temp)
        ystdQueue.get()
        stdY = np.std(yarray[:, 2], ddof=1)

        startIndex = stdYArray.index(min(stdYArray))

        accy = data[2]
        timestamp = data[0]

        if positive:
            if accy > 0.1 and stdY > 0.03 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum + 1
                tevent = Event(yarray[startIndex][0], 2)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                negative = False
                SVM_flag = SVM_flag + 1 # set the flag to denote the event starts
            elif accy > 0.05 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = faultNum
                tflag = True
            elif (accy < 0.05 or stdY < 0.03) and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy < 0.05 or stdY < 0.03) and tthresholdnum > 0:
                SVM_flag = SVM_flag - 1
                if minLength < tthresholdnum < maxLength:
                    tevent.setEndtime(timestamp)
                    tfault = faultNum
                    tthresholdnum = 0
                    negative = True
                    return tevent
                else:
                    tfault = faultNum
                    tthresholdnum = 0
                    negative = True
            else:
                tthresholdnum = tthresholdnum + 1
                tflag = True

        if negative:
            if accy < -0.1 and stdY > 0.03 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum + 1
                tevent = Event(yarray[startIndex][0], 3)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                positive = False
                SVM_flag = SVM_flag + 1 # set the flag to denote the event starts
            elif accy < -0.05 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = faultNum
                tflag = True
            elif (accy > -0.05 or stdY < 0.03) and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy > -0.05 or stdY < 0.03) and tthresholdnum > 0:
                SVM_flag = SVM_flag - 1
                if minLength < tthresholdnum < maxLength:
                    tevent.setEndtime(timestamp)
                    tfault = faultNum
                    tthresholdnum = 0
                    positive = True
                    return tevent
                else:
                    tfault = faultNum
                    tthresholdnum = 0
                    negative = True
            else:
                tthresholdnum = tthresholdnum + 1
                tflag = True

    if tflag:
        tevent.addValue(data)


def calcData(data):
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


def nomalization(vect):
    max = [0.619, 0.944, 0.546, 0.418, 0.208, 0.281, 6.075, 17.258, 0.286, 0.349, 3.901, 26.569, 22.12, 60.271, 0.594, 0.932, 0.097, 0.191, 90, 136,
           122.637, 29.291, 24.982]
    min = [0.034, 0.021, -0.302, -0.249, 0.009, 0.004, 0.325, 0.575, -0.312, -0.281, -3.816, -20.210, -0.061, -1.291, -0.063, -0.067, -0.539,  -0.818, -76, 5,
           4.979, 0.408, 1.581]
    for i in range(len(vect)):
        vect[i] = (vect[i] - min[i]) / (max[i] - min[i])
    return vect


def transformTimestamp(timestamp):
    timestamp = float(int(timestamp) / 1000)
    time_local = time.localtime(timestamp)
    dt = time.strftime(" %H:%M:%S", time_local)
    return dt



def saveResult(start, end, result):
    oldwd = open_workbook('ForLDA.xls', formatting_info=True)
    sheet = oldwd.sheet_by_index(0)
    rowNum = sheet.nrows
    newwb = copy(oldwd)
    newWs = newwb.get_sheet(0)
    write_data(np.array([start, end, result]), newWs, rowNum)
    newwb.save('ForLDA.xls')

def main():
    # initialize the sampling rate of the data reading
    global samplingRate
    global xstdQueue
    global ystdQueue
    global sfault
    global bfault
    global tfault
    global std_window
    global SVMResultQueue

    try:
        # 获取一个游标
        connection = connectDB()
        with connection.cursor() as cursor:
            sql = 'select * from STATUS ORDER BY time DESC LIMIT 5'
            count = cursor.execute(sql)
            timestamp = []
            for row in cursor.fetchall():
                timestamp.append(row[2])
            # calculate the sampling rate of the car
            samplingRate = 4 / ((timestamp[0] - timestamp[-1]) / 1000)
            std_window = int(2*samplingRate+0.5)
            xstdQueue = queue.Queue(maxsize=(4*std_window-1))
            ystdQueue = queue.Queue(maxsize=(4*std_window-1))
    finally:
        connection.close()
    sfault = bfault = int(2*int(samplingRate+0.5)/5)
    tfault = int(8*int(samplingRate+0.5)/15)

    print(samplingRate)

    # start the data collection and event detection thread
    thread1 = detectThread()
    thread1.start()

    # start the thread for SVM
    thread2 = SVMthread()
    thread2.start()

    Panel = GUI.Panel()
    Panel.drawPanel()

    while True:
        Panel.refresh()
        if not SVMResultQueue.empty():
            result = SVMResultQueue.get()






# print('total ',eventNum,'turns')
# print(resultMatrix)
    # file_w = Workbook()
    # table = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
    # write_data(np.array(resultMatrix), table)
    # file_w.save('ForLDA.xls')

def LDATest():
    ldaforevent = LDAForEvent
    ldaforevent.LDATest(ldaforevent,[""])


if __name__ == "__main__":
    main()
