from random import *
import numexpr as ne
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from sympy import *
from sympy.abc import *
from pymsgbox import *

xdots = {}
ydots = {}

exdots = {}
eydots = {}
ey1dots = {}

tanxdots = {}
tanydots = {}

diffxp = {}
diffyp = {}

diffdxp = {}
diffdyp = {}

diffdxpv = {} #вертикальная линия приращения
diffdypv = {}

functions_list = []

colors = []

area = 100

i = 0

step = 0.01 #0.45

edit = false

function_e = " "

amount = 5

instructions = '  **     to power \n ' \
             ' sqrt   to square root \n' \



class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Limit")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.centralwidget.setLayout(self.grid)

        self.result = QLabel(self.centralwidget)
        self.result.setObjectName("label")
        self.grid.addWidget(self.result, 1, 0)

        self.delta = QLabel(self.centralwidget)
        self.delta.setObjectName("label")
        self.grid.addWidget(self.delta, 1, 1)

        self.function_enter = QLineEdit(self.centralwidget)
        self.function_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.function_enter, 3, 0)

        self.point_enter = QLineEdit(self.centralwidget)
        self.point_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.point_enter, 4, 0)

        self.epsilon_enter1 = QLineEdit(self.centralwidget)
        self.epsilon_enter1.setObjectName("lineEdit")
        self.grid.addWidget(self.epsilon_enter1, 5, 0)

        self.epsilon_enter2 = QLineEdit(self.centralwidget)
        self.epsilon_enter2.setObjectName("lineEdit")
        self.grid.addWidget(self.epsilon_enter2, 5, 1)

        self.epsilon_enter3 = QLineEdit(self.centralwidget)
        self.epsilon_enter3.setObjectName("lineEdit")
        self.grid.addWidget(self.epsilon_enter3, 5, 2)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName("pushButton")
        self.grid.addWidget(self.save_button, 3, 1)

        self.epsilon_button = QPushButton(self.centralwidget)
        self.epsilon_button.setObjectName("pushButton")
        self.grid.addWidget(self.epsilon_button, 5, 3)

        self.clean_all_button = QPushButton(self.centralwidget)
        self.clean_all_button.setObjectName("pushButton")
        self.grid.addWidget(self.clean_all_button, 4, 1)

        pg.setConfigOption('background','w')
        pg.setConfigOption('foreground','k')
        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 6, 0, 7, 0)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 662, 21))
        self.menubar.setObjectName("menubar")

        self.limits_view = self.menubar.addMenu('Limits')
        limits_action=QAction(MainWindow)
        limits_action.setText("Open")
        limits_action.triggered.connect(self.open_limits)
        self.limits_view.addAction(limits_action)
        self.limits_view.setEnabled(False)

        MainWindow.setMenuBar(self.menubar)

        self.derivatives_view = self.menubar.addMenu('Derivatives')
        derivatives_action = QAction(MainWindow)
        derivatives_action.setText("Open")
        derivatives_action.triggered.connect(self.open_derivatives)
        self.derivatives_view.addAction(derivatives_action)

        self.instructions_view = self.menubar.addMenu('Instructions')
        instructions_action= QAction(MainWindow)
        instructions_action.setText("Open")
        instructions_action.triggered.connect(self.open_instructions)
        self.instructions_view.addAction(instructions_action)

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
        self.epsilon_enter1.setText(_translate("MainWindow", "0"))
        self.epsilon_enter2.setText(_translate("MainWindow", "0"))
        self.epsilon_enter3.setText(_translate("MainWindow", "0"))
        self.epsilon_button.setText(_translate("MainWindow", "Draw epsilon"))
        self.save_button.setText(_translate("MainWindow", "Save"))
        self.clean_all_button.setText(_translate("MainWindow", "Clean"))
        self.delta.setText(_translate("MainWindow", " "))

        self.function_enter.textChanged.connect(self.draw)
        self.point_enter.textChanged.connect(self.draw)
        self.epsilon_enter1.textChanged.connect(self.draw_epsilon)
        self.epsilon_enter2.textChanged.connect(self.draw_epsilon)
        self.epsilon_enter3.textChanged.connect(self.draw_epsilon)
        self.clean_all_button.clicked.connect(self.clean_all_functions, True)

        MainWindow.show()

    def clean_all(self,exec):
        if exec == 1:
            self.result.close()
            self.delta.close()
            self.function_enter.close()
            self.point_enter.close()
            self.epsilon_enter1.close()
            self.epsilon_button.close()
            self.clean_all_button.close()
            self.graphicsView.close()
            self.save_button.close()
        if exec == 0:
            self.graphicsView.close()
            self.draw_df.close()
            self.draw_tangent.close()
            self.draw_additional.close()
            self.delta_enter.close()
            self.function_enter.close()
            self.point_enter.close()
            self.save_button.close()
            self.clean_all_button.close()

    def open_limits(self):

        self.limits_view.setEnabled(False)
        self.derivatives_view.setEnabled(True)

        self.clean_all(0)

        self.result = QLabel(self.centralwidget)
        self.result.setObjectName("label")
        self.grid.addWidget(self.result, 1, 0)

        self.delta = QLabel(self.centralwidget)
        self.delta.setObjectName("label")
        self.grid.addWidget(self.delta, 1, 1)

        self.function_enter = QLineEdit(self.centralwidget)
        self.function_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.function_enter, 3, 0)

        self.point_enter = QLineEdit(self.centralwidget)
        self.point_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.point_enter, 4, 0)

        self.epsilon_enter1 = QLineEdit(self.centralwidget)
        self.epsilon_enter1.setObjectName("lineEdit")
        self.grid.addWidget(self.epsilon_enter1, 5, 0)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName("pushButton")
        self.grid.addWidget(self.save_button, 3, 1)

        self.epsilon_button = QPushButton(self.centralwidget)
        self.epsilon_button.setObjectName("pushButton")
        self.grid.addWidget(self.epsilon_button, 5, 1)

        self.clean_all_button = QPushButton(self.centralwidget)
        self.clean_all_button.setObjectName("pushButton")
        self.grid.addWidget(self.clean_all_button, 4, 1)

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 6, 0, 7, 0)

        self.retranslateUi(MainWindow)

    def open_derivatives(self):

        global i

        i = 0

        self.clean_all(1)

        self.derivatives_view.setEnabled(False)
        self.limits_view.setEnabled(True)

        self.function_enter = QLineEdit(self.centralwidget)
        self.function_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.function_enter, 1, 0)
        self.function_enter.textChanged.connect(self.draw)

        self.point_enter = QLineEdit(self.centralwidget)
        self.point_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.point_enter, 1, 1)
        self.point_enter.textChanged.connect(self.draw)

        self.delta_enter = QLineEdit(self.centralwidget)
        self.delta_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.delta_enter, 1, 2)
        self.delta_enter.textChanged.connect(self.draw)

        self.draw_tangent = QPushButton(self.centralwidget)
        self.draw_tangent.setObjectName("pushButton")
        self.grid.addWidget(self.draw_tangent, 2, 0)
        self.draw_tangent.setText("Tangent")
        self.draw_tangent.clicked.connect(self.drawtan)

        self.draw_additional = QPushButton(self.centralwidget)
        self.draw_additional.setObjectName("pushButton")
        self.grid.addWidget(self.draw_additional, 2, 1)
        self.draw_additional.setText("Additional")
        self.draw_additional.clicked.connect(self.drawtan)

        self.draw_df = QPushButton(self.centralwidget)
        self.draw_df.setObjectName("pushButton")
        self.grid.addWidget(self.draw_df, 2, 2)
        self.draw_df.setText("df")
        self.draw_df.clicked.connect(self.drawdiff)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName("pushButton")
        self.grid.addWidget(self.save_button, 3, 0)

        self.clean_all_button = QPushButton(self.centralwidget)
        self.clean_all_button.setObjectName("pushButton")
        self.grid.addWidget(self.clean_all_button, 3, 1)

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 5, 0, 7, 0)

        self.save_button.clicked.connect(self.save)
        self.graphics.activated[str].connect(self.setI)
        self.delete_button.clicked.connect(self.delete)
        self.clean_all_button.clicked.connect(self.clean_all_functions, True)

        self.save_button.setText("Save")
        self.delete_button.setText("Delete")
        self.clean_all_button.setText("Clean all")

    def open_instructions(self):

        global instructions

        alert(text=instructions, title='Instructions', button='OK')

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

        try:

            self.clean_all_functions(False)

            global i

            function = self.function_enter.text()
            point = self.point_enter.text()

            X = []
            Y = []

            if (self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function):

                x = Symbol('x')

                try:
                    lim = limit(function, x, point)
                except BaseException:
                    return 0

                lim = str(lim)

                if lim[0] == '<':
                    lim = " Not exist"

                self.result.setText("lim = " + str(lim))

                x = -area
                while x < area:
                    y = ne.evaluate(function)
                    if int(y) > 100 or int(y) < -100:
                        x += step
                        continue
                    else:
                        Y.append(y)
                        X.append(x)
                        ydots.update({str(i): Y})
                        xdots.update({str(i): X})
                    x += step

                self.dataX = xdots.get(str(i))
                self.dataY = ydots.get(str(i))

                self.graphicsView.setYRange(-10, 10)
                self.graphicsView.setXRange(-10, 10)
                c = randint(1, 10)
                colors.append(c)
                self.graphicsView.plot(self.dataX, self.dataY, pen=(colors[i], 3))

                self.draw_epsilon()
        except BaseException:
            self.result.setText("Error")
            alert(text='Error in draw module \n Please check function enter', title='Error', button='OK')
            return 0

    def drawtan(self):

        global i

        function = self.function_enter.text()
        point = self.point_enter.text()

        X = []
        Y = []

        if (self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function):

            x = Symbol('x')

            try:
                dif = str(diff(function,x))
            except BaseException:
                return 0

            x = int(point)

            dif = ne.evaluate(dif)

            fx0 = ne.evaluate(function)

            function = str(fx0)+"+"+str(dif)+"*"+ "(" + "x" + "-" + str(point) + ")"

            x = -area

            while x < area:
                y = ne.evaluate(function)
                Y.append(y)
                X.append(x)
                tanydots.update({str(i): Y})
                tanxdots.update({str(i): X})
                x += step

            self.dataX = tanxdots.get(str(i))
            self.dataY = tanydots.get(str(i))

            self.graphicsView.setYRange(-10, 10)
            self.graphicsView.setXRange(-10, 10)
            c = randint(1, 10)
            self.graphicsView.plot(self.dataX, self.dataY, pen=(c, 3))

    def drawdiff(self):

        global i

        point = self.point_enter.text()
        function = self.function_enter.text()
        delta_point = self.delta_enter.text()

        X = []
        Y = []

        y = -area

        while y < area:

            Y.append(y)
            X.append(int(point))
            diffyp.update({str(i): Y})
            diffxp.update({str(i): X})
            y += step

        self.dataX = diffxp.get(str(i))
        self.dataY = diffyp.get(str(i))

        self.graphicsView.setYRange(-10, 10)
        self.graphicsView.setXRange(-10, 10)
        c = randint(1, 10)

        self.graphicsView.plot(self.dataX, self.dataY, pen=(c, 3))

        X = []
        Y = []

        x=int(point)
        y=ne.evaluate(function)

        x = -area

        while x < area:
            Y.append(y)
            X.append(x)
            diffdyp.update({str(i): Y})
            diffdxp.update({str(i): X})
            x += step

        self.dataX = diffdxp.get(str(i))
        self.dataY = diffdyp.get(str(i))

        self.graphicsView.setYRange(-10, 10)
        self.graphicsView.setXRange(-10, 10)
        c = randint(1, 10)

        self.graphicsView.plot(self.dataX, self.dataY, pen=(c, 3))

        X = []
        Y = []

        y = -area

        while y < area:
            Y.append(y)
            X.append(int(point)+int(delta_point))
            diffdypv.update({str(i): Y})
            diffdxpv.update({str(i): X})
            y += step

        self.dataX = diffdxpv.get(str(i))
        self.dataY = diffdypv.get(str(i))

        self.graphicsView.setYRange(-10, 10)
        self.graphicsView.setXRange(-10, 10)
        c = randint(1, 10)

        self.graphicsView.plot(self.dataX, self.dataY, pen=(c, 3))

    def draw_epsilon(self):

        function = self.function_enter.text()
        point = self.point_enter.text()

        e1_exec = True
        e2_exec = True
        e3_exec = True

        try:
            e1 = float(self.epsilon_enter1.text())
        except BaseException:
            e1_exec = False
        try:
            e2 = float(self.epsilon_enter2.text())
        except BaseException:
            e2_exec = False
        try:
            e3 = float(self.epsilon_enter3.text())
        except BaseException:
            e3_exec = False

        Ex = []
        Ey = []
        Ey1 = []

        Ey2 = []
        Ey3 = []

        Ey4 = []
        Ey5 = []

        if (self.brackets_balance(function) or self.brackets_check(function)) and self.func_check(function):

            x = Symbol('x')

            try:
                lim = limit(function, x, point)
            except BaseException:
                return 0

            lim = str(lim)

            #if lim[0] == '<':
             #   return 0

            x = -area

            while x < area:

                Ex.append(x)
                x += step

                if str(lim) == 'oo' or str(lim) == '-oo' or str(lim).find('<') != -1 :
                    if e1_exec:
                        if e1 <= 0:
                            e1_exec = False
                        Ey1.append(float(10 + e1))
                        Ey.append(float(10 - e1))
                    if e2_exec:
                        if e2 <= 0:
                            e2_exec = False
                        Ey2.append(float(10 - e2))
                        Ey3.append(float(10 + e2))
                    if e3_exec:
                        if e3 <= 0:
                            e3_exec = False
                        Ey4.append(float(10 + e3))
                        Ey5.append(float(10 + e3))
                else:
                    if e1_exec:
                        Ey.append(float(float(lim) - e1))
                        Ey1.append(float(float(lim) + e1))
                    if e2_exec:
                        Ey2.append(float(float(lim) + e2))
                        Ey3.append(float(float(lim) + e2))
                    if e3_exec:
                        Ey4.append(float(float(lim) + e3))
                        Ey5.append(float(float(lim) + e3))

            if e1_exec:
                self.dataEx = Ex
                self.dataEy = Ey
                self.dataEy1 = Ey1

                self.graphicsView.plot(self.dataEx, self.dataEy, pen=(3, 3))
                self.graphicsView.plot(self.dataEx, self.dataEy1, pen=(3, 3))

            if e2_exec:
                self.dataEx = Ex
                self.dataEy = Ey2
                self.dataEy1 = Ey3

                self.graphicsView.plot(self.dataEx, self.dataEy, pen=(3, 3))
                self.graphicsView.plot(self.dataEx, self.dataEy1, pen=(3, 3))

            if e3_exec:
                self.dataEx = Ex
                self.dataEy = Ey4
                self.dataEy1 = Ey5

                self.graphicsView.plot(self.dataEx, self.dataEy, pen=(3, 3))
                self.graphicsView.plot(self.dataEx, self.dataEy1, pen=(3, 3))

    def clean_all_functions(self, exec):

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