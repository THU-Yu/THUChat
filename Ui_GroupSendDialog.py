# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\2019秋季学期（三上）\2019秋计算机网络及应用\HW1 big\GroupSendDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GroupSendDialog(object):
    def setupUi(self, GroupSendDialog):
        GroupSendDialog.setObjectName("GroupSendDialog")
        GroupSendDialog.resize(623, 239)
        self.gridLayout = QtWidgets.QGridLayout(GroupSendDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(GroupSendDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FriendListView = QtWidgets.QListView(GroupSendDialog)
        self.FriendListView.setObjectName("FriendListView")
        self.horizontalLayout.addWidget(self.FriendListView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.AddButton = QtWidgets.QPushButton(GroupSendDialog)
        self.AddButton.setObjectName("AddButton")
        self.verticalLayout.addWidget(self.AddButton)
        self.SubButton = QtWidgets.QPushButton(GroupSendDialog)
        self.SubButton.setObjectName("SubButton")
        self.verticalLayout.addWidget(self.SubButton)
        self.pushButton = QtWidgets.QPushButton(GroupSendDialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.ChooseListView = QtWidgets.QListView(GroupSendDialog)
        self.ChooseListView.setObjectName("ChooseListView")
        self.horizontalLayout.addWidget(self.ChooseListView)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(GroupSendDialog)
        QtCore.QMetaObject.connectSlotsByName(GroupSendDialog)

    def retranslateUi(self, GroupSendDialog):
        _translate = QtCore.QCoreApplication.translate
        GroupSendDialog.setWindowTitle(_translate("GroupSendDialog", "Dialog"))
        self.label.setText(_translate("GroupSendDialog", "选择好友进行群聊"))
        self.AddButton.setText(_translate("GroupSendDialog", ">>"))
        self.SubButton.setText(_translate("GroupSendDialog", "<<"))
        self.pushButton.setText(_translate("GroupSendDialog", "确定"))

