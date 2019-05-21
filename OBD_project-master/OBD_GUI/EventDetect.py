import serial
import time
import numpy as np
import queue
import GUI
import threading
from scipy import signal

matrix = np.array([[0.9988042, 0.00E+00, -0.03458038],
                   [-0.026682913, 0.63608, -0.770697297],
                   [0.021995888, 0.77162, 0.635319376]])

samplingRate = 0  # the sampling rate of the data reading
std_window = 0  # the time window for standard deviation

time_window = 5  # time window for a word in LDA
svm_label_buffer = ""  # the word in a time window
trip_svm_buffer = ""    # save the whole trip's SVm label
LDA_flag = True  # if False, there are a event holding a time window, we should waiting for the end of event
time_window_score = 50
trip_score = 50
GUI_flag = False

timestamp = 0
speed = 0
gpsLa = None
gpsLo = None

# lock = threading.Lock()
eventQueue = queue.Queue()
SVMResultQueue = queue.Queue()
SVM_flag = 0  # if bigger than 0, there are overlapped events in queue
overlapNum = 0  # the number of overlapped events

xstdQueue = queue.Queue(maxsize=19)
ystdQueue = queue.Queue(maxsize=19)

def getSerial():
    ser = serial.Serial(port='/dev/rfcomm0', baudrate=57600, timeout=0.5)
    if not ser.is_open:
        ser.open()
    return  ser

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

class SaveInDatabase(threading.Thread):
    def __init__(self):
        threading.Thred.__init__(self)
        self.__running = threading.Event()
        self.__running.set()


