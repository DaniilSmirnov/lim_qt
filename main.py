import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import math
from sympy import *
from sympy.abc import *
import numexpr as ne
from random import *
import time


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Limit")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.function_enter = QtWidgets.QLineEdit(self.centralwidget)
        self.function_enter.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.function_enter)
        self.horizontalLayout.addLayout(self.verticalLayout)
        #self.horizontalLayout.addWidget(self.function_enter)

        self.point_enter = QtWidgets.QLineEdit(self.centralwidget)
        self.point_enter.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.point_enter)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.draw_epsilon_button = QtWidgets.QPushButton(self.centralwidget)
        self.draw_epsilon_button.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.draw_epsilon_button)
        self.horizontalLayout.addLayout(self.horizontalLayout)

        self.clean_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.clean_all_button.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.clean_all_button)
        self.horizontalLayout.addLayout(self.horizontalLayout)
        #self.horizontalLayout.addWidget(self.clean_all_button)

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        #self.standart_plot()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 662, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.function_enter.setText(_translate("MainWindow", "2-4/(x*x)"))
        self.point_enter.setText(_translate("MainWindow", "oo"))

        self.function_enter.textChanged.connect(self.draw)
        self.point_enter.textChanged.connect(self.draw)


        MainWindow.show()

    def standart_plot(self):
        chain = self.function_enter.text()

        x = Symbol('x')

        lim = limit(2 - 4 / (x * x), x, oo)
        self.label.setText("lim = " + str(lim))

        X = []
        Y = []

        x = 1

        while x < 1000:
            y = 2 - 4 / (x * x)
            if (y > 0):
                Y.append(y)
                X.append(x)
            x = x + 1

        self.dataX = X
        self.dataY = Y

        self.graphicsView.setXRange(0, 100)
        self.graphicsView.plot(self.dataX, self.dataY, pen=None, symbol='o')  # this line doesn't work

    def brackets_balance(self, s):
        meetings = 0
        for c in s:
            if c == '(':
                meetings += 1
            elif c == ')':
                meetings -= 1
                if meetings == 0:
                    return True
                else:
                    return False

    def brackets_check(self, s):
        for c in s:
            if c == '(' or c == ')':
                return False
        return True

    def func_check(self,s):
        for c in s:
            if c == 'x' or c == 'y':
                return True
        return False

    def draw(self):
        # self.graphicsView.close()

        # self.graphicsView = pg.PlotWidget(self.centralwidget)
        # self.graphicsView.setObjectName("graphicsView")
        # self.verticalLayout.addWidget(self.graphicsView)

        function = self.function_enter.text()
        point = self.point_enter.text()

        if ((self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function) and len(function) > 1):

            x = Symbol('x')

            try:
                lim = limit(function, x, point)
            except BaseException:
                return 0

            self.label.setText("lim = " + str(lim))

            X = []
            Y = []
            Ex = []
            Ey = []
            Ex1 = []
            Ey1 = []
            e = 1

            x = -1000

            while x < 1000:
                y = ne.evaluate(function)

                Y.append(y)
                X.append(x)
                x += 1

                Ex.append(x)
                Ex1.append(x)
                if (isinstance(lim, str)):
                    Ey.append(float(x/100-e))
                    Ey1.append(float(x/100)-e)
                else:
                    try:
                        Ey.append(float(lim - e))
                        Ey1.append(float(lim + e))
                    except TypeError:
                        return 0


            self.dataX = X
            self.dataY = Y
            self.dataEx = X
            self.dataEy = Ey
            self.dataEy1 = Ey1

            self.graphicsView.setXRange(0, 100)
            c = randint(1, 10)
            self.graphicsView.plot(self.dataX, self.dataY, pen=(c, 3))
            self.graphicsView.plot(self.dataX, self.dataEy, pen=(3, 3))
            self.graphicsView.plot(self.dataX, self.dataEy1, pen=(3, 3))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
