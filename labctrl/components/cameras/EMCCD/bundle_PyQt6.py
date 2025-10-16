from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from .remote import RemoteEMCCD
from .utils import ignore_connection_error

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget
from .bundle_widget import Ui_EMCCD
from labctrl.widgets.canvas import CanvasWidget

import os
import numpy as np

class BundlePyQt6EMCCD(QWidget, Ui_EMCCD):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat, parent=None) -> None:
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.config: dict = bundle_config["Config"]
        self.name = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat

        update_config = self.lcfg.update_config  # Alias for easier access
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        self.remote = RemoteEMCCD(config)

        # UI setup
        self.lineEdit.setText(config["FileName"])
        self.canvas = CanvasWidget(ax_num=1, xlabel="Wavelength (nm))", ylabel=["Intensity"])
        hbox = QtWidgets.QHBoxLayout(self.widget)
        hbox.addWidget(self.canvas)
        self.pushButton_3.clicked.connect(lambda : self.close())
        self.pushButton_2.clicked.connect(lambda : self.clean())
        self.pushButton_1.clicked.connect(lambda : self.acquire())
        self.pushButton_4.clicked.connect(lambda : self.open_save_data())
        self.pushButton_5.clicked.connect(lambda: self.open_raw())

        @update_config
        def __set_filename():
            filename = self.lineEdit.text()
            config["FileName"] = filename

        self.lineEdit.editingFinished.connect(__set_filename)

    @ignore_connection_error
    def close(self):
        response = self.remote.close()
        self.lstat.fmtmsg(response)

    @ignore_connection_error
    def clean(self):
        response = self.remote.clean_count()
        self.lstat.fmtmsg(response)

    @ignore_connection_error
    def reset(self):
        response = self.remote.reset()
        self.lstat.fmtmsg(response)

    @ignore_connection_error
    def acquire(self):
        filename = self.lineEdit.text()
        response = self.remote.acquire(filename)
        self.lstat.fmtmsg(response)
        filepath = response["save_path"] + "\\" + response["filename"]
        data = np.loadtxt(filepath, delimiter=',')
        # print(data)
        self.canvas.update_plot(data[:,0],data[:,1])
        return data[:,1]

    def open_save_data(self):
        os.startfile(os.getcwd()+r"\acq_data")

    def open_raw(self):
        os.startfile(os.getcwd() + r"\servers\cameras\EMCCD\raw")



