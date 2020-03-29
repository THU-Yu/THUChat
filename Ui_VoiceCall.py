# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\2019秋季学期（三上）\2019秋计算机网络及应用\HW1 big\VoiceCall.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VoiceCallDialog(object):
    def setupUi(self, VoiceCallDialog):
        VoiceCallDialog.setObjectName("VoiceCallDialog")
        VoiceCallDialog.resize(233, 309)
        self.gridLayout = QtWidgets.QGridLayout(VoiceCallDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(VoiceCallDialog)
        font = QtGui.QFont()
        font.setFamily("Pristina")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.UserNameLabel = QtWidgets.QLabel(VoiceCallDialog)
        self.UserNameLabel.setText("")
        self.UserNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.UserNameLabel.setObjectName("UserNameLabel")
        self.gridLayout.addWidget(self.UserNameLabel, 1, 0, 1, 1)
        self.AcceptButton = QtWidgets.QPushButton(VoiceCallDialog)
        self.AcceptButton.setObjectName("AcceptButton")
        self.gridLayout.addWidget(self.AcceptButton, 2, 0, 1, 1)
        self.RefuseButton = QtWidgets.QPushButton(VoiceCallDialog)
        self.RefuseButton.setObjectName("RefuseButton")
        self.gridLayout.addWidget(self.RefuseButton, 3, 0, 1, 1)

        self.retranslateUi(VoiceCallDialog)
        QtCore.QMetaObject.connectSlotsByName(VoiceCallDialog)

    def retranslateUi(self, VoiceCallDialog):
        _translate = QtCore.QCoreApplication.translate
        VoiceCallDialog.setWindowTitle(_translate("VoiceCallDialog", "Dialog"))
        self.label.setText(_translate("VoiceCallDialog", "DAChat"))
        self.AcceptButton.setText(_translate("VoiceCallDialog", "接听"))
        self.RefuseButton.setText(_translate("VoiceCallDialog", "拒绝"))

