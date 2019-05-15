from OBD_GUI.graphics import *


class Panel(object):
    def __init__(self):
        backgroudcolor = color_rgb(33, 33, 33)
        # === creating the graphic window ===
        win = GraphWin("event detection", 500, 300)
        win.setCoords(0, 0, 50, 30)

        # === set the background color ===
        Ground = Rectangle(Point(0, 0), Point(50, 30))
        Ground.setFill("light Green")
        Ground.draw(win)

        self.win = win

    def drawPanel(this):
        # draw the background
        win = this.win
        pntMsg = Point(12, 15)
        txtMsg = Text(pntMsg, "Event")
        txtMsg.setStyle("bold")
        txtMsg.setTextColor("blue")
        txtMsg.setSize(15)
        txtMsg.draw(win)

        gpsTxt = Text(Point(12, 22), "GPS")
        gpsTxt.setTextColor("blue")
        gpsTxt.setSize(15)
        gpsTxt.draw(win)

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
        txtMsg.setSize(15)
        txtMsg.draw(win)

        moneyMsg = Point(41.5, 23)
        moneyMsg = Text(moneyMsg, "$ " + str(3))
        moneyMsg.setStyle("bold")
        moneyMsg.setTextColor("dark green")
        moneyMsg.setSize(15)
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

        image5 = Image(Point(41.5, 15.5), "pic5.gif")
        image5.draw(win)

        image5 = Image(Point(41.5, 5.5), "pic6.gif")
        image5.draw(win)

    def refresh(self):
        tip = Text(Point(0,0),"")
        tip.draw(self.win)
        tip.undraw()