# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

class Ui_MainWindow(object):

    def update2(self):
        data3 = self.data3
        ptr3 = self.ptr3
        data3[ptr3] = np.random.normal()

        ptr3 += 1
        if ptr3 >= data3.shape[0]:
            tmp = data3
            data3 = np.empty(data3.shape[0] * 2)
            data3[:tmp.shape[0]] = tmp
        self.p1.setData(data3[:ptr3])
        self.data3 = data3

        self.p1.setPos(-ptr3, 0)
        self.ptr3 = ptr3

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 511)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bar = QtWidgets.QWidget(self.centralwidget)
        self.bar.setMaximumSize(QtCore.QSize(16777215, 25))
        self.bar.setObjectName("bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.bar)
        self.horizontalLayout.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closer = QtWidgets.QPushButton(self.bar)
        self.closer.setMaximumSize(QtCore.QSize(30, 20))
        self.closer.setText("")
        self.closer.setObjectName("close")
        self.horizontalLayout.addWidget(self.closer)
        self.visit = QtWidgets.QPushButton(self.bar)
        self.visit.setMaximumSize(QtCore.QSize(30, 20))
        self.visit.setText("")
        self.visit.setObjectName("visit")
        self.horizontalLayout.addWidget(self.visit)
        self.mini = QtWidgets.QPushButton(self.bar)
        self.mini.setMaximumSize(QtCore.QSize(30, 20))
        self.mini.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.mini.setText("")
        self.mini.setAutoDefault(False)
        self.mini.setDefault(False)
        self.mini.setFlat(False)
        self.mini.setObjectName("mini")
        self.horizontalLayout.addWidget(self.mini)
        spacerItem = QtWidgets.QSpacerItem(40, 15, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.bar)
        self.Meunu = QtWidgets.QGridLayout()
        self.Meunu.setObjectName("Meunu")
        self.down = QtWidgets.QWidget(self.centralwidget)
        self.down.setMaximumSize(QtCore.QSize(16777215, 120))
        self.down.setObjectName("down")
        self.gridLayout_down = QtWidgets.QGridLayout(self.down)
        self.gridLayout_down.setHorizontalSpacing(5)
        self.gridLayout_down.setObjectName("gridLayout_down")
        self.widget = PlotWidget(self.down)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(300, 120))
        self.widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget.setObjectName("widget")
        self.gridLayout_down.addWidget(self.widget, 0, 0, 1, 1)
        self.CurrentScore = QtWidgets.QLabel(self.down)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CurrentScore.sizePolicy().hasHeightForWidth())
        self.CurrentScore.setSizePolicy(sizePolicy)
        self.CurrentScore.setMinimumSize(QtCore.QSize(20, 60))
        self.CurrentScore.setMaximumSize(QtCore.QSize(300, 120))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.CurrentScore.setFont(font)
        self.CurrentScore.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentScore.setObjectName("CurrentScore")
        self.gridLayout_down.addWidget(self.CurrentScore, 0, 1, 1, 1)
        self.TotalScore = QtWidgets.QLabel(self.down)
        self.TotalScore.setMinimumSize(QtCore.QSize(0, 0))
        self.TotalScore.setMaximumSize(QtCore.QSize(250, 120))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setKerning(True)
        self.TotalScore.setFont(font)
        self.TotalScore.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.TotalScore.setAlignment(QtCore.Qt.AlignCenter)
        self.TotalScore.setObjectName("TotalScore")
        self.gridLayout_down.addWidget(self.TotalScore, 0, 2, 1, 1)
        self.Meunu.addWidget(self.down, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(10)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.Meunu.addWidget(self.line, 1, 0, 1, 1)
        self.up = QtWidgets.QWidget(self.centralwidget)
        self.up.setMinimumSize(QtCore.QSize(0, 0))
        self.up.setMaximumSize(QtCore.QSize(16777215, 350))
        self.up.setObjectName("up")
        self.gridLayout_up = QtWidgets.QGridLayout(self.up)
        self.gridLayout_up.setHorizontalSpacing(5)
        self.gridLayout_up.setVerticalSpacing(7)
        self.gridLayout_up.setObjectName("gridLayout_up")
        self.Turn_bar = QtWidgets.QWidget(self.up)
        self.Turn_bar.setMaximumSize(QtCore.QSize(70, 200))
        self.Turn_bar.setObjectName("Turn_bar")
        self.gridLayout_up.addWidget(self.Turn_bar, 0, 5, 1, 1)
        self.Turn_level = QtWidgets.QWidget(self.up)
        self.Turn_level.setMaximumSize(QtCore.QSize(80, 50))
        self.Turn_level.setObjectName("Turn_level")
        self.gridLayout_up.addWidget(self.Turn_level, 1, 5, 1, 1)
        self.Acc_bar = QtWidgets.QWidget(self.up)
        self.Acc_bar.setMaximumSize(QtCore.QSize(70, 200))
        self.Acc_bar.setObjectName("Acc_bar")
        self.gridLayout_up.addWidget(self.Acc_bar, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_up.addItem(spacerItem1, 0, 2, 1, 1)
        self.feedback = QtWidgets.QToolButton(self.up)
        self.feedback.setMinimumSize(QtCore.QSize(50, 50))
        self.feedback.setMaximumSize(QtCore.QSize(320, 320))
        self.feedback.setFocusPolicy(QtCore.Qt.TabFocus)
        self.feedback.setObjectName("feedback")
        self.gridLayout_up.addWidget(self.feedback, 0, 3, 2, 1)
        self.Brake_bar = QtWidgets.QWidget(self.up)
        self.Brake_bar.setMaximumSize(QtCore.QSize(70, 200))
        self.Brake_bar.setObjectName("Brake_bar")
        self.gridLayout_up.addWidget(self.Brake_bar, 0, 1, 1, 1)
        self.Swerve_level = QtWidgets.QWidget(self.up)
        self.Swerve_level.setMaximumSize(QtCore.QSize(80, 50))
        self.Swerve_level.setObjectName("Swerve_level")
        self.gridLayout_up.addWidget(self.Swerve_level, 1, 6, 1, 1)
        self.Swerve_bar = QtWidgets.QWidget(self.up)
        self.Swerve_bar.setMaximumSize(QtCore.QSize(70, 200))
        self.Swerve_bar.setObjectName("Swerve_bar")
        self.gridLayout_up.addWidget(self.Swerve_bar, 0, 6, 1, 1)
        self.Acc_level = QtWidgets.QWidget(self.up)
        self.Acc_level.setMaximumSize(QtCore.QSize(80, 50))
        self.Acc_level.setObjectName("Acc_level")
        self.gridLayout_up.addWidget(self.Acc_level, 1, 0, 1, 1)
        self.Brake_level = QtWidgets.QWidget(self.up)
        self.Brake_level.setMaximumSize(QtCore.QSize(80, 50))
        self.Brake_level.setObjectName("Brake_level")
        self.gridLayout_up.addWidget(self.Brake_level, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_up.addItem(spacerItem2, 0, 4, 1, 1)
        self.Meunu.addWidget(self.up, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.Meunu)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.closer.setFixedSize(15,15)
        self.visit.setFixedSize(15,15)
        self.mini.setFixedSize(15,15)
        self.closer.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.bar.setStyleSheet('''
            QWidget#bar{
                color:#A7BDBA;
                background:#EFF2F7;
                border:1px solid white;
                border-bottom:0px solid;
                border-top-right-radius:10px;
                border-top-left-radius:10px;
            }
        ''')
        self.up.setStyleSheet('''
            QWidget#up{
                color:#A7BDBA;
                background:#EFF2F7;
                border:1px solid white;
                border-top:0px solid;
            }
        ''')
        self.down.setStyleSheet('''
            QWidget#down{
                border-bottom:1px solid darkGray;
                border-left:1px solid darkGray;
                border-right:1px solid darkGray;
                background:#17191A;
                border-bottom-right-radius:10px;
                border-bottom-left-radius:10px;
            }
            QLabel#CurrentScore{
                color:white;
                border:none;
                font-size:50px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QLabel#TotalScore{
                color:white;
                border:none;
                font-size:15px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(0.97)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.closer.clicked.connect(self.close)

        self.widget.setDownsampling(mode='peak')
        self.widget.setClipToView(True)
        self.widget.setXRange(0, 100)
        self.widget.setLimits(xMax=0)
        self.p1 = self.widget.plot()
        self.p1.setPen(pg.mkPen('y', width=3))
        self.data3 = np.empty(10)
        self.ptr3 = 0


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.CurrentScore.setText(_translate("MainWindow", "86"))
        self.TotalScore.setText(_translate("MainWindow", "1240 points"))
        self.feedback.setText(_translate("MainWindow", "..."))
from pyqtgraph import PlotWidget
import pyqtgraph as pg
