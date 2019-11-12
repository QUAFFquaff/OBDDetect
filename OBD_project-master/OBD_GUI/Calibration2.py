from graphics import *
import time
import pymysql
import pymysql.cursors
from numpy import *
import math


def connectDB():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='obd1234',
                                 db='DRIVINGDB',
                                 port=3306,
                                 charset='utf8')
    return connection


def average(array):
    len = 0
    len = size(array)
    sum = 0
    for i in array:
        sum = sum + i
    return sum / len


def lengthOfForce(x, y, z):
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))


def decomposeToG(G, Acc):
    product = dot(G, Acc)
    Glen = lengthOfForce(G[0], G[1], G[2])
    Alen = lengthOfForce(Acc[0], Acc[1], Acc[2])
    cosine = product / (Glen * Alen)

    return round(cosine * Alen, 9)


def Calibration():
    def drawBackground():
        backgroudcolor = color_rgb(33, 33, 33)
        # === creating the graphic window ===
        win = GraphWin("calibrate instruction", 800, 400)
        win.setCoords(0, 0, 40, 20)

        # === set the background color ===
        Ground = Rectangle(Point(0, 0), Point(40, 20))
        Ground.setFill("light Green")
        Ground.draw(win)

        return win

    win = drawBackground()

    # === draw the calibrate ===
    calibrateBtn = Rectangle(Point(15, 7), Point(25, 13))
    calibrateBtn.setWidth(4)
    calibrateBtn.setFill("light gray")
    calibrateBtn.draw(win)

    pntMsg = Point(20, 10)
    txtMsg = Text(pntMsg, "calibrate")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("blue")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    win.getMouse()

    gpsMsg = Text(Point(30, 18), '')
    gpsMsg.setSize(15)
    gpsMsg.draw(win)

    # === draw the calibrate instruction ===
    calibrateBtn.undraw()
    txtMsg.undraw()
    pntMsg = Point(20, 10)
    txtMsg = Text(pntMsg, "start the car and stand by 5 seconds")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("red")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    time.sleep(1)

    countDownMsg = Text(Point(20, 6), "5")
    countDownMsg.setSize(36)
    countDownMsg.draw(win)

    time.sleep(1)

    countDownMsg.setText("4")

    time.sleep(1)

    countDownMsg.setText("3")

    time.sleep(1)

    countDownMsg.setText("2")

    time.sleep(1)

    countDownMsg.setText("1")

    time.sleep(1)
    countDownMsg.undraw()

    standbyBtn = Rectangle(Point(15, 3), Point(25, 7))
    standbyBtn.setWidth(4)
    standbyBtn.setFill("light gray")
    standbyBtn.draw(win)
    pntMsg = Point(20, 5)
    nextMsg = Text(pntMsg, "next")
    nextMsg.setTextColor("blue")
    nextMsg.setSize(30)
    nextMsg.draw(win)

    g_x = []
    g_y = []
    g_z = []
    try:
        # 获取一个游标
        connection = connectDB()
        with connection.cursor() as cursor:
            sql = 'select * from STATUS ORDER BY time DESC LIMIT 100'
            cout = cursor.execute(sql)

            for row in cursor.fetchall():
                g_x.append(float(row[4]))
                g_y.append(float(row[5]))
                g_z.append(float(row[6]))
                gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
    finally:
        connection.close()
    Gx = average(g_x)
    Gy = average(g_y)
    Gz = average(g_z)
    Gforce = array([float(Gx), float(Gy), float(Gz)])
    glen = lengthOfForce(Gx, Gy, Gz)

    # get unit g force
    unitGx = Gx / glen
    unitGy = Gy / glen
    unitGz = Gz / glen
    unitG = array([float(unitGx), float(unitGy), float(unitGz)])
    print(Gforce)

    win.getMouse()

    # === draw the move forward instruction ===
    standbyBtn.undraw()
    txtMsg.undraw()
    nextMsg.undraw()
    pntMsg = Point(20, 12)
    txtMsg = Text(pntMsg, "move forward for 6 seconds without slow down")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("red")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    standbyBtn = Rectangle(Point(15, 3), Point(25, 7))
    standbyBtn.setWidth(4)
    standbyBtn.setFill("light gray")
    standbyBtn.draw(win)
    pntMsg = Point(20, 5)
    nextMsg = Text(pntMsg, "start")
    nextMsg.setTextColor("blue")
    nextMsg.setSize(30)
    nextMsg.draw(win)

    win.getMouse()
    standbyBtn.undraw()
    nextMsg.undraw()

    # start counting down
    countDownMsg = Text(Point(20, 6), "6")
    countDownMsg.setSize(36)
    countDownMsg.draw(win)
    speedMsg = Text(Point(18, 10), "speed:")
    speedMsg.setSize(20)
    speedMsg.draw(win)
    speedNumMsg = Text(Point(22, 10), "0")
    speedNumMsg.setSize(20)
    speedNumMsg.draw(win)

    for i in range(1, 7):
        time.sleep(1)
        countDownMsg.setText(str(6 - i))
        try:
            connection = connectDB()
            with connection.cursor() as cursor:
                sql = 'select * from STATUS ORDER BY time DESC LIMIT 1'
                count = cursor.execute(sql)

                for row in cursor.fetchall():
                    Speed = row[3]
                    speedNumMsg.setText(Speed)
                    gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
        finally:
            connection.close()

    time.sleep(1)
    countDownMsg.undraw()
    speedMsg.undraw()
    speedNumMsg.undraw()

    A_x = []  # accelerate
    A_y = []
    A_z = []
    try:
        # 获取一个游标
        connection = connectDB()
        with connection.cursor() as cursor:
            sql = 'select * from STATUS ORDER BY time DESC LIMIT 60'
            cout = cursor.execute(sql)

            for row in cursor.fetchall():
                A_x.append(float(row[4]))
                A_y.append(float(row[5]))
                A_z.append(float(row[6]))
                gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
    finally:
        connection.close()
    Ax = average(A_x)
    Ay = average(A_y)
    Az = average(A_z)
    Aforce = array([float(Ax), float(Ay), float(Az)])

    # Get the force component of the resultant force Acc in the g direction
    Ag = decomposeToG(Gforce, Aforce)
    AcomponentG = Ag * unitG
    componentA = Aforce - AcomponentG  # here we get the force for x axis

    # === draw the slow down instruction ===
    txtMsg.undraw()
    pntMsg = Point(20, 12)
    txtMsg = Text(pntMsg, "please slow down to static")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("red")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    S_x = []  # slow down
    S_y = []
    S_z = []
    speedMsg.draw(win)
    speedNumMsg.draw(win)
    while True:
        try:
            # 获取一个游标
            connection = connectDB()
            with connection.cursor() as cursor:
                sql = 'select * from STATUS ORDER BY time DESC LIMIT 1'
                cout = cursor.execute(sql)

                tmpSpeed = 0
                speed = 0
                for row in cursor.fetchall():
                    speed = row[3]
                    speedNumMsg.setText(speed)
                    gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
                if speed == 0:
                    speedMsg.undraw()
                    speedNumMsg.undraw()
                    break
        finally:
            connection.close()
        time.sleep(0.5)

    try:
        # 获取一个游标
        connection = connectDB()
        with connection.cursor() as cursor:
            sql = 'select * from STATUS ORDER BY time DESC LIMIT 30'
            cout = cursor.execute(sql)

            tmpSpeed = -1
            for row in cursor.fetchall():
                if row[3] >= tmpSpeed and row[3] > 0:
                    tmpSpeed = row[3]
                    S_x.append(float(row[4]))
                    S_y.append(float(row[5]))
                    S_z.append(float(row[6]))
                    gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
    finally:
        connection.close()
    Sx = average(S_x)
    Sy = average(S_y)
    Sz = average(S_z)
    Sforce = array([float(Sx), float(Sy), float(Sz)])  # joint force when slow down

    # Get the force component of the resultant force Acc in the g direction
    Sg = decomposeToG(Gforce, Sforce)
    ScomponentG = Sg * unitG
    componentS = Sforce - ScomponentG  # here we get the force for x axis

    backBtn = Rectangle(Point(15, 3), Point(25, 7))
    backBtn.setWidth(4)
    backBtn.setFill("light gray")
    backBtn.draw(win)
    pntMsg = Point(20, 5)
    nextMsg = Text(pntMsg, "next")
    nextMsg.setTextColor("blue")
    nextMsg.setSize(30)
    nextMsg.draw(win)
    win.getMouse()

    # === draw the back forward instruction ===
    backBtn.undraw()
    nextMsg.undraw()
    txtMsg.undraw()
    pntMsg = Point(20, 12)
    txtMsg = Text(pntMsg, "move forward for 6 seconds without slow down")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("red")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    standbyBtn = Rectangle(Point(15, 3), Point(25, 7))
    standbyBtn.setWidth(4)
    standbyBtn.setFill("light gray")
    standbyBtn.draw(win)
    pntMsg = Point(20, 5)
    nextMsg = Text(pntMsg, "start")
    nextMsg.setTextColor("blue")
    nextMsg.setSize(30)
    nextMsg.draw(win)

    win.getMouse()
    standbyBtn.undraw()
    nextMsg.undraw()

    # start counting down
    countDownMsg = Text(Point(20, 6), "6")
    countDownMsg.setSize(36)
    countDownMsg.draw(win)
    speedMsg = Text(Point(18, 10), "speed:")
    speedMsg.setSize(20)
    speedMsg.draw(win)
    speedNumMsg = Text(Point(22, 10), "0")
    speedNumMsg.setSize(20)
    speedNumMsg.draw(win)

    for i in range(1, 7):
        time.sleep(1)
        countDownMsg.setText(str(6 - i))
        try:
            connection = connectDB()
            with connection.cursor() as cursor:
                sql = 'select * from STATUS ORDER BY time DESC LIMIT 1'
                count = cursor.execute(sql)

                for row in cursor.fetchall():
                    Speed = row[3]
                    speedNumMsg.setText(Speed)
                    gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
        finally:
            connection.close()

    time.sleep(1)
    countDownMsg.undraw()
    speedMsg.undraw()
    speedNumMsg.undraw()

    A_x2 = []  # accelerate
    A_y2 = []
    A_z2 = []
    try:
        # 获取一个游标
        connection = connectDB()
        with connection.cursor() as cursor:
            sql = 'select * from STATUS ORDER BY time DESC LIMIT 60'
            cout = cursor.execute(sql)

            for row in cursor.fetchall():
                A_x2.append(float(row[4]))
                A_y2.append(float(row[5]))
                A_z2.append(float(row[6]))
                gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
    finally:
        connection.close()
    Ax2 = average(A_x2)
    Ay2 = average(A_y2)
    Az2 = average(A_z2)
    Aforce2 = array([float(Ax2), float(Ay2), float(Az2)])

    # Get the force component of the resultant force Acc in the g direction
    Ag2 = decomposeToG(Gforce, Aforce2)
    AcomponentG2 = Ag2 * unitG
    componentA2 = Aforce2 - AcomponentG2  # here we get the force for x axis

    # === draw the slow down instruction ===
    txtMsg.undraw()
    pntMsg = Point(20, 12)
    txtMsg = Text(pntMsg, "please slow down to static")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("red")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    S_x2 = []  # slow down
    S_y2 = []
    S_z2 = []
    speedMsg.draw(win)
    speedNumMsg.draw(win)
    while True:
        try:
            # 获取一个游标
            connection = connectDB()
            with connection.cursor() as cursor:
                sql = 'select * from STATUS ORDER BY time DESC LIMIT 1'
                cout = cursor.execute(sql)

                tmpSpeed = 0
                speed = 0
                for row in cursor.fetchall():
                    speed = row[3]
                    speedNumMsg.setText(speed)
                    gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
                if speed == 0:
                    speedMsg.undraw()
                    speedNumMsg.undraw()
                    break
        finally:
            connection.close()
        time.sleep(0.5)

    try:
        # 获取一个游标
        connection = connectDB()
        with connection.cursor() as cursor:
            sql = 'select * from STATUS ORDER BY time DESC LIMIT 30'
            cout = cursor.execute(sql)

            tmpSpeed = -1
            for row in cursor.fetchall():
                if row[3] >= tmpSpeed and row[3] > 0:
                    tmpSpeed = row[3]
                    S_x2.append(float(row[4]))
                    S_y2.append(float(row[5]))
                    S_z2.append(float(row[6]))
                    gpsMsg.setText('GPS:(' + str(row[7]) + ',' + str(row[8]) + ')')
    finally:
        connection.close()
    Sx2 = average(S_x2)
    Sy2 = average(S_y2)
    Sz2 = average(S_z2)
    Sforce2 = array([float(Sx2), float(Sy2), float(Sz2)])  # joint force when slow down

    # Get the force component of the resultant force Acc in the g direction
    Sg2 = decomposeToG(Gforce, Sforce2)
    ScomponentG2 = Sg2 * unitG
    componentS2 = Sforce2 - ScomponentG2  # here we get the force for x axis



    pntMsg = Point(20, 10)
    txtMsg = Text(pntMsg, "you can stop")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("red")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    x = array([0,1,0])
    y = array([1,0,0])


    # calculate the correct x, y, z
    Accx = (componentA[0] + componentA2[0] - componentS[0] - componentS2[0]) / 4
    Accy = (componentA[1] + componentA2[1] - componentS[1] - componentS2[1]) / 4
    Accz = (componentA[2] + componentA2[2] - componentS[2] - componentS2[2]) / 4
    Acclength = lengthOfForce(Accx, Accy, Accz)

    cosPitch = dot(x, array([float(Accx), float(Accy), float(Accz)])) / (Acclength * 1)
    sinPitch = math.sin(math.acos(cosPitch))

    unitAccx = Accx / Acclength
    unitAccy = Accy / Acclength
    unitAccz = Accz / Acclength

    # Swervex = unitAccy*unitG[2] - unitAccz*unitG[1]
    # Swervey = unitAccz*unitG[0] - unitAccx*unitG[2]
    # Swervez = unitAccx*unitG[1] - unitAccy*unitG[0]
    # Swelength = lengthOfForce(Swervex, Swervey, Swervez)

    # cosRoll = dot(y, array([float(Swervex), float(Swervey), float(Swervez)])) / (Swelength*1)
    # sinRoll = math.sin(math.acos(cosRoll))
    sinRoll = Gforce[0] / glen
    cosRoll = math.cos(math.asin(sinRoll))

    Rx = array([(1, 0 , 0),
                (0, cosPitch, -sinPitch),
                (0, sinPitch, cosPitch)])
    Ry = array([(cosRoll, 0, -sinRoll),
                (0, 1, 0),
                (sinRoll, 0, cosRoll)])

    orientationMatrix = dot(Rx, Ry)

    savetxt('orientation.txt', orientationMatrix)

    txtMsg.undraw()
    pntMsg = Point(20, 10)
    txtMsg = Text(pntMsg, "Calibration success")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("red")
    txtMsg.setSize(36)
    txtMsg.draw(win)

    win.getMouse()


Calibration()