import pymysql
import pymysql.cursors
from numpy import *
from graphics import *
import time as t
from time import *

matrix = array([(-0.146736425, -0.046935409, 0.98806148),
                (0.986075641, -0.085959069, 0.142358237),
                (0.078251203, 0.995192497, 0.05889519)])

drivingData = []

class DrivingStatus(object):
    def __init__(self, time, speed, x, y, z):
        self.time = time
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z

    def getTime(self):
        format = '%Y-%m-%d %H:%M:%S'
        value = t.localtime(float(self.time/1000))
        dt = t.strftime(format, value)
        return dt

def connectDB():
    connection=pymysql.connect(host='localhost',
                                user='root',
                                password='970608',
                                db='DRIVINGDB',
                                port=3306,
                                charset='utf8')
    return connection


time = []
speed = []
x = []
y = []
z = []


def hardBrakeCounter(drivingData):
    #sum = 0
    counter = 0
    thresholdnum = 0
    for i in range(size(drivingData)):
        sum = 0
        if i > 9:
            tmp = i
            for j in range(10):
                sum = sum + (drivingData[tmp].x * drivingData[tmp].x)
                tmp = tmp-1
            sma = round(sum / 8, 10) * (drivingData[i].x / abs(drivingData[i].x))
            #print(sma)
            if sma < (-0.085):
                thresholdnum = thresholdnum + 1
            if sma > -0.085 and thresholdnum > 0:
                if thresholdnum > 5:
                    counter = counter + 1
                    thresholdnum = 0
                    #print(i)
    return counter

def hardSpeedCounter(drivingData):
    counter = 0
    thresholdnum = 0
    negativeMax = 2
    smaList = []
    for i in range(size(drivingData)):
        sum = 0
        if i > 9:
            tmp = i
            for j in range(10):
                sum = sum + (drivingData[tmp].x * drivingData[tmp].x)
                tmp = tmp - 1
            sma = round(sum / 8, 10) * (drivingData[i].x / abs(drivingData[i].x))
            smaList.append(sma)
            # print(sma)
            if sma > 0.045:
                thresholdnum = thresholdnum + 1
            elif sma < 0 and smaList[i - 11] > 0 and thresholdnum > 0: #if sma <0 check if the previous is positive
                negativeMax = 2
            elif sma < 0 and negativeMax > 0 and thresholdnum >0: #if just 2 negative, still count in speed up
                thresholdnum = thresholdnum + 1
                negativeMax =negativeMax-1
            elif negativeMax == 0:
                thresholdnum = 0
                negativeMax = 2
            elif sma > 0.04 and thresholdnum >0:
                thresholdnum = thresholdnum + 1
            elif sma < 0.04 and sma > 0  and thresholdnum > 0:
                #print (thresholdnum)
                if thresholdnum > 10:
                    counter = counter + 1
                thresholdnum = 0

    return(counter)

def hardswerveCounter(drivingData):
    counter = 0
    thresholdnum = 0
    smaList = []
    for i in range(size(drivingData)):
        sum = 0
        if i > 3:
            tmp = i
            for j in range(7):
                sum = sum + (drivingData[tmp].y * drivingData[tmp].y)
                tmp = tmp - 1
            sma = round(sum / 5, 10) * (drivingData[i].y / abs(drivingData[i].y))
            smaList.append(sma)
            if sma > 0.3 or sma < -0.3:
                thresholdnum = thresholdnum + 1
            elif (drivingData[i-1].y*sma) < 0 and (drivingData[i-2].y*sma) < 0 and thresholdnum > 0:
                thresholdnum = thresholdnum + 1
            elif sma <0.3 and sma > -0.3 and thresholdnum > 0:
                if thresholdnum > 5:
                    counter = counter + 1
                    thresholdnum = 0
    return counter


try:
        #获取一个游标
        connection = connectDB()
        with connection.cursor() as cursor:
            sql = 'select * from test '
            cout = cursor.execute(sql)
            #print("数量： "+str(cout))

            i = 0

            for row in cursor.fetchall():
                    time.append(row[2])
                    speed.append(row[3])
                    acc = array([float(row[4]), float(row[5]), float(row[6])])
                    acc = dot(acc, matrix)
                    x.append(round(acc[0], 9))
                    y.append(round(acc[1], 9))
                    z.append(round(acc[2], 9))
                    drivingData.append(DrivingStatus(time[-1],speed[-1],x[-1],y[-1],z[-1]))

        #print(drivingData[0].getTime())
        hardBrakeNum = hardBrakeCounter(drivingData)
        hradSpeedUpNum = hardSpeedCounter(drivingData)
        hardSwerveNum = hardswerveCounter(drivingData)
        print('there are total '+ str(hardBrakeNum) + ' hard brakes')
        print('there are total '+ str(hradSpeedUpNum) + ' hard speed up')
        print('there are total '+ str(hardSwerveNum) + ' hard swerve maneuvers')
finally:
        connection.close()

