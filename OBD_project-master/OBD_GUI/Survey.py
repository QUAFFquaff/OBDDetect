import pymysql
import pymysql.cursors
import time
from graphics import *
from numpy import *
import threading
import queue

matrix = array([(-0.146736425, -0.046935409, 0.98806148),
                (0.986075641, -0.085959069, 0.142358237),
                (0.078251203, 0.995192497, 0.05889519)])
#matrix = loadtxt('orientation.txt')
#drivingData = []




def connectDB():
    connection=pymysql.connect(host='localhost',
                                user='root',
                                password='970608',
                                db='DRIVINGDB',
                                port=3306,
                                charset='utf8')
    return connection

# class of an event
class Event(object):
    def __init__(self, starttime, endtime, type):
        self.starttime = starttime
        self.endtime = endtime
        self.type = type

    def getStarttime(self):
        return self.starttime
    def getEndtime(self):
        return self.endtime
    def getType(self):
        return self.type

lock = threading.Lock()
eventQueue = queue.Queue()




# thread class to write
class myThread(threading.Thread):  # threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        speed = []
        x = []
        y = []
        z = []
        newrecord = 0  # use time to detect if there is new record
        while self.__running.isSet():
            isCatch = False
            try:
                # 获取一个游标
                connection = connectDB()
                with connection.cursor() as cursor:
                    sql = 'select * from test ORDER BY time DESC LIMIT 10'
                    cout = cursor.execute(sql)

                    i = 0

                    for row in cursor.fetchall():
                        if i == 0:
                            if row[2] != newrecord:  # detect if catch the same data
                                isCatch = True
                                newrecord = row[2]
                                speed = []
                                x = []
                                y = []
                                z = []

                        if isCatch:
                            speed.append(row[3])
                            acc = array([float(row[4]), float(row[5]), float(row[6])])
                            acc = dot(acc, matrix)
                            x.append(round(acc[0], 9))
                            y.append(round(acc[1], 9))
                            z.append(round(acc[2], 9))

                        i = i + 1
                # calculate sma
                smaX = calculateSMA(x)
                smaY = calculateSMAY(y)

                print(smaX)
                if isCatch:
                    brakeResult = brakeDetector(smaX, newrecord)
                    if brakeResult:  # when detect a brake event, start a new thread to process
                        eventQueue.put(brakeResult)  # put this event in queue

                    speedupResult = speedupDetector(smaX, newrecord)
                    if speedupResult:  # when detect a speed up event
                        eventQueue.put(brakeResult)  # put this event in queue

            finally:
                connection.close()

    def stop(self):
        self.__running.clear()

# detect brake
bthresholdnum = 0
oneMore = 2
brakeStart = 0

sthresholdnum = 0
negativeMax = 2
speedupStart = 0
def calculateSMA(acc):
    sum = 0
    for i in range(size(acc)):
        sum = sum + (acc[i] * acc[i])
    sma = round(sum / 8, 10) * (acc[0] / abs(acc[0]))
    return sma

def calculateSMAY(acc):
    sum = 0
    for i in range(5):
        sum = sum + (acc[i] * acc[i])
    sma = round(sum / 3, 10) * (acc[0] / abs(acc[0]))
    return sma


def brakeDetector(sma, time):
    global bthresholdnum
    global oneMore
    global brakeStart
    if sma < -0.2:
        bthresholdnum = bthresholdnum + 1
        oneMore = 2
        if brakeStart == 0:
            brakeStart = time
    elif sma > -0.2 and oneMore > 0 and bthresholdnum>0:
        bthresholdnum = bthresholdnum + 1
        oneMore = oneMore - 1
    elif sma > -0.2 and oneMore==0 and bthresholdnum > 0:
        if bthresholdnum > 3:
            brakeEvent  = Event(brakeStart, time, 'brake')
            bthresholdnum = 0
            oneMore = 2
            brakeStart = 0
            return brakeEvent
        bthresholdnum = 0
        oneMore = 2
        brakeStart = 0
    return Event(1542318353140, 1542318354500, 'brake')