class detectThread(threading.Thread):  # threading.Thread

    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        newrecord = 0

        global timestamp
        global speed
        # global gpsLa
        # global gpsLo
        global samplingRate
        global eventQueue
        global overlapNum
        global SVM_flag

        lowpass = queue.Queue()
        obddata = ''
        obddata = obddata.encode('utf-8')

        lowpassCount = 0

        while True:
            row = obddata + serial.readline()
            if obddata != b'':
                row = splitByte(row)
                speed = row[3]
                accy = row[4]
                accx = row[5]
                accz = row[6]
                gyox = row[9]
                gyoy = row[10]
                gyoz = row[11]
                acc = np.array([accy,accx,accz])
                acc = acc.astype(np.float64)

                #calibration
                acc = np.dot(matrix, acc)
                lowpass.put(acc)
                if(lowpassCount>=29):
                    timestamp = int(round(time.time()*1000))

                    cutoff = 2 * (1 / samplingRate)  # cutoff frequency of low pass filter
                    # low pass filter
                    b, a = signal.butter(3, cutoff, 'low')
                    accxsf = signal.filtfilt(b, a, self.getLowPass(lowpass, 'x'))
                    accysf = signal.filtfilt(b, a, self.getLowPass(lowpass, 'y'))
                    acczsf = signal.filtfilt(b, a, self.getLowPass(lowpass, 'z'))


                    # detect event
                    event = detectEvent(
                        [timestamp[1], speed[1], accysf[1], accxsf[1], acczsf[1], gyox[1], gyoy[1], gyoz[1]])
                    yevent = detectYEvent(
                        [timestamp[1], speed[1], accysf[1], accxsf[1], acczsf[1], gyox[1], gyoy[1], gyoz[1]])

                    # put the event into Queue
                    if not event is None:

                        if SVM_flag > 0:
                            overlapNum = overlapNum + 1
                        eventQueue.put(event)
                        SVM_flag = SVM_flag - 1
                    if not yevent is None:
                        data = yevent.getValue()
                        # max_gyo = max(max(data[:, 5:6]), abs(min(data[:, 5:6])))
                        # if max_gyo < 15:
                        #     yevent.setType(yevent.getType() + 2)
                        if SVM_flag > 0:
                            overlapNum = overlapNum + 1
                        eventQueue.put(yevent)
                        SVM_flag = SVM_flag - 1

    def getLowPass(self,lowpass, opt):
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
    minLength = int(samplingRate * 1.2)  # the minimum length that the event should be
    faultNum = int(2 * samplingRate / 5)

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
        startIndex = stdXArray.index(min(stdXArray))

        accx = data[3]
        timestamp = data[0]

        if accx > 0.12 and stdX > 0.01 and thresholdnum == 0:
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
        elif accx < 0.05 and sfault > 0 and thresholdnum > 0:
            sfault = sfault - 1
            thresholdnum = thresholdnum + 1
            sflag = True
        elif (accx < 0.05 or stdX < 0.01) and thresholdnum > 0:
            if thresholdnum > minLength:
                sevent.setEndtime(timestamp)
                sfault = faultNum
                thresholdnum = 0
                return sevent
            else:
                thresholdnum = 0
                sfault = faultNum
                SVM_flag = SVM_flag - 1
                LDA_flag = True
                print("dismis the event")
        elif thresholdnum>0:
            thresholdnum = thresholdnum + 1
            sflag = True


        if accx < -0.12 and stdX > 0.012 and bthresholdnum == 0:
            bthresholdnum = bthresholdnum + 1
            bevent = Event(xarray[startIndex][0], 1)
            for i in range(startIndex, len(xarray)):  # add the previous data to event
                bevent.addValue(xarray[i])
            bflag = True
            SVM_flag += 1  # set the flag to denote the event starts
            LDA_flag = False
            print("catch a break")
        elif accx < -0.05 and bthresholdnum > 0:
            bthresholdnum = bthresholdnum + 1
            bfault = faultNum
            bflag = True
        elif accx > -0.05 and bfault > 0 and bthresholdnum > 0:
            bfault = bfault - 1
            bthresholdnum = bthresholdnum + 1
            bflag = True
        elif (accx > -0.05 or stdX < 0.012) and bthresholdnum > 0:
            if bthresholdnum > minLength:
                bevent.setEndtime(timestamp)
                bfault = faultNum
                bthresholdnum = 0
                return bevent
            else:
                bfault = faultNum
                bthresholdnum = 0
                SVM_flag = SVM_flag - 1
                LDA_flag = True
                print("dimiss the break")
        elif bthresholdnum>0:
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
    global LDA_flag
    yarray = []
    stdYArray = []  # use to get the smallest std, which will be the beginning of an event
    tflag = False
    minLength = int(samplingRate * 1.2)
    maxLength = int(samplingRate * 9.6)
    faultNum = int(8 * samplingRate / 15)
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

        startIndex = stdYArray.index(min(stdYArray))

        accy = data[2]
        timestamp = data[0]

        if positive:
            if accy > 0.15 and stdY > 0.015 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum + 1
                tevent = Event(yarray[startIndex][0], 2)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                negative = False
                SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
                print("catch turn")
            elif accy > 0.05 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = faultNum
                tflag = True
            elif (accy < 0.05 or stdY < 0.015) and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy < 0.05 or stdY < 0.015) and tthresholdnum > 0:
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
                    SVM_flag = SVM_flag - 1
                    LDA_flag = True
                    print("dismiss the turn")
            elif tthresholdnum>0:
                tthresholdnum = tthresholdnum + 1
                tflag = True

        if negative:
            if accy < -0.15 and stdY > 0.015 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum + 1
                tevent = Event(yarray[startIndex][0], 3)
                for i in range(startIndex, len(stdYArray)):  # add the previous data to event
                    tevent.addValue(yarray[i])
                tflag = True
                positive = False
                SVM_flag = SVM_flag + 1  # set the flag to denote the event starts
                print("catch the turn")
            elif accy < -0.05 and tthresholdnum > 0:
                tthresholdnum = tthresholdnum + 1
                tfault = faultNum
                tflag = True
            elif (accy > -0.05 or stdY < 0.015) and tfault > 0 and tthresholdnum > 0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy > -0.05 or stdY < 0.03) and tthresholdnum > 0:
                if minLength < tthresholdnum < maxLength:
                    tevent.setEndtime(timestamp)
                    tfault = faultNum
                    tthresholdnum = 0
                    positive = True
                    return tevent
                else:
                    tfault = faultNum
                    tthresholdnum = 0
                    positive = True
                    SVM_flag = SVM_flag - 1
                    LDA_flag = True
                    print("dismiss the turn")
            elif tthresholdnum>0:
                tthresholdnum = tthresholdnum + 1
                tflag = True

    if tflag:
        tevent.addValue(data)


def splitByte(obdData):
    row = obdData.split(" ")[0]
    row = row.split(",")
    return row

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
    global GUI_flag



    serial = getSerial()
    countDown = 15
    obddata = ''
    obddata = obddata.encode('utf-8')
    timestamp = []
    while countDown > 0:
        row = obddata + serial.readline()
        if obddata != b'':
            row = splitByte(row)
            timestamp.append(row[2])
            # calculate the sampling rate of the car
            samplingRate = 14 / ((timestamp[0] - timestamp[-1]) / 1000)
            std_window = int(samplingRate + 0.5)
            xstdQueue = queue.Queue(maxsize=(2*std_window - 1))
            ystdQueue = queue.Queue(maxsize=(2*std_window - 1))
            countDown = countDown - 1

    sfault = bfault = int(2 * int(samplingRate + 0.5) / 5)
    tfault = int(8 * int(samplingRate + 0.5) / 15)
    print('samplingrate--'+str(samplingRate))

    # start the data collection and event detection thread
    thread1 = detectThread()
    thread1.start()

    # start the thread for SVM
    thread2 = SVMthread()
    thread2.start()

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






            # print('total ',eventNum,'turns')
            # print(resultMatrix)
            # file_w = Workbook()
            # table = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
            # write_data(np.array(resultMatrix), table)
            # file_w.save('ForLDA.xls')


def LDATest():
    ldaforevent = LDAForEvent
    ldaforevent.LDATest(ldaforevent, [""])


if __name__ == "__main__":
    main()
