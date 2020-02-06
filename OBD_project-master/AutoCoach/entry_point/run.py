import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from AutoCoach.GUI import *
from AutoCoach.QssLoader import *
import pyqtgraph as pg

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        styleFile = '././QSS/style.qss'
        qssStyle = QssLoader.loadQss(styleFile)
        self.setStyleSheet(qssStyle)




def run():
    app = QApplication(sys.argv)
    myWin = MyWindow()

    myWin.show()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(myWin.update2)
    timer.start(50)
    sys.exit(app.exec_())