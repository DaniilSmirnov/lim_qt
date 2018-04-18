import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import math
from sympy import *
from sympy.abc import *
import numexpr as ne
from random import *
import time


# noinspection PyArgumentList
class Ui_MainWindow(object):

    i=0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Limit")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.centralwidget.setLayout(self.grid)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.grid.addWidget(self.label,1,0)

        self.delta = QLabel(self.centralwidget)
        self.delta.setObjectName("label")
        self.grid.addWidget(self.delta,1,1)


        self.function_enter = QLineEdit(self.centralwidget)
        self.function_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.function_enter,2,0)

        self.point_enter = QLineEdit(self.centralwidget)
        self.point_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.point_enter,2,1)


        self.epsilon_enter = QLineEdit(self.centralwidget)
        self.epsilon_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.epsilon_enter, 2, 2)

        self.draw_epsilon_button = QPushButton(self.centralwidget)
        self.draw_epsilon_button.setObjectName("pushButton")
        self.grid.addWidget(self.draw_epsilon_button, 3, 1)

        self.clean_all_button = QPushButton(self.centralwidget)
        self.clean_all_button.setObjectName("pushButton")
        self.grid.addWidget(self.clean_all_button, 3, 2)


        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView,4, 0,5,0)

        #self.standart_plot()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 662, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Limit"))
        self.function_enter.setText(_translate("MainWindow", "x"))
        self.point_enter.setText(_translate("MainWindow", "oo"))
        self.epsilon_enter.setText(_translate("MainWindow", "1"))
        self.clean_all_button.setText(_translate("MainWindow","Clean all"))
        self.draw_epsilon_button.setText(_translate("MainWindow", "Draw epsilon"))

        self.function_enter.textChanged.connect(self.draw)
        self.point_enter.textChanged.connect(self.draw)
        self.clean_all_button.clicked.connect(self.clean_all)
        self.draw_epsilon_button.clicked.connect(self.draw_epsilon)
        MainWindow.show()

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

        global i

        function = self.function_enter.text()
        point = self.point_enter.text()

        if (self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function):

            x = Symbol('x')

            try:
                lim = limit(function, x, point)
            except BaseException:
                return 0

            self.label.setText("lim = " + str(lim))

            X = []
            Y = []

            x = -1000

            while x < 1000:
                y = ne.evaluate(function)
                Y.append(y)
                X.append(x)
                x += 1

            self.dataX = X
            self.dataY = Y

            self.graphicsView.setXRange(0, 100)
            c = randint(1, 10)
            self.graphicsView.plot(self.dataX, self.dataY, pen=(c, 3))

            i+=1

    def draw_epsilon(self):

        function = self.function_enter.text()
        point = self.point_enter.text()
        e = float(self.epsilon_enter.text())

        Ex = []
        Ey = []
        Ey1 = []

        if (self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function):

            x = Symbol('x')

            try:
                lim = limit(function, x, point)
            except BaseException:
                return 0

            x = -1000

            while x < 1000:

                Ex.append(x)
                x +=100

                if str(lim) == 'oo' or str(lim) == '-oo':
                    Ey.append(float(10 - e))
                    Ey1.append(float(10 + e))
                else:
                    try:
                        Ey.append(float(float(lim) - e))
                        Ey1.append(float(float(lim) + e))
                        if (float(y) == float(lim - e)) or (float(y) == float(lim + e)):
                            self.delta.setText("y = " + str(y))
                    except TypeError:
                        return 0

            self.dataEx = Ex
            self.dataEy = Ey
            self.dataEy1 = Ey1

            self.graphicsView.plot(self.dataEx, self.dataEy, pen=(3, 3))
            self.graphicsView.plot(self.dataEx, self.dataEy1, pen=(3, 3))

    def clean_all(self):
        self.graphicsView.close()
        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 4, 0, 5, 0)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
