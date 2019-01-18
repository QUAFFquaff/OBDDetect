import pymysql
import pymysql.cursors
from numpy import *
from graphics import *
import time as t
from time import *

#matrix = array([(-0.146736425, -0.046935409, 0.98806148),
#                (0.986075641, -0.085959069, 0.142358237),
#                (0.078251203, 0.995192497, 0.05889519)])
matrix = loadtxt('orientation.txt')
drivingData = []


class DrivingStatus(object):
    def __init__(self, time, speed, x, y, z):
        self.time = time
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z

    def setSMAX(self, smaX):
        self.smaX = smaX

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


def drawBackground():
    backgroudcolor = color_rgb(33, 33, 33)
    # === creating the graphic window ===
    win = GraphWin("Proactive Driver Panel", 1080, 600)
    win.setCoords(0, 0, 50, 30)

    # === set the background color ===
    Ground = Rectangle(Point(0, 0), Point(50, 30))
    Ground.setFill("light Green")
    Ground.draw(win)


    return win

def show(money):

    win = drawBackground()

    # === draw the reward box ===
    rewardB = Rectangle(Point(36, 21), Point(47, 28))
    rewardB.setWidth(4)
    rewardB.setFill("light gray")
    rewardB.draw(win)

    # === draw the alert box ===
    rewardB = Rectangle(Point(36, 11), Point(47, 19.5))
    rewardB.setWidth(4)
    rewardB.setFill("light gray")
    rewardB.draw(win)

    # === draw the recommend box ===
    rewardB = Rectangle(Point(36, 1.5), Point(47, 9.5))
    rewardB.setWidth(4)
    rewardB.setFill("light gray")
    rewardB.draw(win)

    pntMsg = Point(41.5, 26)
    txtMsg = Text(pntMsg, "Reward")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("blue")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    moneyMsg = Point(41.5, 23)
    moneyMsg = Text(moneyMsg, "$ " + str(money))
    moneyMsg.setStyle("bold")
    moneyMsg.setTextColor("dark green")
    moneyMsg.setSize(36)
    moneyMsg.draw(win)

    # show leftdown icon
    image1 = Image(Point(7.5, 2.75), "pic1.gif")
    image1.draw(win)

    image2 = Image(Point(14.5, 2.75), "pic2.gif")
    image2.draw(win)

    image3 = Image(Point(21.5, 2.75), "pic3.gif")
    image3.draw(win)

    image4 = Image(Point(28.5, 2.75), "pic4.gif")
    image4.draw(win)


    speed = []
    x = []
    y = []
    z = []
    newrecord = 0

    sleep(1)

    while True:
        isCatch = False
        try:
            #获取一个游标
            connection = connectDB()
            with connection.cursor() as cursor:
                sql = 'select * from test ORDER BY time DESC LIMIT 10'
                cout = cursor.execute(sql)

                i = 0

                for row in cursor.fetchall():
                    if i == 0:
                        if row[2] != newrecord:# detect if catch the same data
                            isCatch = True
                            newrecord = row[2]
                            time = []
                            speed = []
                            x = []
                            y = []
                            z = []


                    if isCatch:
                        time.append(row[2])
                        speed.append(row[3])
                        acc = array([float(row[4]), float(row[5]), float(row[6])])
                        acc = dot(acc, matrix)
                        x.append(round(acc[0], 9))
                        y.append(round(acc[1], 9))
                        z.append(round(acc[2], 9))

                    i = i+1

                drivingData.append(DrivingStatus(time[0], speed[0], x[0], y[0], z[0]))
                #calculate sma
                print(drivingData[0].getTime())
                smaX = calculateSMA(x)
                smaY = calculateSMAY(y)
                #print(smaX)


                if isCatch:
                    # detect hard brake number
                    detectHardBrake(smaX)
                    # detetc hard sped up number
                    detectHardSpeed(smaX, x)
                    # detect hard change line
                    detectHardSwerve(smaY, y)

                #detect hard brake number
                detectHardBrake(smaX)
                #detetc hard sped up number
                detectHardSpeed(smaX, x)
                #detect hard change line
                detectHardSwerve(smaY, y)



            # === display acc ===

            # acc abar
            wid = 2
            x2 = 7.5
            x1 = x2 - wid
            x3 = x2 + wid
            y1 = 8
            apntMsg = Point(x2, 28.5)
            atxtMsg = Text(apntMsg, "Hard")
            if smaX > 0.05:
                smaX = 0.05
                atxtMsg.setStyle("bold")
                atxtMsg.setTextColor("red")
                atxtMsg.setSize(15)
                atxtMsg.draw(win)
            blocknum = int((14 * (smaX / 0.05)) / 2)
            accValue = y1 - 1 + 14 * (smaX / 0.05) + blocknum
            aBar = Polygon(Point(x1, y1 - 2), Point(x1, accValue - 1), Point(x2, accValue), Point(x3, accValue - 1), Point(x3, y1 - 2),
                           Point(x2, y1 - 1))
            if isCatch:
                aBar.undraw()

            if smaX >= 0:
                while blocknum > 0:
                    aBar = Polygon(Point(x1, y1 - 2), Point(x1, y1), Point(x2, y1+1), Point(x3, y1), Point(x3, y1-2), Point(x2, y1-1))
                    blocknum = blocknum - 1
                    y1 = y1 + 3
                    aBar.draw(win)
                    aBar.setFill(color_rgb(209, 0, 0))
                aBar = Polygon(Point(x1, y1 - 2), Point(x1, accValue - 1), Point(x2, accValue), Point(x3, accValue - 1),Point(x3, y1 - 2),Point(x2, y1 - 1))
                bBar.undraw()
                aBar.draw(win)
                aBar.setFill(color_rgb(209, 0, 0))

            # brake bbar
            x2 = 14.5
            x1 = x2-wid
            x3 = x2+wid
            y1 = 8
            bpntMsg = Point(x2, 28.5)
            btxtMsg = Text(bpntMsg, "Hard")
            if smaX < -0.1:
                smaX = -0.1
                btxtMsg.setStyle("bold")
                btxtMsg.setTextColor("red")
                btxtMsg.setSize(15)
                btxtMsg.draw(win)
            blocknum = int((14*((-smaX)/0.1))/2)
            brakeValue = y1 - 1 + 14*((-smaX)/0.1)+blocknum
            bBar = Polygon(Point(x1, y1 - 2), Point(x1, brakeValue - 1), Point(x2, brakeValue), Point(x3, brakeValue - 1), Point(x3, y1 - 2),Point(x2, y1 - 1))

            if isCatch:
                bBar.undraw()

            if smaX < 0:
                while blocknum > 0:
                    bBar = Polygon(Point(x1, y1 - 2), Point(x1, y1), Point(x2, y1+1), Point(x3, y1), Point(x3, y1-2), Point(x2, y1-1))
                    blocknum = blocknum - 1
                    y1 = y1 + 3
                    bBar.draw(win)
                    bBar.setFill(color_rgb(230, 240, 0))
                bBar = Polygon(Point(x1, y1 - 2), Point(x1, brakeValue-1), Point(x2, brakeValue), Point(x3, brakeValue - 1), Point(x3, y1-2), Point(x2, y1 - 1))
                aBar.undraw()
                bBar.draw(win)
                bBar.setFill(color_rgb(230, 240, 0))

            # === display swerve ===
            x2 = 21.5
            x1 = x2 - wid
            x3 = x2 + wid
            y1 = 8
            cpntMsg = Point(x2, 28.5)
            ctxtMsg = Text(cpntMsg, 'hard')
            if abs(smaY)>0.3:
                ctxtMsg.setStyle("bold")
                ctxtMsg.setTextColor("red")
                ctxtMsg.setSize(15)
                ctxtMsg.draw(win)
                smaY =0.3
            blocknum = int((14 * (abs(smaY) / 0.3)) / 2)
            swerveValue = y1 - 1 + 14 * (abs(smaY) / 0.3) + blocknum
            cBar = Polygon(Point(x1, y1 - 2), Point(x1, swerveValue - 1), Point(x2, swerveValue), Point(x3, swerveValue - 1),
                           Point(x3, y1 - 2), Point(x2, y1 - 1))

            if isCatch:
                cBar.undraw()
            while blocknum > 0:
                cBar = Polygon(Point(x1, y1 - 2), Point(x1, y1), Point(x2, y1 + 1), Point(x3, y1),
                               Point(x3, y1 - 2), Point(x2, y1 - 1))
                blocknum = blocknum - 1
                y1 = y1 + 3
                cBar.draw(win)
                cBar.setFill('blue')
            cBar = Polygon(Point(x1, y1 - 2), Point(x1, swerveValue - 1), Point(x2, swerveValue), Point(x3, swerveValue - 1),
                           Point(x3, y1 - 2), Point(x2, y1 - 1))
            cBar.draw(win)
            cBar.setFill('blue')


            # speed dbar
            x2 = 28.5
            x1 = x2 - wid
            x3 = x2 + wid
            y1 = 8
            spntMsg = Point(x2, 28.5)
            stxtMsg = Text(spntMsg, str(speed[0]))
            if speed[0]>120:
                stxtMsg.setStyle("bold")
                stxtMsg.setTextColor("red")
                stxtMsg.setSize(15)
                stxtMsg.draw(win)
                speed[0] =120
            blocknum = int((14 * ((speed[0]) / 120)) / 2)
            speedValue = y1 - 1 + 14 * ((speed[0]) / 120) + blocknum
            dBar = Polygon(Point(x1, y1 - 2), Point(x1, speedValue - 1), Point(x2, speedValue), Point(x3, speedValue - 1),
                           Point(x3, y1 - 2), Point(x2, y1 - 1))

            if isCatch:
                dBar.undraw()

            while blocknum > 0:
                dBar = Polygon(Point(x1, y1 - 2), Point(x1, y1), Point(x2, y1 + 1), Point(x3, y1),
                                   Point(x3, y1 - 2), Point(x2, y1 - 1))
                blocknum = blocknum - 1
                y1 = y1 + 3
                dBar.draw(win)
                dBar.setFill(color_rgb(209, 100, 10))
            dBar = Polygon(Point(x1, y1 - 2), Point(x1, speedValue - 1), Point(x2, speedValue), Point(x3, speedValue - 1),
                               Point(x3, y1 - 2), Point(x2, y1 - 1))
            dBar.draw(win)
            dBar.setFill(color_rgb(209, 100, 10))

            # show right down icon (uper one)
            if True:
                image5 = Image(Point(41.5, 15.5), "pic5.gif")
                image5.draw(win)

            # show right down icon (lower one)
            if True:
                image5 = Image(Point(41.5, 5.5), "pic6.gif")
                image5.draw(win)

            atxtMsg.undraw()
            btxtMsg.undraw()
            stxtMsg.undraw()

        finally:
            connection.close()



