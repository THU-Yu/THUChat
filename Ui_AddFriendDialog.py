# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\2019秋季学期（三上）\2019秋计算机网络及应用\HW1 big\AddFriendDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddFriendDialog(object):
    def setupUi(self, AddFriendDialog):
        AddFriendDialog.setObjectName("AddFriendDialog")
        AddFriendDialog.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(AddFriendDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.RequestListView = QtWidgets.QListView(AddFriendDialog)
        self.RequestListView.setObjectName("RequestListView")
        self.gridLayout.addWidget(self.RequestListView, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(AddFriendDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.AcceptButton = QtWidgets.QPushButton(AddFriendDialog)
        self.AcceptButton.setObjectName("AcceptButton")
        self.verticalLayout.addWidget(self.AcceptButton)
        self.RefuseButton = QtWidgets.QPushButton(AddFriendDialog)
        self.RefuseButton.setObjectName("RefuseButton")
        self.verticalLayout.addWidget(self.RefuseButton)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(AddFriendDialog)
        QtCore.QMetaObject.connectSlotsByName(AddFriendDialog)

    def retranslateUi(self, AddFriendDialog):
        _translate = QtCore.QCoreApplication.translate
        AddFriendDialog.setWindowTitle(_translate("AddFriendDialog", "Dialog"))
        self.label.setText(_translate("AddFriendDialog", "添加好友邀请："))
        self.AcceptButton.setText(_translate("AddFriendDialog", "同意"))
        self.RefuseButton.setText(_translate("AddFriendDialog", "拒绝"))

