import numpy as np
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


matrix = np.array([[0.0649579822346719, 0, -0.997888],
               [-0.140818558599268, 0.989992982850364, -0.00916664939131784],
               [0.987902117670584, 0.141116596851819, 0.0643079465924438]])


def connectDB():
    connection=pymysql.connect(host='localhost',
                                user='root',
                                password='970608',
                                db='DRIVINGDB',
                                port=3306,
                                charset='utf8')
    return connection

class Event(object):
    def __init__(self,starttime,type):
        self.start = starttime
        self.type =type
        self.vect = []

    def setEndtime(self,endtime):
        self.end = endtime

    def getDuration(self):
        duration = (self.end-self.start)/5
        return duration

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def addValue(self,data):
        temp = []
        temp = self.vect
        temp.append(data)
        self.vect=temp

        return self.vect
    def getValue(self):
        return self.vect

    def getType(self):
        return self.type


def getLowPass(lowpass, opt):
    acc = []
    if opt=='x':
        for i in range(lowpass.qsize()):
            temp = lowpass.get()
            lowpass.put(temp)
            acc.append(temp[1])
    if opt=='y':
        for i in range(lowpass.qsize()):
            temp = lowpass.get()
            lowpass.put(temp)
            acc.append(temp[0])
    if opt=='z':
        for i in range(lowpass.qsize()):
            temp = lowpass.get()
            lowpass.put(temp)
            acc.append(temp[2])

    return acc

def write_data(dataTemp, table):
    data = np.array(dataTemp)
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            table.write(i, j, data[i][j])


xstdQueue =queue.Queue(maxsize=10)
ystdQueue = queue.Queue(maxsize=10)

thresholdnum = 0
bthresholdnum = 0
sevent=Event(0,-1)
bevent = Event(0,-1)
sfault = 3
bfault = 3
def detectEvent(data):
    global thresholdnum
    global bthresholdnum
    global sevent
    global bevent
    global sfault
    global  bfault
    sflag = False
    bflag = False
    xarray = []
    x = []
    xstdQueue.put(data)

    if xstdQueue.full():
        for i in range(xstdQueue.qsize()):
            temp = xstdQueue.get()
            xarray.append(temp)
            x.append(temp[3])
            xstdQueue.put(temp)
        xstdQueue.get()
        stdX = np.std(x,ddof=1)

        accx =data[3]
        timestamp = data[0]

        if accx>0.1 and stdX>0.025 and thresholdnum == 0:
            thresholdnum = thresholdnum + 1
            sevent = Event(xarray[-5][0],0)
            for i in range(-5,-1):
                sevent.addValue(xarray[i])
            sflag = True
        elif accx > 0.05 and thresholdnum > 0:
            thresholdnum = thresholdnum + 1
            sfault = 3
            sflag = True
        elif accx < 0.05 and sfault > 0 and thresholdnum > 0:
            sfault = sfault-1
            thresholdnum = thresholdnum+1
            sflag = True
        elif (accx < 0.05 or stdX < 0.025) and thresholdnum > 0:
            if thresholdnum > 10:
                sevent.setEndtime(timestamp)
                sfault = 3
                thresholdnum = 0
                return sevent
            thresholdnum = 0
            sfault = 3

        if accx<-0.10 and stdX>0.02 and bthresholdnum ==0:
            bthresholdnum = bthresholdnum + 1
            bevent = Event(xarray[-5][0],2)
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
tevent = Event(0,-1)
tfault = 3
swerveFlag = False
positive = True
negative = True
def detectYEvent(data):
    global tthresholdnum
    global tevent
    global tfault
    global swerveFlag
    global positive
    global negative
    yarray = []
    y = []
    tflag = False
    ystdQueue.put(data)

    if ystdQueue.full():
        for i in range(ystdQueue.qsize()):
            temp = ystdQueue.get()
            yarray.append(temp)
            y.append(temp[2])
            ystdQueue.put(temp)
        ystdQueue.get()
        stdY = np.std(y,ddof=1)

        accy = data[2]
        timestamp = data[0]


        if positive:
            if accy > 0.1 and stdY > 0.02 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum+1
                tevent = Event(yarray[-5][0],4)
                for i in range(-5,-1):
                    tevent.addValue(yarray[i])
                tflag = True
                negative = False
            elif accy >0.05 and tthresholdnum>0:
                tthresholdnum = tthresholdnum + 1
                tfault = 3
                tflag = True
            elif (accy < 0.05 or stdY<0.02) and tfault>0 and tthresholdnum>0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy < 0.05 or stdY<0.02) and tthresholdnum>0:
                if tthresholdnum>15 and not swerveFlag:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    negative = True
                    return tevent
                elif stdY>0.1:
                    swerveFlag = True
                    tthresholdnum = tthresholdnum+1
                    tflag = True
                elif tthresholdnum > 15:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    negative = True
                    swerveFlag = False
                    return tevent
                else:
                    tflag = 3
                    tthresholdnum = 0
                    swerveFlag = False
                    negative = True

        if negative:
            if accy < -0.1 and stdY > 0.02 and tthresholdnum == 0:
                tthresholdnum = tthresholdnum+1
                tevent = Event(yarray[-5][0],4)
                for i in range(-5,-1):
                    tevent.addValue(yarray[i])
                tflag = True
                positive = False
            elif accy < -0.05 and tthresholdnum>0:
                tthresholdnum = tthresholdnum + 1
                tfault = 3
                tflag = True
            elif (accy > -0.05 or stdY<0.02) and tfault>0 and tthresholdnum>0:
                tfault = tfault - 1
                tthresholdnum = tthresholdnum + 1
                tflag = True
            elif (accy > -0.05 or stdY<0.02) and tthresholdnum>0:
                if tthresholdnum>15 and not swerveFlag:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    positive = True
                    return tevent
                elif stdY>0.1:
                    swerveFlag = True
                    tthresholdnum = tthresholdnum+1
                    tflag = True
                elif tthresholdnum > 15:
                    tevent.setEndtime(timestamp)
                    tfault = 3
                    tthresholdnum = 0
                    positive = True
                    swerveFlag = False
                    return tevent
                else:
                    tflag = 3
                    tthresholdnum = 0
                    swerveFlag = False
                    positive = True

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
    t = (data[-1, 0] - data[0, 0])/1000
    meanSP = np.mean(data[:, 1])
    varSP = np.std(data[:, 1])
    return [rangeAX, rangeAY, varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY, maxOX,
            maxOY, minAY, meanSP, varSP, t]