def speedupDetector(sma, time):
    global sthresholdnum
    global negativeMax
    global speedupStart
    if sma > 0.01:
        sthresholdnum = sthresholdnum + 1
        negativeMax = 2
        if speedupStart == 0:
            speedupStart = time
    elif sma < 0 and negativeMax > 0 and sthresholdnum>0:
        sthresholdnum = sthresholdnum + 1
        negativeMax = negativeMax -1
    elif negativeMax == 0:
        sthresholdnum = 0
    elif sma > 0.005 and sthresholdnum > 0:
        sthresholdnum = sthresholdnum + 1
    elif sma < 0.005 and sthresholdnum > 0:
        if sthresholdnum > 5:
            sthresholdnum = 0
            speedupEvent = Event(speedupStart, time, 'speedup')
            return speedupEvent
        sthresholdnum = 0
        negativeMax = 2
        speedupStart = 0
    return False




def main():
    def drawBackground():
        backgroudcolor = color_rgb(33, 33, 33)
        # === creating the graphic window ===
        win = GraphWin("calibrate instruction", 1080, 600)
        win.setCoords(0, 0, 40, 20)

        # === set the background color ===
        Ground = Rectangle(Point(0, 0), Point(40, 20))
        Ground.setFill("light Green")
        Ground.draw(win)

        return win

    def confirm():
        print('confirm')

    def cancel():
        print('cancel')

    def catchEvent(event):
        question = Text(Point(20, 12), "Detect an event, is this the normal one?")

        # confirm button board
        confirmBtn = Rectangle(Point(13, 5), Point(18, 7))
        confirmBtn.setWidth(4)
        confirmBtn.setFill("light gray")

        time_local = time.localtime(float(event.getStarttime() / 1000))
        start = time.strftime("%m-%d %H:%M:%S", time_local)
        time_local = time.localtime(float(event.getEndtime() / 1000))
        end = time.strftime("%H:%M:%S", time_local)

        timeText = Text(Point(20, 9), "This event is from "+str(start)+' to '+str(end))

        # confirm text
        confirmText = Text(Point(15, 6), "yes")
        confirmText.setSize(30)

        # cancel button board
        cancelBtn = Rectangle(Point(22, 5), Point(26, 7))
        cancelBtn.setWidth(4)
        cancelBtn.setFill("light gray")

        # cancel text
        cancelText = Text(Point(24, 6), "no")
        cancelText.setSize(36)

        # draw
        question.draw(win)
        timeText.draw(win)
        confirmBtn.draw(win)
        confirmText.draw(win)
        cancelBtn.draw(win)
        cancelText.draw(win)

        choose = win.getMouse()
        if (13 < choose.getX() < 18) and (5 < choose.getY() < 7):
            print('confirm')
            starttime = event.getStarttime()
            endtime = event.getEndtime()
            type = event.getType()
            try:
                # 获取一个游标
                connection = connectDB()
                with connection.cursor() as cursor:
                    sql = 'INSERT INTO eventlogger (startTime, endTime, type, normal) VALUES ('+str(starttime)+','+str(endtime)+',"'+type+'", "yes")'
                    cursor.execute(sql)
                    connection.commit()
            except Exception:
                connection.rollback()
            finally:
                connection.close()
        elif (22 < choose.getX() < 26) and (5 < choose.getY() < 7):
            print('cancel')
            starttime = event.getStarttime()
            endtime = event.getEndtime()
            type = event.getType()
            try:
                # 获取一个游标
                connection = connectDB()
                with connection.cursor() as cursor:
                    sql = 'INSERT INTO eventlogger (startTime, endTime, type, normal) VALUES (' + str(starttime) + ',' + str(endtime) + ',"' + type + '", "no")'
                    cout = cursor.execute(sql)
                    connection.commit()
            except Exception:
                    connection.rollback()
            finally:
                connection.close()

        question.undraw()
        timeText.undraw()
        confirmBtn.undraw()
        confirmText.undraw()
        cancelBtn.undraw()
        cancelText.undraw()

    thread1 = myThread()
    thread1.start()

    # initial
    win = drawBackground()
    pntMsg = Point(20, 13)

    while True:
        tip = Text(pntMsg, "Event detector, when the system detect an event, it will ask you if it is a normal one")

        tip.draw(win)

        time.sleep(0.5)

        if not eventQueue.empty():
            tip.undraw()
            event = eventQueue.get()
            catchEvent(event)
            tip.draw(win)
        else:
            print("empty")


        tip.undraw()


main()

