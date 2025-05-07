import sys
import json
import requests
from PyQt6.QtWidgets import QWidget, QApplication
from .ui.servo import Ui_ServoStage

class ServoManualControlWidget(QWidget, Ui_ServoStage):
    def __init__(self, parent=None):
        self.last_response = None
        # server
        self.url = "http://127.0.0.1:50001"
        # init setup
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.lineEdit_1.setText('0')
        self.lineEdit_2.setText('30')
        self.lineEdit_3.setText('0')
        self.lineEdit_4.setText('0')
        # functions
        self.lineEdit_1.setReadOnly(True)
        self.lineEdit_2.editingFinished.connect(lambda: self.set_velocity())
        self.pushButton_1.clicked.connect(lambda: self.movepos())
        self.pushButton_2.clicked.connect(lambda: self.moveneg())
        self.pushButton_3.clicked.connect(lambda: self.moveabs())
        self.pushButton_4.clicked.connect(lambda: self.autohome())

    def get_request(self, command):
        try:
            # print(self.url+command)
            res = requests.get(self.url+command)
            rc = res.content.decode()
            self.last_response = json.loads(rc)
            return json.loads(rc)
        except requests.exceptions.ConnectionError as err:
            print(err)
            return None

    def set_velocity(self):
        vel = float(self.lineEdit_2.text())
        command = f"/set_velocity/{vel}"
        self.get_request(command)

    def update_position(self, res):
        position = res['position']
        self.lineEdit_1.setText(str(position))

    def moveabs(self):
        pos = float(self.lineEdit_4.text())
        command = f"/moveabs/{pos}"
        self.get_request(command)
        self.update_position(self.last_response)

    def movepos(self):
        dis = float(self.lineEdit_3.text())
        command = f"/moveinc/{dis}"
        self.get_request(command)
        self.update_position(self.last_response)

    def moveneg(self):
        dis = -float(self.lineEdit_3.text())
        command = f"/moveinc/{dis}"
        self.get_request(command)
        self.update_position(self.last_response)

    def autohome(self):
        command = "/autohome"
        self.get_request(command)
        self.update_position(self.last_response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ServoManualControlWidget()
    mainWindow.show()
    sys.exit(app.exec())