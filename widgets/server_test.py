import sys
import json
import requests
from PyQt6.QtWidgets import QMainWindow, QApplication
from ui.server_test import Ui_MainWindow

class ServerTestWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.get())
        self.lineEdit.setText('50008')
        self.lineEdit_2.setText('/get_data')

    def get(self):
        try:
            host = '127.0.0.1'
            port = int(self.lineEdit.text())
            command = str(self.lineEdit_2.text())
            apicall = f"http://{host}:{port}{command}"
            res = requests.get(apicall)
            rc = res.content.decode()
            self.response_log(rc)
            return json.loads(rc)
        except requests.exceptions.ConnectionError as err:
            print(err)
            self.response_log(str(err))
            return None

    def response_log(self, content):
        self.textEdit.append(content)
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ServerTestWindow()
    mainWindow.show()
    sys.exit(app.exec())