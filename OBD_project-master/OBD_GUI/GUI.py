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

        a2 = 8
        a1 = a2 - 2
        a3 = a2 + 2
        self.aBar = Polygon(Point(a1, 10 - 2), Point(a1, 11 - 1), Point(a2, 11), Point(a3, 11 - 1), Point(a3, 10 - 2),
                            Point(a2, 10 - 1))
        self.aBar.setFill(color_rgb(209, 0, 0))
        # self.aBar.draw(win)

        b2 = 15
        b1 = b2 - 2
        b3 = b2 + 2
        self.bBar = Polygon(Point(b1, 10 - 2), Point(b1, 11 - 1), Point(b2, 11), Point(b3, 11 - 1), Point(b3, 10 - 2),
                            Point(b2, 10 - 1))
        self.bBar.setFill(color_rgb(209, 0, 0))
        # self.bBar.draw(win)

        c2 = 22
        c1 = c2 - 2
        c3 = c2 + 2
        self.cBar = Polygon(Point(c1, 10 - 2), Point(c1, 11 - 1), Point(c2, 11), Point(c3, 11 - 1), Point(c3, 10 - 2),
                            Point(c2, 10 - 1))
        self.cBar.setFill(color_rgb(209, 0, 0))
        # self.cBar.draw(win)

        d2 = 29
        d1 = d2 - 2
        d3 = d2 + 2
        self.dBar = Polygon(Point(d1, 10 - 2), Point(d1, 11 - 1), Point(d2, 11), Point(d3, 11 - 1), Point(d3, 10 - 2),
                            Point(d2, 10 - 1))
        self.dBar.setFill(color_rgb(209, 0, 0))
        # self.dBar.draw(win)

        self.moneyMsg = Text(Point(41.5, 20), "")
        self.moneyMsg.draw(win)
        self.tripscoreMsg = Text(Point(41.5, 5), "")
        self.tripscoreMsg.draw(win)

    def drawPanel(self):
        # draw the background
        win = self.win

        # gpsTxt = Text(Point(12, 22), "GPS")
        # gpsTxt.setTextColor("blue")
        # gpsTxt.setSize(15)
        # gpsTxt.draw(win)

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

        # image5 = Image(Point(41.5, 15.5), "pic5.gif")
        # image5.draw(win)
        #
        # image6 = Image(Point(41.5, 5.5), "pic6.gif")
        # image6.draw(win

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

    def drawBar(self, Eventtype):
        a2 = 8
        a1 = a2 - 2
        a3 = a2 + 2
        b2 = 15
        b1 = b2 - 2
        b3 = b2 + 2
        c2 = 22
        c1 = c2 - 2
        c3 = c2 + 2
        d2 = 29
        d1 = d2 - 2
        d3 = d2 + 2
        y = 11
        if Eventtype < 4:
            if Eventtype == 0:
                self.bBar = Polygon(Point(b1, y - 3), Point(b1, y - 1), Point(b2, y), Point(b3, y - 1),
                                    Point(b3, y - 3), Point(b2, y - 2))
                self.bBar.setFill(color_rgb(39, 244, 106))
                self.bBar.draw(self.win)
            if Eventtype == 1:
                self.aBar = Polygon(Point(a1, y - 3), Point(a1, y - 1), Point(a2, y), Point(a3, y - 1),
                                    Point(a3, y - 3), Point(a2, y - 2))
                self.aBar.setFill(color_rgb(39, 244, 106))
                self.aBar.draw(self.win)
            if Eventtype == 2:
                self.cBar = Polygon(Point(c1, y - 3), Point(c1, y - 1), Point(c2, y), Point(c3, y - 1),
                                    Point(c3, y - 3), Point(c2, y - 2))
                self.cBar.setFill(color_rgb(39, 244, 106))
                self.cBar.draw(self.win)
            if Eventtype == 3:
                self.dBar = Polygon(Point(d1, y - 3), Point(d1, y - 1), Point(d2, y), Point(d3, y - 1),
                                    Point(d3, y - 3), Point(d2, y - 2))
                self.dBar.setFill(color_rgb(39, 244, 106))
                self.dBar.draw(self.win)
        elif 3 < Eventtype < 8:
            blocknum = 3
            if Eventtype == 4:
                while blocknum > 0:
                    self.bBar = Polygon(Point(b1, y - 3), Point(b1, y - 1), Point(b2, y), Point(b3, y - 1),
                                        Point(b3, y - 3), Point(b2, y - 2))
                    self.bBar.setFill(color_rgb(208, 173, 44))
                    self.bBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3
            if Eventtype == 5:
                while blocknum > 0:
                    self.aBar = Polygon(Point(a1, y - 3), Point(a1, y - 1), Point(a2, y), Point(a3, y - 1),
                                        Point(a3, y - 3), Point(a2, y - 2))
                    self.aBar.setFill(color_rgb(208, 173, 44))
                    self.aBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3
            if Eventtype == 6:
                while blocknum > 0:
                    self.cBar = Polygon(Point(c1, y - 3), Point(c1, y - 1), Point(c2, y), Point(c3, y - 1),
                                        Point(c3, y - 3), Point(c2, y - 2))
                    self.cBar.setFill(color_rgb(208, 173, 44))
                    self.cBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3
            if Eventtype == 7:
                while blocknum > 0:
                    self.dBar = Polygon(Point(d1, y - 3), Point(d1, y - 1), Point(d2, y), Point(d3, y - 1),
                                        Point(d3, y - 3), Point(d2, y - 2))
                    self.dBar.setFill(color_rgb(208, 173, 44))
                    self.dBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3
        elif 7 < Eventtype < 12:
            blocknum = 6
            if Eventtype == 8:
                while blocknum > 0:
                    self.bBar = Polygon(Point(b1, y - 3), Point(b1, y - 1), Point(b2, y), Point(b3, y - 1),
                                        Point(b3, y - 3), Point(b2, y - 2))
                    self.bBar.setFill(color_rgb(243, 30, 51))
                    self.bBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3
            if Eventtype == 9:
                while blocknum > 0:
                    self.aBar = Polygon(Point(a1, y - 3), Point(a1, y - 1), Point(a2, y), Point(a3, y - 1),
                                        Point(a3, y - 3), Point(a2, y - 2))
                    self.aBar.setFill(color_rgb(243, 30, 51))
                    self.aBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3
            if Eventtype == 10:
                while blocknum > 0:
                    self.cBar = Polygon(Point(c1, y - 3), Point(c1, y - 1), Point(c2, y), Point(c3, y - 1),
                                        Point(c3, y - 3), Point(c2, y - 2))
                    self.cBar.setFill(color_rgb(243, 30, 51))
                    self.cBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3
            if Eventtype == 11:
                while blocknum > 0:
                    self.dBar = Polygon(Point(d1, y - 3), Point(d1, y - 1), Point(d2, y), Point(d3, y - 1),
                                        Point(d3, y - 3), Point(d2, y - 2))
                    self.dBar.setFill(color_rgb(243, 30, 51))
                    self.dBar.draw(self.win)
                    blocknum = blocknum - 1
                    y = y + 3

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




