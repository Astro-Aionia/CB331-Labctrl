import numpy as np
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from .remote import ProxiedTOPAS

from PyQt6.QtWidgets import QWidget
from .bundle_widget import Ui_TOPASDemo

class BundlePyQt6TOPAS(QWidget, Ui_TOPASDemo):
    def __init__(self,bundle_config: dict, lcfg: LabConfig, lstat: LabStat, parent=None):
        QWidget.__init__(self,parent=parent)
        self.config: dict = bundle_config["Config"]
        self.name = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat

        update_config = self.lcfg.update_config  # Alias for easier access
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        self.remote = ProxiedTOPAS(config)
        self.update_scanlist(config)

        # UI setup and initialize parameters
        self.setupUi(self)
        self.comboBox.setCurrentText(config["ManualInteraction"])
        self.lineEdit_1.setText(str(config["ManualTarget"]))
        self.lineEdit_2.setText(str(config["RangeScanStart"]))
        self.lineEdit_3.setText(str(config["RangeScanStop"]))
        self.lineEdit_4.setText(str(config["RangeScanStep"]))

        self.pushButton.clicked.connect(lambda : self.change_shutter())

        @update_config
        def __set_wavelength():
            interation = self.comboBox.currentText()
            wavelength = self.lineEdit_1.text()
            response = self.remote.set_wavelength(interation, wavelength)
            config["ManualTarget"] = wavelength
            config["ManualInteraction"] = interation
            self.lstat.fmtmsg(response)

        self.lineEdit_1.editingFinished.connect(__set_wavelength)

        def __set_scanlist():
            config["RangeScanStart"] = float(self.lineEdit_2.text())
            config["RangeScanStop"] = float(self.lineEdit_3.text())
            config["RangeScanStep"] = float(self.lineEdit_4.text())
            self.update_scanlist(config)

        self.lineEdit_2.editingFinished.connect(__set_scanlist)
        self.lineEdit_3.editingFinished.connect(__set_scanlist)
        self.lineEdit_4.editingFinished.connect(__set_scanlist)

    def change_shutter(self):
        name = self.name
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        response = self.remote.change_shutter()
        self.lstat.fmtmsg(response)
        self.lstat.stat[name]["ShutterIsOpen"] = response["shutterIsOpen"]
        self.lstat.dump_stat("last_stat.json")

    def update_scanlist(self, config) -> list:
        name = config["Name"]
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        self.lstat.stat[name]["ScanList"] = np.arange(config["RangeScanStart"], config["RangeScanStop"], config["RangeScanStep"]).tolist()
        self.lstat.dump_stat("last_stat.json")
        return self.lstat.stat[name]["ScanList"]