def nomalization(vect):
    max = [0.619,0.944,0.208,0.281,6.075,17.258,0.286,0.349,3.901,26.569,10.171,60.271,0.097,106.5,29.291,24.982]
    min = [0.034,0.021,0.009,0.004,0.325,0.845,-0.312,-0.281,-3.816,-20.210,-0.061,-1.291,-0.818,4.979,0.408,1.581]
    for i in range(len(vect)):
        vect[i] = (vect[i] - min[i]) / (max[i] - min[i])
    return vect

def drawBackground():
    backgroudcolor = color_rgb(33, 33, 33)
    # === creating the graphic window ===
    win = GraphWin("event detection", 500, 300)
    win.setCoords(0, 0, 10, 5)

    # === set the background color ===
    Ground = Rectangle(Point(0, 0), Point(10, 5))
    Ground.setFill("light Green")
    Ground.draw(win)

    return win

def main():
    svm = joblib.load('svm.pkl')
    data = open_workbook('STATUS.xlsx')
    table = data.sheets()[0]
    resultMatrix = []

    start = 0  # 开始的行
    end = 3500  # 结束的行
    # end = 4450  # 结束的行

    lowpass = queue.Queue()

    eventNum = 0
    badEventNum = 0


    win = drawBackground()

    for x in range(start, end):
        row = table.row_values(x)


        accx = row[4]
        accy = row[5]
        accz = row[6]
        acc = np.array([accx, accy, accz])
        acc = acc.astype(np.float64)

        # calibration
        acc = np.dot(matrix, acc)
        lowpass.put(acc)
        if x>=29:
            row = table.row_values(x-1)
            timestamp = row[2]
            speed = row[3]
            gyox = row[9]
            gyoy = row[10]
            gyoz = row[11]
            #print(acc[0],acc[1],acc[2])
            # low pass filter
            b, a = signal.butter(3, 0.4, 'low')
            accxsf = signal.filtfilt(b, a, getLowPass(lowpass,'x'))
            accysf = signal.filtfilt(b, a, getLowPass(lowpass,'y'))
            acczsf = signal.filtfilt(b, a, getLowPass(lowpass,'z'))
            #print(accxsf, accysf,acczsf)
            # if(x>=30):
                # lowpassed.append([accysf[-2],accxsf[-2],acczsf[-2]])

            #detect event
            event = detectEvent([timestamp,speed,accysf[-2],accxsf[-2],acczsf[-2],gyox,gyoy,gyoz])
            yevent = detectYEvent([timestamp,speed,accysf[-2],accxsf[-2],acczsf[-2],gyox,gyoy,gyoz])

            #  define type and intensity
            if not event is None:


                vect = np.array(event.getValue())
                # print(vect)
                vect = vect.astype(np.float64)

                vect = calcData(vect)
                vect = nomalization(vect)

                result = svm.predict([vect])

                if result<4:
                    print(event.getType(), ' event: ', event.getStart(), '-', event.getEnd())
                    print(result)
                    eventNum = eventNum + 1
                    if result==1 or result==3:
                        badEventNum = badEventNum+1
                    resultMatrix.append([event.getStart(),event.getEnd(),result[0]])
            if not yevent is None:
                print(yevent.getType(), ' event: ', yevent.getStart(), '-', yevent.getEnd())

                vect = np.array(yevent.getValue())
                vect = vect.astype(np.float64)

                vect = calcData(vect)
                vect = nomalization(vect)

                result = svm.predict([vect])
                print(result)
                # if result>3:
                if result ==5 or result == 7:
                    badEventNum = badEventNum+1
                eventNum = eventNum +1
                resultMatrix.append([yevent.getStart(), yevent.getEnd(), result[0]])


            lowpass.get()
        # else:
        #     lowpassed.append([acc[0],acc[1],acc[2]])

    print('total ',eventNum,'turns')
    # print(resultMatrix)
    frequency = badEventNum/((int(resultMatrix[-1][1])-int(resultMatrix[0][0]))/(1000*3600))
    print("the frequency of Bad events",frequency," times/h")
    totaleventtime = 0
    for i in range(len(resultMatrix)):
        totaleventtime = totaleventtime+(int(resultMatrix[i][1])-int(resultMatrix[i][0]))
    print("the density if ",totaleventtime/(int(resultMatrix[-1][1])-int(resultMatrix[0][0])))

    file_w = Workbook()
    table = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
    write_data(np.array(resultMatrix), table)
    file_w.save('ForLDA.xls')


if __name__ == "__main__":
    main()