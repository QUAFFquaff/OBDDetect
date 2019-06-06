from graphics import *
import time
import datetime
import pygame


class Panel(object):
    def __init__(self):

        # === creating the graphic window ===
        win = GraphWin("event detection", 480, 320)
        win.setCoords(0, 0, 48, 32)

        # === set the background color ===
        Ground = Rectangle(Point(0, 0), Point(48, 32))
        Ground.setFill("light Green")
        Ground.draw(win)

        self.win = win

        self.eventMsg = Text(Point(18, 28), "Event")
        self.eventMsg.setStyle("bold")
        self.eventMsg.setTextColor("blue")
        self.eventMsg.setSize(15)
        self.eventMsg.draw(win)

        # parameters for aBar
        self._a2 = 8
        self._a1 = self._a2 - 2
        self._a3 = self._a2 + 2

        # parameters for bBar
        self._b2 = 15
        self._b1 = self._b2 - 2
        self._b3 = self._b2 + 2

        # parameters for cBar
        self._c2 = 22
        self._c1 = self._c2 - 2
        self._c3 = self._c2 + 2

        # parameters for dBar
        self._d2 = 29
        self._d1 = self._d2 - 2
        self._d3 = self._d2 + 2

        # parameters for sth
        self._y = 11

        # generate Bar list
        self._aList = []
        self._bList = []
        self._cList = []
        self._dList = []

        # parameters for sth
        self.moneyMsg = Text(Point(41.5, 20), "")
        self.moneyMsg.draw(win)
        self.tripscoreMsg = Text(Point(41.5, 5), "")
        self.tripscoreMsg.draw(win)
        self.initBarList()

    def initBarList(self):
        y = self._y
        for i in range(6):
            # a bars
            aBar = Polygon(Point(self._a1, y - 3), Point(self._a1, y - 1), Point(self._a2, y),
                           Point(self._a3, y - 1),
                           Point(self._a3, y - 3), Point(self._a2, y - 2))
            aBar.setFill(color_rgb(208, 173, 44))
            self._aList.append(aBar)

            # b Bar
            bBar = Polygon(Point(self._b1, y - 3), Point(self._b1, y - 1), Point(self._b2, y),
                                Point(self._b3, y - 1),
                                Point(self._b3, y - 3), Point(self._b2, y - 2))
            bBar.setFill(color_rgb(208, 173, 44))
            self._bList.append(bBar)

            # c Bar
            cBar = Polygon(Point(self._c1, y - 3), Point(self._c1, y - 1), Point(self._c2, y),
                                Point(self._c3, y - 1),
                                Point(self._c3, y - 3), Point(self._c2, y - 2))
            cBar.setFill(color_rgb(208, 173, 44))
            self._cList.append(cBar)


            # d Bar
            dBar = Polygon(Point(self._d1, y - 3), Point(self._d1, y - 1), Point(self._d2, y),
                                Point(self._d3, y - 1),
                                Point(self._d3, y - 3), Point(self._d2, y - 2))
            dBar.setFill(color_rgb(208, 173, 44))
            self._dList.append(dBar)

            y += 3

    def drawPanel(self):
        # draw the background
        win = self.win

        # === draw the reward box ===
        rewardB1 = Rectangle(Point(36, 15), Point(47, 28))
        rewardB1.setWidth(4)
        rewardB1.setFill("light gray")
        rewardB1.draw(win)

        # === draw the alert box ===
        rewardB2 = Rectangle(Point(36, 1.5), Point(47, 13))
        rewardB2.setWidth(4)
        rewardB2.setFill("light gray")
        rewardB2.draw(win)

        # === draw the text on the box ===
        pntMsg = Point(41.5, 25)
        txtMsg = Text(pntMsg, "Time Window\nScore")
        txtMsg.setStyle("bold")
        txtMsg.setTextColor("purple")
        txtMsg.setSize(13)
        txtMsg.draw(win)

        # === draw the text on the box ===
        pntMsg = Point(41.5, 10)
        txtMsg = Text(pntMsg, "Trip\nScore")
        txtMsg.setStyle("bold")
        txtMsg.setTextColor("purple")
        txtMsg.setSize(13)
        txtMsg.draw(win)

        # show leftdown icon
        image1 = Image(Point(7.5, 4), "pic1.gif")
        image1.draw(win)

        image2 = Image(Point(14.5, 4), "pic2.gif")
        image2.draw(win)

        image3 = Image(Point(21.5, 4), "pic3.gif")
        image3.draw(win)

        image4 = Image(Point(28.5, 4), "pic4.gif")
        image4.draw(win)

    def change_score(self, time_window_score, trip_score):

        win = self.win
        self.moneyMsg.undraw()
        self.tripscoreMsg.undraw()

        # === write time window score on the box ===
        self.moneyMsg = Text(Point(41.5, 20), str(time_window_score)[:4])
        self.moneyMsg.setStyle("bold")
        self.moneyMsg.setTextColor("dark green")
        self.moneyMsg.setSize(15)
        self.moneyMsg.draw(win)

        # === write trip score on the box ===
        self.tripscoreMsg = Text(Point(41.5, 5), str(trip_score)[0:4])
        self.tripscoreMsg.setStyle("bold")
        self.tripscoreMsg.setTextColor("dark green")
        self.tripscoreMsg.setSize(15)
        self.tripscoreMsg.draw(win)

        if time_window_score < 40: self.sadSound()
        if time_window_score > 90: self.happySound()

    def refresh(self):
        tip = Text(Point(0, 0), "")
        tip.draw(self.win)
        tip.undraw()

    def showEvent(self, start, end, event_type):
        self.eventMsg.undraw()
        self.eventMsg.setText(start + "--" + end + "[" + self.transfer(event_type) + "]")
        self.eventMsg.draw(self.win)
        self.drawBar(event_type)

    def transfer(self, Eventtype):
        if Eventtype == 0:
            return "normal speedup"
        if Eventtype == 1:
            return "normal brake"
        if Eventtype == 2:
            return "normal turn"
        if Eventtype == 3:
            return "normal swerve"
        if Eventtype == 4:
            return "medium speedup"
        if Eventtype == 5:
            return "medium brake"
        if Eventtype == 6:
            return "medium turn"
        if Eventtype == 7:
            return "medium swerve"
        if Eventtype == 8:
            return "high speedup"
        if Eventtype == 9:
            return "high brake"
        if Eventtype == 10:
            return "high turn"
        if Eventtype == 11:
            return "high swerve"

    def drawBar(self, event_type):
        if event_type % 4 == 0:
            self.addaBar(event_type)
        elif event_type % 4 == 1:
            self.addbBar(event_type)
        if event_type % 4 == 2:
            self.addcBar(event_type)
        if event_type % 4 == 3:
            self.adddBar(event_type)

    def addaBar(self, event_type):
        block_num = 2 * int(event_type / 4) + 1
        y = self._y
        while block_num > 0:
            self._aList[block_num].draw()
            block_num -= 1
            y += 3

    def addbBar(self, event_type):
        block_num = 2 * int(event_type / 4) + 1
        y = self._y
        while block_num > 0:
            self._bList[block_num].draw(self.win)
            block_num -= 1
            y += 3

    def addcBar(self, event_type):
        block_num = 2 * int(event_type / 4) + 1
        y = self._y
        while block_num > 0:
            self._cList[block_num].draw(self.win)
            self.cBar.draw(self.win)
            block_num -= 1
            y += 3

    def adddBar(self, event_type):
        block_num = 2 * int(event_type / 4) + 1
        y = self._y
        while block_num > 0:
            self._dList[block_num].draw(self.win)
            block_num -= 1
            y += 3
    def clean_bars(self):
        self.removeaBar()
        self.removebBar()
        self.removecBar()
        self.removedBar()
    def removeaBar(self):
        for node in self._aList:
            node.undraw()
    def removebBar(self):
        for node in self._bList:
            node.undraw()
    def removecBar(self):
        for node in self._cList:
            node.undraw()
    def removedBar(self):
        for node in self._dList:
            node.undraw()

    def happySound(self):
        file = 'sound/POP Brust 16 copy.mp3'
        pygame.mixer.init()
        track = pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        time.sleep(0.05)
        pygame.mixer.music.stop()

    def sadSound(self):
        file = 'sound/NEGATIVE Failure Beeps Oh No 05 copy.mp3'
        pygame.mixer.init()
        track = pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        time.sleep(0.1)
        pygame.mixer.music.stop()

    def coinSound(self):
        file = 'sound/COINS Collect Chime 01 copy.mp3'
        pygame.mixer.init()
        track = pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        time.sleep(0.1)
        pygame.mixer.music.stop()
