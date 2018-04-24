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

exdots ={}
eydots = {}
ey1dots = {}

functions_list = []

i = 0

edit = false

function_e = " "

amount = 5

instructions='  **     to power \n ' \
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
        self.grid.addWidget(self.delete_button, 2, 1)

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 6, 0, 7, 0)

        self.graphics = QComboBox(self.centralwidget)
        self.graphics.setObjectName("graphics")
        self.grid.addWidget(self.graphics, 2, 0)
        self.graphics.addItem(" ")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 662, 21))
        self.menubar.setObjectName("menubar")

        self.limits_view = self.menubar.addMenu('Limits')
        limits_action=QAction(MainWindow)
        limits_action.triggered.connect(self.open_limits)
        self.limits_view.addAction(limits_action)

        MainWindow.setMenuBar(self.menubar)

        self.derivatives_view = self.menubar.addMenu('Derivatives')
        derivatives_action = QAction(MainWindow)
        derivatives_action.triggered.connect(self.open_derivatives)
        self.derivatives_view.addAction(derivatives_action)

        self.instructions_view = self.menubar.addMenu('Instructions')
        instructions_action= QAction(MainWindow)
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

        global i

        j = functions_list.index(function_e)
        self.graphics.removeItem(i+1)
        del xdots[str(i)]
        del ydots[str(i)]

        for items in xdots:
          self.dataX = xdots.get(str(items))
          self.dataY = ydots.get(str(items))

          self.graphicsView.setYRange(-10, 10)
          self.graphicsView.setXRange(-10, 10)
          c = randint(1, 10)
          self.graphicsView.plot(self.dataX, self.dataY, pen=(i, 3))

    def clean_all(self,exec):
        if exec == 1:
            self.result.close()
            self.delta.close()
            self.function_enter.close()
            self.point_enter.close()
            self.epsilon_enter.close()
            self.epsilon_button.close()
            self.clean_all_button.close()
            self.graphicsView.close()
            self.save_button.close()
            self.delete_button.close()
            self.graphics.close()

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
        self.clean_all()

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

        self.delete_button = QPushButton(self.centralwidget)
        self.delete_button.setObjectName("pushButton")
        self.grid.addWidget(self.delete_button, 2, 1)

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 6, 0, 7, 0)

        self.graphics = QComboBox(self.centralwidget)
        self.graphics.setObjectName("graphics")
        self.grid.addWidget(self.graphics, 2, 0)
        self.graphics.addItem(" ")

        self.retranslateUi(MainWindow)

    def open_derivatives(self):
        self.clean_all(1)

        self.function_enter = QLineEdit(self.centralwidget)
        self.function_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.function_enter, 1, 0)
        self.function_enter.textChanged.connect(self.draw)

        self.delta_enter = QLineEdit(self.centralwidget)
        self.delta_enter.setObjectName("lineEdit")
        self.grid.addWidget(self.delta_enter, 1, 1)

        self.draw_tangent = QPushButton(self.centralwidget)
        self.draw_tangent.setObjectName("pushButton")
        self.grid.addWidget(self.draw_tangent, 2, 0)
        self.draw_tangent.setText("Tangent")
        self.draw_tangent.clicked.connect(self.drawtan)

        self.draw_additional = QPushButton(self.centralwidget)
        self.draw_additional.setObjectName("pushButton")
        self.grid.addWidget(self.draw_additional, 2, 1)
        self.draw_additional.setText("Additional")

        self.draw_df = QPushButton(self.centralwidget)
        self.draw_df.setObjectName("pushButton")
        self.grid.addWidget(self.draw_df, 2, 2)
        self.draw_df.setText("df")

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.grid.addWidget(self.graphicsView, 3, 0, 7, 0)

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

            lim = str(lim)

            if lim[0] == '<':
                lim = " Not exist"

            self.result.setText("lim = " + str(lim))

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

    def drawtan(self):
        print("kek")

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

            lim = str(lim)

            if lim[0] == '<':
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

                exdots.update({str(i): Ex})
                eydots.update({str(i): Ey})
                ey1dots.update({str(i): Ey1})

            self.dataEx = exdots.get(str(i))
            self.dataEy = eydots.get(str(i))
            self.dataEy1 = ey1dots.get(str(i))

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