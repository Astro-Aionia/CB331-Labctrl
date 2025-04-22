import sys
import json
import requests

import numpy
import matplotlib
from click import command

matplotlib.use('Qt5Agg')
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from widgets.ui.boxcar_preveiw import Ui_BoxcarPreview

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.set_xlabel('Wavelength')
        plt.tight_layout()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

class BoxcarPreviewWidget(QWidget, Ui_BoxcarPreview):
    def __init__(self, parent=None):
        self.last_response = None
        # server
        self.url = "http://127.0.0.1:50008"
        # init setup
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.data_canvas = MplCanvas()
        self.toolbox = NavigationToolbar(self.data_canvas)
        mpl_wid = QtWidgets.QVBoxLayout(self.widget)
        mpl_wid.addWidget(self.toolbox)
        mpl_wid.addWidget(self.data_canvas)
        self.pushButton.clicked.connect(lambda: self.get_data())

    def get_request(self, command):
        try:
            print(self.url + command)
            res = requests.get(self.url + command)
            rc = res.content.decode()
            self.last_response = json.loads(rc)
            return json.loads(rc)
        except requests.exceptions.ConnectionError as err:
            print(err)
            return None

    def get_data(self):
        command = "/get_data"
        self.get_request(command)
        # print(self.last_response["data"])
        self.data_canvas.ax.clear()
        self.data_canvas.ax.plot(self.last_response["data"])
        self.data_canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = BoxcarPreviewWidget()
    mainWindow.show()
    sys.exit(app.exec())