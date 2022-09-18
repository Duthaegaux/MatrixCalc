from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
import os
import wmi
import numpy

pc = wmi.WMI()

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        fontz = QtGui.QFont("Rubik", 13)
        fontt = QtGui.QFont("Rubik", 11)
        resx, resy = 0, 0

        self.setWindowTitle("MatrixCalc")
        for i in pc.Win32_VideoController():
            resx = i.CurrentHorizontalResolution
            resy = i.CurrentVerticalResolution
            break
        self.setGeometry((resx - 345) // 2, (resy - 286) // 2, 345, 286)
        self.setFixedSize(345, 286)
        self.setWindowIcon(QtGui.QIcon(resource_path("mxcalc.ico")))

        self.mx1 = QtWidgets.QPlainTextEdit(self)
        self.mx1.setGeometry(27, 10, 128, 128)

        self.mx2 = QtWidgets.QPlainTextEdit(self)
        self.mx2.setGeometry(27, 148, 128, 128)

        self.zn1 = QtWidgets.QLabel(self)
        self.zn1.setFont(fontz)
        self.zn1.setGeometry(10, 67, 30, 15)

        self.zn2 = QtWidgets.QLabel(self)
        self.zn2.setFont(fontz)
        self.zn2.setGeometry(10, 207, 30, 15)

        self.plbtn = QtWidgets.QPushButton(self)
        self.plbtn.setText("+")
        self.plbtn.setFont(fontz)
        self.plbtn.setGeometry(0, 0, 50, 50)
        self.plbtn.move(165, 10)
        self.plbtn.clicked.connect(lambda: self.plus(self.mx1, self.mx2))

        self.mnbtn = QtWidgets.QPushButton(self)
        self.mnbtn.setText("-")
        self.mnbtn.setFont(fontz)
        self.mnbtn.setGeometry(0, 0, 50, 50)
        self.mnbtn.move(225, 10)
        self.mnbtn.clicked.connect(lambda: self.min(self.mx1, self.mx2))

        self.dtbtn = QtWidgets.QPushButton(self)
        self.dtbtn.setText("det")
        self.dtbtn.setFont(fontt)
        self.dtbtn.setGeometry(0, 0, 50, 50)
        self.dtbtn.move(285, 10)
        self.dtbtn.clicked.connect(lambda: self.det(self.mx1, self.mx2))

        self.pwbtn = QtWidgets.QPushButton(self)
        self.pwbtn.setText("*")
        self.pwbtn.setFont(fontz)
        self.pwbtn.setGeometry(0, 0, 50, 50)
        self.pwbtn.move(165, 70)
        self.pwbtn.clicked.connect(lambda: self.pow(self.mx1, self.mx2))

        self.dlbtn = QtWidgets.QPushButton(self)
        self.dlbtn.setText("/")
        self.dlbtn.setFont(fontz)
        self.dlbtn.setGeometry(0, 0, 50, 50)
        self.dlbtn.move(225, 70)
        self.dlbtn.clicked.connect(lambda: self.div(self.mx1, self.mx2))

        self.sinbtn = QtWidgets.QPushButton(self)
        self.sinbtn.setText("sin")
        self.sinbtn.setFont(fontt)
        self.sinbtn.setGeometry(0, 0, 50, 50)
        self.sinbtn.move(285, 70)
        self.sinbtn.clicked.connect(lambda: self.sin(self.mx1, self.mx2))

        self.adpbtn = QtWidgets.QPushButton(self)
        self.adpbtn.setText("adp")
        self.adpbtn.setFont(fontt)
        self.adpbtn.setGeometry(0, 0, 80, 50)
        self.adpbtn.move(165, 130)
        self.adpbtn.clicked.connect(lambda: self.adp(self.mx1, self.mx2))

        self.clnbtn = QtWidgets.QPushButton(self)
        self.clnbtn.setText("clean")
        self.clnbtn.setFont(fontt)
        self.clnbtn.setGeometry(0, 0, 80, 50)
        self.clnbtn.move(255, 130)
        self.clnbtn.clicked.connect(lambda: self.clean())

    def rcr(self, matrix):
        c = 0
        rdmx = []
        zn = []
        mxnp = matrix.toPlainText()
        for i in mxnp:
            if i == "\n":
                if len(zn) != 0:
                    c1 = zn[-1]
                    zn.append(c)
                    rdmx.append(list(mxnp[c1:c].split()))
                else:
                    zn.append(c)
                    rdmx.append(list(mxnp[:c].split()))
            c += 1
        if mxnp[-1] != "\n":
            rdmx.append(list(mxnp[zn[-1]:].split()))
        try:
            for i in rdmx:
                for x in range(len(i)):
                    i[x] = int(i[x])
            rdmx = numpy.array(rdmx)
            return rdmx
        except:
            return rdmx

    def nprcr(self, matrix):
        c = 0
        rdmx = ""
        matrix = list(matrix)
        for i in range(len(matrix)):
            matrix[i] = list(matrix[i])
        for i in matrix:
            for x in i:
                c += 1
                if c != len(i):
                    rdmx += f"{x} "
                else:
                    rdmx += f"{x}\n"
            c = 0
        return rdmx

    def det(self, mx1, mx2):
        try:
            if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText(f"{numpy.linalg.det(self.rcr(mx1))}")
                self.mx2.setPlainText(f"{numpy.linalg.det(self.rcr(mx2))}")
            elif len(mx1.toPlainText()) != 0:
                self.mx1.setPlainText(f"{numpy.linalg.det(self.rcr(mx1))}")
            elif len(mx2.toPlainText()) != 0:
                self.mx2.setPlainText(f"{numpy.linalg.det(self.rcr(mx2))}")
        except:
            self.mx1.setPlainText("Error")
            self.mx2.setPlainText("Matrix must be square")

    def sin(self, mx1, mx2):
        try:
            if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
                if numpy.linalg.det(self.rcr(mx1)) != 0:
                    self.mx1.setPlainText("False")
                else:
                    self.mx1.setPlainText("True")
                if numpy.linalg.det(self.rcr(mx2)) != 0:
                    self.mx2.setPlainText("False")
                else:
                    self.mx2.setPlainText("True")
            elif len(mx1.toPlainText()) != 0:
                if numpy.linalg.det(self.rcr(mx1)) != 0:
                    self.mx1.setPlainText("False")
                else:
                    self.mx1.setPlainText("True")
            elif len(mx2.toPlainText()) != 0:
                if numpy.linalg.det(self.rcr(mx2)) != 0:
                    self.mx2.setPlainText("False")
                else:
                    self.mx2.setPlainText("True")
        except:
            self.mx1.setPlainText("Error")
            self.mx2.setPlainText("Maybe matrix must be square.")

    def plus(self, mx1, mx2):
        try:
            if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText(f"{self.nprcr(self.rcr(mx1) + self.rcr(mx2))}")
                self.mx2.setPlainText("")
            elif len(mx1.toPlainText()) != 0:
                self.mx1.setPlainText("")
                self.mx2.setPlainText("Matrix must be filled!")
            elif len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText("Matrix must be filled!")
                self.mx2.setPlainText("")
        except:
            self.mx1.setPlainText("Error")
            self.mx2.setPlainText("Try read matrix rules.")

    def min(self, mx1, mx2):
        try:
            if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText(f"{self.nprcr(self.rcr(mx1) - self.rcr(mx2))}")
                self.mx2.setPlainText("")
            elif len(mx1.toPlainText()) != 0:
                self.mx1.setPlainText("")
                self.mx2.setPlainText("Matrix must be filled!")
            elif len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText("Matrix must be filled!")
                self.mx2.setPlainText("")
        except:
            self.mx1.setPlainText("Error")
            self.mx2.setPlainText("Try read matrix rules.")

    def pow(self, mx1, mx2):
        try:
            if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText(f"{self.nprcr(self.rcr(mx1).dot(self.rcr(mx2)))}")
                self.mx2.setPlainText("")
            elif len(mx1.toPlainText()) != 0:
                self.mx1.setPlainText("")
                self.mx2.setPlainText("Matrix must be filled!")
            elif len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText("Matrix must be filled!")
                self.mx2.setPlainText("")
        except:
            self.mx1.setPlainText("Error")
            self.mx2.setPlainText("Number of columns in the first matrix must be equal to the number of rows in the second matrix.")

    def adp(self, mx1, mx2):
        if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
            crd = self.fr(mx1)
            i = crd[0]
            j = crd[1]
            crd = self.fr(mx2)
            i1 = crd[0]
            j1 = crd[1]
        elif len(mx1.toPlainText()) != 0:
            crd = self.fr(mx1)
            i = crd[0]
            j = crd[1]
        elif len(mx2.toPlainText()) != 0:
            crd = self.fr(mx2)
            i1 = crd[0]
            j1 = crd[1]
        try:
            if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
                self.ard(self.mx1, i, j, self.zn1)
                self.ard(self.mx2, i1, j1, self.zn2)
            elif len(mx1.toPlainText()) != 0:
                self.ard(self.mx1, i, j, self.zn1)
            elif len(mx2.toPlainText()) != 0:
                self.ard(self.mx2, i1, j1, self.zn2)
        except:
            self.mx1.setPlainText("Error")
            self.mx2.setPlainText("Try to point wheres adp using letters or symbols")

    def div(self, mx1, mx2):
        try:
            if len(mx1.toPlainText()) != 0 and len(mx2.toPlainText()) != 0:
                imx2 = numpy.linalg.inv(self.rcr(mx2))
                mx2.setPlainText(self.nprcr(numpy.around(imx2.dot(self.rcr(mx1)), decimals=2)))
                mx1.setPlainText(self.nprcr(numpy.around(self.rcr(mx1).dot(imx2), decimals=2)))
            elif len(mx1.toPlainText()) != 0:
                self.mx1.setPlainText("")
                self.mx2.setPlainText("Matrix must be filled!")
            elif len(mx2.toPlainText()) != 0:
                self.mx1.setPlainText("Matrix must be filled!")
                self.mx2.setPlainText("")
        except:
            self.mx1.setPlainText("Error")
            self.mx2.setPlainText("Try read matrix rules.")

    def clean(self):
        self.mx1.setPlainText("")
        self.mx2.setPlainText("")
        self.zn1.setText("")
        self.zn2.setText("")

    def cut(self, matrix, i, j):
        return numpy.delete(numpy.delete(matrix, i, axis=0), j, axis=1)

    def fr(self, mx):
        ex = 0
        i, j = 0, 0
        for f in self.rcr(mx):
            i = 0
            for x in f:
                try:
                    x = int(x)
                    i += 1
                except:
                    ex = 1
                    break
            if ex == 1:
                break
            j += 1
        return i, j

    def ard(self, mx, i, j, zn):
        zn1 = pow(-1, i + j)
        if zn1 == -1:
            zn.setText("-")
        mn = self.cut(self.rcr(mx), j, i)
        mx.setPlainText(self.nprcr(mn))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    application()
