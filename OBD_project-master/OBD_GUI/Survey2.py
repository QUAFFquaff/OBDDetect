import pymysql
import pymysql.cursors
import time
from graphics import *
from numpy import *
import threading
import queue

lock = threading.Lock()
eventQueue = queue.Queue()

speed = 0
currenttime = 0
newrecord = 0  # use time to detect if there is new record

# build database connection
def connectDB():
    connection=pymysql.connect(host='localhost',
                                user='root',
                                password='970608',
                                db='DRIVINGDB',
                                port=3306,
                                charset='utf8')
    return connection

# thread class to write
class myThread(threading.Thread):  # threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        global speed
        global newrecord
        global currenttime
        newrecord = 0  # use time to detect if there is new record
        while self.__running.isSet():
            isCatch = False
            try:
                # 获取一个游标
                connection = connectDB()
                with connection.cursor() as cursor:
                    sql = 'select * from STATUS ORDER BY time DESC LIMIT 1'
                    cout = cursor.execute(sql)



                    for row in cursor.fetchall():

                        if row[2] != newrecord:  # detect if catch the same data
                            isCatch = True
                            newrecord = row[2]
                            speed = 0

                        if isCatch:
                            speed = row[3]
                            currenttime = row[2]

            finally:
                connection.close()

    def stop(self):
        self.__running.clear()

