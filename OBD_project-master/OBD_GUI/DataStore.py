import serial
import time
import numpy as np
import pymysql
import pymysql.cursors
import threading
from graphics import *

Speed = 0

def getSerial():
    ser = serial.Serial(port='/dev/rfcomm0', baudrate=57600, timeout=0.5)
    if not ser.is_open:
        ser.open()
    return ser

def connectDB():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='obd1234',
                                 db='DRIVINGDB',
                                 port=3306,
                                 charset='utf8')
    return connection

class dataStore(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        global Speed
        BTserial = getSerial()
        obddata = ''.encode('utf-8')

        while True:
            row = obddata + BTserial.readline()
            print(row)
            row = splitByte(row)
            if row != "":
                timestamp = int(round(time.time() * 1000))
                device = row[0]
                speed = row[1]
                accy = row[2]
                accx = row[3]
                accz = row[4]
                gyox = row[5]
                gyoy = row[6]
                gyoz = row[7]
                acc = np.array([accy, accx, accz])
                acc = acc.astype(np.float64)
                Speed = speed

                try:
                    # 获取一个游标
                    connection = connectDB()
                    connection.autocommit(True)

                    mycursor = connection.cursor()
                    sql = "INSERT INTO STATUS(VIN,DEVICEID,TIME,SPEED,PARAM_1,PARAM_2,PARAM_3,LONGITUDE,LATITUDE,GYROX,GYROY,GYROZ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (device, "zahraa", timestamp, speed, accy, accx, accz, "", "", gyox, gyoy, gyoz)
                    mycursor.execute(sql, val)
                    mycursor.close()
                finally:
                    connection.close()

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
    thread = dataStore()
    thread.setDaemon(True)
    thread.start()


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

    win = drawBackground()

    # === draw the calibrate ===
    calibrateBtn = Rectangle(Point(15, 7), Point(25, 13))
    calibrateBtn.setWidth(4)
    calibrateBtn.setFill("light gray")
    calibrateBtn.draw(win)

    pntMsg = Point(20, 10)
    txtMsg = Text(pntMsg, "start")
    txtMsg.setStyle("bold")
    txtMsg.setTextColor("blue")
    txtMsg.setSize(36)
    txtMsg.draw(win)
    Msg = Text(Point(0,0), "")
    thread.join(1)
    while True:
        txtMsg.setText(Speed)
        Msg.draw(win)
        Msg.undraw()


if __name__ == "__main__":
    main()