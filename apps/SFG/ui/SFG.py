# Form implementation generated from reading ui file 'SFG.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SFGExperiment(object):
    def setupUi(self, SFGExperiment):
        SFGExperiment.setObjectName("SFGExperiment")
        SFGExperiment.resize(1337, 808)
        self.centralwidget = QtWidgets.QWidget(parent=SFGExperiment)
        self.centralwidget.setObjectName("centralwidget")
        self.StageWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.StageWidget.setGeometry(QtCore.QRect(9, 9, 553, 392))
        self.StageWidget.setObjectName("StageWidget")
        self.MessageWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.MessageWidget.setGeometry(QtCore.QRect(9, 418, 553, 381))
        self.MessageWidget.setObjectName("MessageWidget")
        self.DetectorWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.DetectorWidget.setGeometry(QtCore.QRect(568, 348, 761, 451))
        self.DetectorWidget.setObjectName("DetectorWidget")
        self.TOPASWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.TOPASWidget.setGeometry(QtCore.QRect(570, 10, 751, 330))
        self.TOPASWidget.setObjectName("TOPASWidget")
        self.pushButton_1 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(10, 400, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 400, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        SFGExperiment.setCentralWidget(self.centralwidget)

        self.retranslateUi(SFGExperiment)
        QtCore.QMetaObject.connectSlotsByName(SFGExperiment)

    def retranslateUi(self, SFGExperiment):
        _translate = QtCore.QCoreApplication.translate
        SFGExperiment.setWindowTitle(_translate("SFGExperiment", "SFG"))
        self.pushButton_1.setText(_translate("SFGExperiment", "Start"))
        self.pushButton_2.setText(_translate("SFGExperiment", "Stop"))
