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

xdots = {}
ydots = {}

functions_list = []

i = 0

edit = false

function_e = " "

amount = 5


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Limit")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.centralwidget.setLayout(self.grid)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.grid.addWidget(self.label, 1, 0)

        self.delta = QLabel(self.centralwidget)
        self.delta.setObjectName("label")
        self.grid.addWidget(self.delta, 1, 1)

        self.function_enter = QLineEdit(self.centralwidget)
        self.function_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.function_enter, 3, 0)

        self.point_enter = QLineEdit(self.centralwidget)
        self.point_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.point_enter, 4, 0)

        self.epsilon_enter = QLineEdit(self.centralwidget)
        self.epsilon_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.epsilon_enter, 5, 0)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName("pushButton")
        self.grid.addWidget(self.save_button, 3, 1)

        self.epsilon_button = QPushButton(self.centralwidget)
        self.epsilon_button.setObjectName("pushButton")
        self.grid.addWidget(self.epsilon_button, 5, 1)

        self.clean_all_button = QPushButton(self.centralwidget)
        self.clean_all_button.setObjectName("pushButton")
        self.grid.addWidget(self.clean_all_button, 4, 1)

        self.delete_button=QPushButton(self.centralwidget)
        self.delete_button.setObjectName("pushButton")
        self.grid.addWidget(self.delete_button,2,1)

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 6, 0, 7, 0)

        self.graphics = QComboBox(self.centralwidget)
        self.graphics.setObjectName("graphics")
        self.grid.addWidget(self.graphics,2,0)
        self.graphics.addItem(" ")

        # self.standart_plot()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 662, 21))
        self.menubar.setObjectName("menubar")

        self.limits_view = self.menubar.addMenu('Limits')
        MainWindow.setMenuBar(self.menubar)

        self.derivatives_view = self.menubar.addMenu('Derivatives')
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
        self.clean_all_button.setText(_translate("MainWindow", "Clean all"))
        self.epsilon_button.setText(_translate("MainWindow", "Draw epsilon"))
        self.save_button.setText(_translate("MainWindow", "Save"))
        self.delete_button.setText(_translate("MainWindow", "Delete"))

        self.function_enter.textChanged.connect(self.draw)
        self.point_enter.textChanged.connect(self.draw)
        self.clean_all_button.clicked.connect(self.clean_all_functions,True)
        self.epsilon_button.clicked.connect(self.draw_epsilon)
        self.save_button.clicked.connect(self.save)
        self.graphics.activated[str].connect(self.setI)
        self.delete_button.clicked.connect(self.delete)

        MainWindow.show()

    def setI(self, text):
        global i,edit,function_e
        i=functions_list.index(text)
        edit=True
        function_e=text

    def delete(self):
       global function_e

       j = functions_list.index(function_e)
       self.graphics.removeItem(j)
       del xdots[str(j)]
       del ydots[str(j)]

       for items in xdots:
         self.dataX = xdots.get(str(items))
         self.dataY = ydots.get(str(items))

         self.graphicsView.setYRange(-10, 10)
         self.graphicsView.setXRange(-10, 10)
         c = randint(1, 10)
         self.graphicsView.plot(self.dataX, self.dataY, pen=(i, 3))

    def clean_all(self):
        self.label.close()
        self.delta.close()
        self.function_enter.close()
        self.point_enter.close()
        self.epsilon_enter.close()
        self.epsilon_button.close()
        self.clean_all_button.close()
        self.graphicsView.close()

    def save(self):

        global i, edit

        function = self.function_enter.text()

        functions_list.append(str(function))

        self.graphics.addItem(str(function))

        self.clean_all_functions(False)

        for items in xdots:

            self.dataX = xdots.get(str(items))
            self.dataY = ydots.get(str(items))

            self.graphicsView.setYRange(-10, 10)
            self.graphicsView.setXRange(-10, 10)
            c = randint(1, 10)
            self.graphicsView.plot(self.dataX, self.dataY, pen=(i, 3))

        if edit:
            j = functions_list.index(function_e)
            self.graphics.removeItem(j)
            del xdots[str(j)]
            del ydots[str(j)]


        i = i + 1
        return 0

    def open_limits(self):
        print("kek")
        # self.clean_all()

    def open_derivatives(self):
        print("kek")
        # self.clean_all()

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

    def func_check(self, s):
        for c in s:
            if c == 'x' or c == 'y':
                return True
        return False

    def draw(self):

        global i

        # global xdots,ydots

        function = self.function_enter.text()
        point = self.point_enter.text()

        X=[]
        Y=[]

        if (self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function):

            x = Symbol('x')

            try:
                lim = limit(function, x, point)
            except BaseException:
                return 0

            self.label.setText("lim = " + str(lim))

            x = -1000
            while x < 1000:
                y = ne.evaluate(function)
                Y.append(y)
                X.append(x)
                ydots.update({str(i): Y})
                xdots.update({str(i): X})
                x += 1

            self.dataX = xdots.get(str(i))
            self.dataY = ydots.get(str(i))

            self.graphicsView.setYRange(-10, 10)
            self.graphicsView.setXRange(-10, 10)
            c = randint(1, 10)
            self.graphicsView.plot(self.dataX, self.dataY, pen=(c, 3))

    def draw_epsilon(self):

        function = self.function_enter.text()
        point = self.point_enter.text()
        e = float(self.epsilon_enter.text())
        self.delta.setText(" ")

        Ex = []
        Ey = []
        Ey1 = []
        Y = []

        if (self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function):

            x = Symbol('x')

            try:
                lim = limit(function, x, point)
            except BaseException:
                return 0

            x = -1000

            while x < 1000:

                y = ne.evaluate(function)
                Ex.append(x)
                x += 1

                if str(lim) == 'oo' or str(lim) == '-oo':
                    Ey.append(float(10 - e))
                    Ey1.append(float(10 + e))
                else:
                    Ey.append(float(float(lim) - e))
                    Ey1.append(float(float(lim) + e))
                    if (float(y) == float(lim - e)) or (float(y) == float(lim + e)):
                        self.delta.setText("y = " + str(y))

            self.dataEx = Ex
            self.dataEy = Ey
            self.dataEy1 = Ey1

            self.graphicsView.plot(self.dataEx, self.dataEy, pen=(3, 3))
            self.graphicsView.plot(self.dataEx, self.dataEy1, pen=(3, 3))

    def clean_all_functions(self,exec):

        if exec:
            xdots.clear()
            ydots.clear()

        self.graphicsView.close()
        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 6, 0, 7, 0)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
