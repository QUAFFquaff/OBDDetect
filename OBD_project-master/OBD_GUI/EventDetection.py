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
from graphics import *
import threading
import time
from dataHandler.LDAForEvent import *

matrix = np.array([[0.0649579822346719, 0, -0.997888],
                   [-0.140818558599268, 0.989992982850364, -0.00916664939131784],
                   [0.987902117670584, 0.141116596851819, 0.0643079465924438]])

time_window = 40 # time window for a word in LDA
svm_label_buffer = "" # the word in a time window
LDA_flag = True # if False, there are a event holding a time window, we should waiting for the end of event

timestamp = []
speed = []
gyox = []
gyoy = []
gyoz = []
gpsLa = []
gpsLo = []
accelerationx = 0
accelerationy = 0
accelerationz = 0

#lock = threading.Lock()
eventQueue = queue.Queue()


def connectDB():
    connection = pymysql.connect(host='35.197.95.95',
                                 user='root',
                                 password='obd12345',
                                 db='DRIVINGDB',
                                 port=3306,
                                 charset='utf8')
    return connection


class Event(object):
    def __init__(self, starttime, type):
        self.start = starttime
        self.type = type
        self.vect = []

    def setEndtime(self, endtime):
        self.end = endtime

    def getDuration(self):
        duration = (self.end - self.start) / 5
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


# thread class to write
class myThread(threading.Thread):  # threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        newrecord = 0

        global timestamp
        global speed
        accx = []
        accy = []
        accz = []
        global gyox
        global gyoy
        global gyoz
        global gpsLa
        global gpsLo
        global accelerationx
        global accelerationy
        global accelerationz
        global eventQueue

        while (True):
            isCatch = False
            lowpass = []
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
                            accx.append(row[4])
                            accy.append(row[5])
                            accz.append(row[6])
                            gpsLa.append(row[7])
                            gpsLo.append(row[8])
                            gyox.append(row[9])
                            gyoy.append(row[10])
                            gyoz.append(row[11])
                            acc = np.array([accx, accy, accz])
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
                # gpsTxt.setText('GPS:(' + gpsLa[-2] + ',' + gpsLo[-1] + ')')
                # low pass filter
                lowpass = np.array(lowpass)
                b, a = signal.butter(3, 0.4, 'low')
                accxsf = signal.filtfilt(b, a, lowpass[:, 1])
                accysf = signal.filtfilt(b, a, lowpass[:, 0])
                acczsf = signal.filtfilt(b, a, lowpass[:, 2])
                # print(accxsf, accysf,acczsf)
                # if(x>=30):
                # lowpassed.append([accysf[-2],accxsf[-2],acczsf[-2]])

                # detect event
                event = detectEvent(
                    [timestamp[-2], speed[-2], accysf[-2], accxsf[-2], acczsf[-2], gyox[-2], gyoy[-2], gyoz[-2]])
                yevent = detectYEvent(
                    [timestamp[-2], speed[-2], accysf[-2], accxsf[-2], acczsf[-2], gyox[-2], gyoy[-2], gyoz[-2]])

                # put the event into Queue
                if not event is None:
                    eventQueue.put(event)
                if not yevent is None:
                    eventQueue.put(yevent)

    def stop(self):
        self.__running.clear()
# this thread for time-window monitor and LDA detection
class thread_for_lda(threading.Thread):  # threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()
        self.score_queue = []

    def run(self):
        global svm_label_buffer
        ldaforevent = LDAForEvent
        start_time = time.time()
        #  monitor time-window
        while True:
            if time.time()-start_time > time_window and LDA_flag:
                start_time = time.time()
                temp_word = svm_label_buffer
                svm_label_buffer = ""
                if svm_label_buffer != "":
                    result = ldaforevent.LDATest(ldaforevent, [temp_word])
                    self.score_queue.append(self.result_to_score(self,result))
                    if len(self.score_queue) > 5:
                        self.score_queue.pop()


    def calc_score(self,type):
        if 1 == type:
            return np.average(self.score_queue)
        if 2 == type:
            return 1
        return 0


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
sfault = 3
bfault = 3


