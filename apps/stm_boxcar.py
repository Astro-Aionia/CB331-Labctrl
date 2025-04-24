import sys
import json
import requests

from setuptools.sandbox import save_path

sys.path.append('..')

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from apps.ui.stm_boxcar import Ui_STMBoxcar

from widgets.servo_manual_control import ServoManualControlWidget

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(1, 1, 1)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

class STMBoxcarExperiment(Ui_STMBoxcar, QMainWindow):
    def __init__(self, parent=None):
        # components
        self.servo = ServoManualControlWidget()
        self.boxcar_url = "http://127.0.0.1:50008"
        # ui
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        manual = QtWidgets.QVBoxLayout(self.widget)
        manual.addWidget(self.servo)
        self.scan_window = MplCanvas()
        self.scan_toolbox = NavigationToolbar(self.scan_window)
        scan_window = QtWidgets.QVBoxLayout(self.widget_2)
        scan_window.addWidget(self.scan_toolbox)
        scan_window.addWidget(self.scan_window)
        # animation
        self.x = []
        self.y = []
        # self.ani = FuncAnimation(self.scan_window.figure, self.update_plot, interval=10)
        # functions
        self.lineEdit.setText("..\\delaylist\\delay.txt")
        self.lineEdit_2.setText("delay.csv")
        self.lineEdit_3.setText("0")
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setText("1")
        self.pushButton.clicked.connect(lambda : self.scan())

    def scan(self):
        delaylistfile = self.lineEdit.text()
        round = int(self.lineEdit_4.text())
        # print(delaylistfile)
        save_path = "..\\acq_data\\"
        filename = self.lineEdit_2.text()
        # print(save_path)
        delaylist = np.loadtxt(delaylistfile)
        for i in range(round):
            self.lineEdit_3.setText(str(i))
            self.x = []
            self.y = []
            for position in delaylist:
                self.servo.lineEdit_4.setText(str(position))
                self.servo.moveabs()
                self.textEdit.append(self.servo.last_response["message"])
                res = requests.get(self.boxcar_url + "/get_value")
                rc = res.content.decode()
                value = json.loads(rc)["value"]
                # message = json.loads(rc)["message"]
                self.textEdit.append(f"get data at position {position} mm.")
                self.x.append(position)
                self.y.append(value)
                self.update_plot()
                QApplication.processEvents()
            np.savetxt(save_path+filename+"Round"+str(i).zfill(5)+".csv", np.vstack((self.x, self.y)).T, delimiter=',')
            self.textEdit.append("File saved at "+save_path+filename+'.')

    def update_plot(self):
        self.scan_window.ax.clear()
        self.scan_window.ax.plot(self.x, self.y)
        self.scan_window.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = STMBoxcarExperiment()
    mainWindow.show()
    sys.exit(app.exec())