import importlib
from threading import Thread
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont

class AppButton(QPushButton):
    def __init__(self, app_name:str, parent=None):
        self.app = importlib.import_module(f"apps.{app_name}.main")
        QPushButton.__init__(self,parent)
        self.clicked.connect(lambda : self.app_run())
        self.setText(app_name)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)

    def app_run(self):
        try:
            self.app.mainWindow.show()
        except:
            print("Error")