import sys
import requests
import json
import datetime

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from .ui.server_test import Ui_serverTest
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

app_name = "server_test"
app_config: dict = lcfg.config["apps"][app_name]

class ServerTestExperiment(QMainWindow, Ui_serverTest):
    def __init__(self, lcfg: LabConfig, lstat: LabStat, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.lcfg = lcfg
        self.lstat = lstat

        update_config = self.lcfg.update_config
        config = lcfg.config["apps"][app_name]

        self.host = config["Host"]
        self.port = config["Port"]
        self.command = config["Command"]

        self.hostEdit.setText(self.host)
        self.portEdit.setText(str(self.port))
        self.cmdEdit.setText(self.command)
       
        self.resWidget.setReadOnly(True)
        self.sendButton.clicked.connect(self.sendCmd)

        @update_config
        def setHost():
            host = self.hostEdit.text()
            self.host = host
            self.lcfg.config["apps"][app_name]["Host"] = self.host

        self.hostEdit.editingFinished.connect(setHost)

        @update_config
        def setPort():
            port = self.portEdit.text()
            self.port = int(port)
            self.lcfg.config["apps"][app_name]["Port"] = self.port

        self.portEdit.editingFinished.connect(setPort)

        @update_config
        def setCommand():
            command = self.cmdEdit.text()
            self.command = command
            self.lcfg.config["apps"][app_name]["Command"] = self.command

        self.cmdEdit.editingFinished.connect(setCommand)

    def sendCmd(self):
        try:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            self.resWidget.append(f"[{time}] Sending: http://{self.host}:{self.port}/{self.command}")
            QApplication.processEvents()
            response = requests.get(f"http://{self.host}:{self.port}/{self.command}")
            rc = response.content.decode()
            if json.loads(rc)["success"]:
                time = datetime.datetime.now().strftime("%H:%M:%S")
                self.resWidget.append(f"[{time}] Response:")
                for key, value in json.loads(rc).items():
                    self.resWidget.append(f"{key}: {value}")
            else:
                time = datetime.datetime.now().strftime("%H:%M:%S")
                self.resWidget.append(f"[{time}] Failed.")
            self.resWidget.append(" ")
            QApplication.processEvents()
        except requests.exceptions.ConnectionError as err:
            print(err)

if __name__ == "mainWindow":
    STMBoxcar = QApplication(sys.argv)
    mainWindow = ServerTestExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.show()
    sys.exit(STMBoxcar.exec())
else:
    def app_run():
        STMBoxcar = QApplication(sys.argv)
        mainWindow = ServerTestExperiment(lcfg=lcfg, lstat=lstat)
        mainWindow.show()
        sys.exit(STMBoxcar.exec())

    mainWindow = ServerTestExperiment(lcfg=lcfg, lstat=lstat)