def calculateSMA(acc):
    sum = 0
    for i in range(size(acc)):
        sum = sum+ (acc[i]*acc[i])
    sma = round(sum/8, 10)*(acc[0]/abs(acc[0]))
    return sma

def calculateSMAY(acc):
    sum = 0
    for i in range(5):
        sum = sum+ (acc[i]*acc[i])
    sma = round(sum/3, 10)*(acc[0]/abs(acc[0]))
    return sma


bthresholdnum = 0
bcount = 0
hardBrakeList = []
def detectHardBrake(sma):
    global bthresholdnum
    global hardBrakeList
    global bcount
    if sma < -0.1:
        bthresholdnum = bthresholdnum + 1
        hardBrakeList.append(drivingData[-1])
    if sma > -0.1 and bthresholdnum > 0:
        if bthresholdnum > 5 :
            bcount = bcount + 1
            bthresholdnum = 0
            return True
        bthresholdnum = 0
    return False



scounter = 0
sthresholdnum = 0
negativeMax = 2
def detectHardSpeed(sma,x):
    global scounter
    global sthresholdnum
    global negativeMax

    if sma < 0 and x[1] > 0 and sthresholdnum > 0:  # if sma <0 check if the previous is positive
        negativeMax = 2
    if sma > 0.045:
        sthresholdnum = sthresholdnum + 1

    if sma > 0.045:
        sthresholdnum = sthresholdnum + 1
    elif sma < 0 and x[1] > 0 and sthresholdnum > 0:  # if sma <0 check if the previous is positive
        negativeMax = 2
    elif sma < 0 and negativeMax > 0 and sthresholdnum > 0:  # if just 2 negative, still count in speed up
        sthresholdnum = sthresholdnum + 1
        negativeMax = negativeMax - 1
    elif sma > 0.04 and sthresholdnum > 0:
        sthresholdnum = sthresholdnum + 1
    elif sma < 0.04 and sthresholdnum > 0:
        if sthresholdnum > 10:
            scounter = scounter + 1
            sthresholdnum = 0
            negativeMax = 2
            return True
        sthresholdnum = 0
        negativeMax = 2
    return False 
    elif negativeMax == 0:
        sthresholdnum = 0
        negativeMax = 2
    elif sma > 0.04 and sthresholdnum > 0:
        sthresholdnum = sthresholdnum + 1
    elif sma < 0.04 and sma > 0 and sthresholdnum > 0:
        if sthresholdnum > 10:
            scounter = scounter + 1
            sthresholdnum = 0


tcounter = 0
tthresholdnum = 0 #threshold for turn or change line
def detectHardSwerve(sma,y):
    global tcounter
    global tthresholdnum
    if sma > 0.3 or sma < -0.3:
        tthresholdnum = tthresholdnum + 1
    elif (y[1] * sma) < 0 and (y[2] * sma) < 0 and tthresholdnum > 0:
        tthresholdnum = tthresholdnum + 1
    elif sma < 0.3 and sma > -0.3 and tthresholdnum > 0:
        if tthresholdnum > 5:
            tcounter = tcounter + 1
            tthresholdnum = 0
            return True
        tthresholdnum = 0
    return False




show(0)