#  detect event from acceleration x
def detectEvent(data):
    global thresholdnum
    global bthresholdnum
    global sevent
    global bevent
    global sfault
    global bfault
    sflag = False
    bflag = False
    xarray = []
    # x = []
    stdXArray = []  # use to get the smallest std, which will be the beginning of an event
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
        elif accx > 0.05 and thresholdnum > 0:
            thresholdnum = thresholdnum + 1
            sfault = 3
            sflag = True
        elif accx < 0.05 and sfault > 0 and thresholdnum > 0:
            sfault = sfault - 1
            thresholdnum = thresholdnum + 1
            sflag = True
        elif (accx < 0.05 or stdX < 0.02) and thresholdnum > 0:
            if thresholdnum > 10:
                sevent.setEndtime(timestamp)
                sfault = 3
                thresholdnum = 0
                return sevent
            thresholdnum = 0
            sfault = 3

        if accx < -0.10 and stdX > 0.02 and bthresholdnum == 0:
            bthresholdnum = bthresholdnum + 1
            bevent = Event(xarray[startIndex][0], 2)
            for i in range(startIndex, len(xarray)):  # add the previous data to event
                bevent.addValue(xarray[i])
            bflag = True
        elif accx < -0.05 and bthresholdnum > 0:
            bthresholdnum = bthresholdnum + 1
            bfault = 3
            bflag = True
        elif accx > -0.05 and bfault > 0 and bthresholdnum > 0:
            bfault = bfault - 1
            bthresholdnum = bthresholdnum + 1
            bflag = True
        elif (accx > -0.05 or stdX < 0.02) and bthresholdnum > 0:
            if bthresholdnum > 10:
                bevent.setEndtime(timestamp)
                bfault = 3
                bthresholdnum = 0
                return bevent
            bfault = 3
            bthresholdnum = 0

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
    yarray = []
    stdYArray = []  # use to get the smallest std, which will be the beginning of an event
    # y = []
    tflag = False
    ystdQueue.put(data)

    if ystdQueue.full():
        t = []  # transform the queue to array
        for i in range(ystdQueue.qsize()):
            temp = ystdQueue.get()
            t.append(temp[2])
            if i > 8:
                stdYArray.append(np.std(t[i - 9:i]), ddof=1)
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
                tevent = Event(yarray[startIndex][0], 4)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                negative = False
            elif accy > 0.05 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = 3
                tflag = True
            elif (accy < 0.05 or stdY < 0.03) and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy < 0.05 or stdY < 0.03) and tthresholdnum > 0:
                if tthresholdnum > 15 and not swerveFlag:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    negative = True
                    return tevent
                elif stdY > 0.1:
                    tthresholdnum = tthresholdnum + 1
                    tflag = True
                elif tthresholdnum > 15:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    negative = True
                    return tevent
                else:
                    tflag = 3
                    tthresholdnum = 0
                    negative = True

        if negative:
            if accy < -0.1 and stdY > 0.03 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum + 1
                tevent = Event(yarray[startIndex][0], 4)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                positive = False
            elif accy < -0.05 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = 3
                tflag = True
            elif (accy > -0.05 or stdY < 0.03) and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy > -0.05 or stdY < 0.03) and tthresholdnum > 0:
                if tthresholdnum > 15 and not swerveFlag:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    positive = True
                    return tevent
                elif stdY > 0.1:
                    tthresholdnum = tthresholdnum + 1
                    tflag = True
                elif tthresholdnum > 15:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    positive = True
                    return tevent
                else:
                    tflag = 3
                    tthresholdnum = 0
                    negative = True

    if tflag:
        tevent.addValue(data)


def calcData(data):
    maxAX = max(data[:, 3])
    maxAY = max(data[:, 2])
    minAX = min(data[:, 3])
    minAY = min(data[:, 2])
    rangeAX = maxAX - minAX
    rangeAY = maxAY - minAY
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
    return [rangeAX, rangeAY, varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY, maxOX,
            maxOY, minAY, meanSP, varSP, t]


def nomalization(vect):
    max = [0.619, 0.944, 0.208, 0.281, 6.075, 17.258, 0.286, 0.349, 3.901, 26.569, 10.171, 60.271, 0.097, 106.5, 29.291,
           24.982]
    min = [0.034, 0.021, 0.009, 0.004, 0.325, 0.845, -0.312, -0.281, -3.816, -20.210, -0.061, -1.291, -0.818, 4.979,
           0.408, 1.581]
    for i in range(len(vect)):
        vect[i] = (vect[i] - min[i]) / (max[i] - min[i])
    return vect


def transformTimestamp(timestamp):
    timestamp = float(int(timestamp) / 1000)
    time_local = time.localtime(timestamp)
    dt = time.strftime(" %H:%M:%S", time_local)
    return dt


def drawBackground():
    backgroudcolor = color_rgb(33, 33, 33)
    # === creating the graphic window ===
    win = GraphWin("event detection", 500, 300)
    win.setCoords(0, 0, 25, 15)

    # === set the background color ===
    Ground = Rectangle(Point(0, 0), Point(25, 15))
    Ground.setFill("light Green")
    Ground.draw(win)

    return win

def saveResult(start, end, result):
    oldwd = open_workbook('ForLDA.xls', formatting_info=True)
    sheet = oldwd.sheet_by_index(0)
    rowNum = sheet.nrows
    newwb = copy(oldwd)
    newWs = newwb.get_sheet(0)
    write_data(np.array([start, end, result]), newWs, rowNum)
    newwb.save('ForLDA.xls')

def main():
    svm = joblib.load('svm.pkl')
    resultMatrix = []
    eventNum = 0

    # start the data collection and event detection thread
    thread1 = myThread()
    thread1.start()

    # draw the background
    win = drawBackground()
    pntMsg = Point(12, 6)
    txtMsg = Text(pntMsg, "Event")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("blue")
    txtMsg.setSize(15)
    txtMsg.draw(win)

    gpsTxt = Text(Point(12, 12), "GPS")
    gpsTxt.setTextColor("blue")
    gpsTxt.setSize(15)
    gpsTxt.draw(win)

    while True:
        #  define type and intensity
        if not eventQueue.empty():
            event = eventQueue.get()

            print(event.getType(), ' event: ', event.getStart(), '-', event.getEnd())

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
                eventNum = eventNum + 1
                resultMatrix.append([event.getStart(), event.getEnd(), result[0]])

                txtMsg.undraw()
                if result == 0:
                    txtMsg.setText(transformTimestamp(event.getStart()) + '--' + transformTimestamp(
                        event.getEnd()) + ' speed up')
                elif result == 1:
                    txtMsg.setText(transformTimestamp(event.getStart()) + '--' + transformTimestamp(
                        event.getEnd()) + 'hard speed up')
                elif result == 2:
                    txtMsg.setText(
                        transformTimestamp(event.getStart()) + '--' + transformTimestamp(event.getEnd()) + ' brake')
                elif result == 3:
                    txtMsg.setText(transformTimestamp(event.getStart()) + '--' + transformTimestamp(
                        event.getEnd()) + ' hrad brake')
                txtMsg.draw(win)

                saveResult(event.getStart(), event.getEnd(), result[0])



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