def main():
    def drawBackground():
        backgroudcolor = color_rgb(33, 33, 33)
        # === creating the graphic window ===
        win = GraphWin("calibrate instruction", 1080, 600)
        win.setCoords(0, 0, 40, 35)

        # === set the background color ===
        Ground = Rectangle(Point(0, 0), Point(40, 35))
        #Ground.setFill("light Green")
        Ground.draw(win)

        return win

    thread1 = myThread()
    thread1.start()

    # initial
    win = drawBackground()

    speedBar = Rectangle(Point(2, 30.5), Point(38, 34.5))
    speedBar.setWidth(2)
    speedBar.setFill("light gray")
    speedBar.draw(win)

    speedtext = Text(Point(18, 32.5), "Speed:")
    speedtext.setSize(35)
    speedtext.draw(win)

    # brake module
    brakeBar = Rectangle(Point(2, 19), Point(19.5, 30))
    brakeBar.setWidth(2)
    brakeBar.setFill("white")
    brakeBar.draw(win)

    braketext = Text(Point(11, 28.5), "Brake")
    braketext.setSize(28)
    braketext.draw(win)

    # speed up module
    sppedupBar = Rectangle(Point(20.5, 19), Point(38, 30))
    sppedupBar.setWidth(2)
    sppedupBar.setFill("white")
    sppedupBar.draw(win)

    speeduptext = Text(Point(29, 28.5), "Speedup")
    speeduptext.setSize(28)
    speeduptext.draw(win)

    # turn module
    turnBar = Rectangle(Point(2, 7), Point(19.5, 18))
    turnBar.setWidth(2)
    turnBar.setFill("white")
    turnBar.draw(win)

    turntext = Text(Point(11, 16.5), "Turn")
    turntext.setSize(28)
    turntext.draw(win)

    # swerve module
    swerveBar = Rectangle(Point(20.5, 7), Point(38, 18))
    swerveBar.setWidth(2)
    swerveBar.setFill("white")
    swerveBar.draw(win)

    swervetext = Text(Point(29, 16.5), "Swerve")
    swervetext.setSize(28)
    swervetext.draw(win)

    logBar = Rectangle(Point(2, 0.5), Point(38, 6.5))
    logBar.setWidth(2)
    logBar.setFill("light gray")
    logBar.draw(win)

    # ===================button===========================
    # 4 brake buttons
    brake1 = Rectangle(Point(3, 24), Point(10.5, 27))
    brake1.setFill("red")
    brake1.draw(win)
    braketext1 = Text(Point(6.5,25.5),'Very Aggressive')
    braketext1.draw(win)

    brake2 = Rectangle(Point(11, 24), Point(18.5, 27))
    brake2.setFill("orange")
    brake2.draw(win)
    braketext1 = Text(Point(14.5, 25.5), 'Aggressive')
    braketext1.draw(win)

    brake3 = Rectangle(Point(3, 20), Point(10.5, 23))
    brake3.setFill("light green")
    brake3.draw(win)
    braketext1 = Text(Point(6.5, 21.5), 'Careful')
    braketext1.draw(win)

    brake4 = Rectangle(Point(11, 20), Point(18.5, 23))
    brake4.setFill("yellow")
    brake4.draw(win)
    braketext1 = Text(Point(14.5, 21.5), 'Very Careful')
    braketext1.draw(win)

    # 4 speed up buttons
    speedup1 = Rectangle(Point(21.5, 24), Point(29, 27))
    speedup1.setFill("red")
    speedup1.draw(win)
    speeduptext1 = Text(Point(25, 25.5), 'Very Aggressive')
    speeduptext1.draw(win)

    speedup2 = Rectangle(Point(29.5, 24), Point(37, 27))
    speedup2.setFill("orange")
    speedup2.draw(win)
    speeduptext2 = Text(Point(33, 25.5), 'Aggressive')
    speeduptext2.draw(win)

    speedup3 = Rectangle(Point(21.5, 20), Point(29, 23))
    speedup3.setFill("light green")
    speedup3.draw(win)
    speeduptext3 = Text(Point(25, 21.5), 'Careful')
    speeduptext3.draw(win)

    speedup4 = Rectangle(Point(29.5, 20), Point(37, 23))
    speedup4.setFill("yellow")
    speedup4.draw(win)
    speeduptext4 = Text(Point(33, 21.5), 'Very Careful')
    speeduptext4.draw(win)

    # 4 Turn buttons
    turn1 = Rectangle(Point(3, 12), Point(10.5, 15))
    turn1.setFill("red")
    turn1.draw(win)
    turntext1 = Text(Point(6.5, 13.5), 'Very Aggressive')
    turntext1.draw(win)

    turn2 = Rectangle(Point(11, 12), Point(18.5, 15))
    turn2.setFill("orange")
    turn2.draw(win)
    turntext2 = Text(Point(14.5, 13.5), 'Very Aggressive')
    turntext2.draw(win)

    turn3 = Rectangle(Point(3, 8), Point(10.5, 11))
    turn3.setFill("light green")
    turn3.draw(win)
    turntext3 = Text(Point(6.5, 9.5), 'Careful')
    turntext3.draw(win)

    turn4 = Rectangle(Point(11, 8), Point(18.5, 11))
    turn4.setFill("yellow")
    turn4.draw(win)
    turntext4 = Text(Point(14.5, 9.5), 'Very Careful')
    turntext4.draw(win)

    # 4 Turn buttons
    swerve1 = Rectangle(Point(21.5, 12), Point(29, 15))
    swerve1.setFill("red")
    swerve1.draw(win)
    swervetext1 = Text(Point(25, 13.5), 'Very Aggressive')
    swervetext1.draw(win)

    swerve2 = Rectangle(Point(29.5, 12), Point(37, 15))
    swerve2.setFill("orange")
    swerve2.draw(win)
    swervetext2 = Text(Point(33, 13.5), 'Aggressive')
    swervetext2.draw(win)

    swerve3 = Rectangle(Point(21.5, 8), Point(29, 11))
    swerve3.setFill("light green")
    swerve3.draw(win)
    swervetext3 = Text(Point(25, 9.5), 'Careful')
    swervetext3.draw(win)

    swerve4 = Rectangle(Point(29.5, 8), Point(37, 11))
    swerve4.setFill("yellow")
    swerve4.draw(win)
    swervetext4 = Text(Point(33, 9.5), 'Very Careful')
    swervetext4.draw(win)


    global speed
    global currenttime
    brakes = 0
    speedups = 0
    turns = 0
    swerves = 0
    recordText1 = Text(Point(20, 4), '')
    recordText2 = Text(Point(20, 2), '')
    while True:
        speedValue = Text(Point(22, 32.5), str(speed))
        speedValue.setSize(35)
        speedValue.draw(win)



        choose = win.checkMouse()
        if(choose != None):
            # ====================================brake button =============================
            if (3 < choose.getX() < 10.5) and (24 < choose.getY() < 27):
                brakes = brakes + 1
                print(currenttime)
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Brake' + '","' + 'Very Aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(brakes)+' brakes recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (11 < choose.getX() < 18.5) and (24 < choose.getY() < 27):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Brake' + '","' + 'Aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                brakes = brakes + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(brakes) + ' brakes recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (3 < choose.getX() < 10.5) and (20 < choose.getY() < 23):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Brake' + '","' + 'Careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                brakes = brakes + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(brakes) + ' brakes recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (11 < choose.getX() < 18.5) and (20 < choose.getY() < 23):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Brake' + '","' + 'Very Careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                brakes = brakes + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very Careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(brakes) + ' brakes recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            # ====================================speed up button =============================
            if (21.5 < choose.getX() < 29) and (24 < choose.getY() < 27):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Speedup' + '","' + 'Very aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                speedups = speedups + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(speedups) + ' speedups recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (29.5 < choose.getX() < 37) and (24 < choose.getY() < 27):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Speedup' + '","' + 'Aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                speedups = speedups + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(speedups) + ' speedups recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (21.5 < choose.getX() < 29) and (20 < choose.getY() < 23):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Speedup' + '","' + 'Careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                speedups = speedups + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(speedups) + ' speedups recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (29.5 < choose.getX() < 37) and (20 < choose.getY() < 23):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Speedup' + '","' + 'Very careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                speedups = speedups + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very Careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(speedups) + ' speedups recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            # ====================================turn button =============================
            if (3 < choose.getX() < 10.5) and (12 < choose.getY() < 15):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Turn' + '","' + 'Very aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                turns = turns + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(turns) + ' turns recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (11 < choose.getX() < 18.5) and (12 < choose.getY() < 15):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Turn' + '","' + 'Aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                turns = turns + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(turns) + ' turns recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (3 < choose.getX() < 10.5) and (8 < choose.getY() < 11):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Turn' + '","' + 'Careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                turns = turns + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(turns) + ' turns recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (11 < choose.getX() < 18.5) and (8 < choose.getY() < 11):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Turn' + '","' + 'Very careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                turns = turns + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(turns) + ' turns recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            # ====================================swerve button =============================
            if (21.5 < choose.getX() < 29) and (12 < choose.getY() < 15):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Swerve' + '","' + 'Very aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                swerves = swerves + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(swerves) + ' swerves recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (29.5 < choose.getX() < 37) and (12 < choose.getY() < 15):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Swerve' + '","' + 'Aggressive' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                swerves = swerves + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Aggressive] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(swerves) + ' swerves recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (21.5 < choose.getX() < 29) and (8 < choose.getY() < 11):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Swerve' + '","' + 'Careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                swerves = swerves + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(swerves) + ' swerves recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
            if (29.5 < choose.getX() < 37) and (8 < choose.getY() < 11):
                try:
                    # 获取一个游标
                    connection = connectDB()
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO label (labeltime, behavior, type) VALUES (' + str(
                            currenttime) + ',"' + 'Swerve' + '","' + 'Very Careful' + '")'
                        cursor.execute(sql)
                        connection.commit()
                except Exception:
                    connection.rollback()
                swerves = swerves + 1
                recordText1.undraw()
                recordText2.undraw()
                recordText1 = Text(Point(20, 4), 'Your selection of [Very Careful] has been recorded')
                recordText1.setSize(25)
                recordText1.draw(win)
                recordText2 = Text(Point(20, 2), str(swerves) + ' swerves recorded')
                recordText2.setSize(25)
                recordText2.draw(win)
        time.sleep(0.1)
        speedValue.undraw()






main()