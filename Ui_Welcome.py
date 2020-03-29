# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\2019秋季学期（三上）\2019秋计算机网络及应用\HW1 big\Welcome.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 210, 71, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 210, 71, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 100, 51, 21))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(90, 160, 51, 21))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 10, 261, 61))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(21)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Username = QtWidgets.QLineEdit(Dialog)
        self.Username.setGeometry(QtCore.QRect(150, 100, 131, 31))
        self.Username.setObjectName("Username")
        self.Password = QtWidgets.QLineEdit(Dialog)
        self.Password.setGeometry(QtCore.QRect(150, 150, 131, 31))
        self.Password.setObjectName("Password")
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_2.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label.raise_()
        self.pushButton.raise_()
        self.Username.raise_()
        self.Password.raise_()

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.Login)
        self.pushButton_2.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Welcome"))
        self.pushButton.setText(_translate("Dialog", "登入"))
        self.pushButton_2.setText(_translate("Dialog", "离开"))
        self.label_2.setText(_translate("Dialog", "账户："))
        self.label_3.setText(_translate("Dialog", "密码："))
        self.label.setText(_translate("Dialog", "DAChat"))
