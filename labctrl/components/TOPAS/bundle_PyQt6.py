import time

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
        self.comboBox_1.setCurrentText(config["ManualInteraction"])
        self.comboBox_2.setCurrentText(config["ScanMode"])
        self.lineEdit_1.setText(str(config["ManualTarget"]))
        self.lineEdit_2.setText(str(config["RangeScanStart"]))
        self.lineEdit_3.setText(str(config["RangeScanStop"]))
        self.lineEdit_4.setText(str(config["RangeScanStep"]))

        self.pushButton.clicked.connect(lambda : self.shutter_switch())

        @update_config
        def __set_wavelength():
            interation = self.comboBox_1.currentText()
            wavelength = self.lineEdit_1.text()
            response = self.remote.set_wavelength(interation, wavelength)
            config["ManualTarget"] = wavelength
            config["ManualInteraction"] = interation
            self.lstat.fmtmsg(response)

        self.lineEdit_1.editingFinished.connect(__set_wavelength)

        def __set_scan_mode():
            config["ScanMode"] = self.comboBox_2.currentText()
            self.update_scanlist(config)

        self.comboBox_2.currentTextChanged.connect(__set_scan_mode)

        def __set_scanlist():
            config["RangeScanStart"] = float(self.lineEdit_2.text())
            config["RangeScanStop"] = float(self.lineEdit_3.text())
            config["RangeScanStep"] = float(self.lineEdit_4.text())
            self.update_scanlist(config)

        self.lineEdit_2.editingFinished.connect(__set_scanlist)
        self.lineEdit_3.editingFinished.connect(__set_scanlist)
        self.lineEdit_4.editingFinished.connect(__set_scanlist)

        def scan_range(func, meta=''):
            """
            decorator, when applied to func, scan range for func.
            adds or alters the following meta params:
                meta[name]["PumpWavelength"] : str or float, current wavelength
                meta[name]["iPumpWavelength"]: int, index of current wavelength
            """

            def iterate(meta=dict()):
                if config["ScanMode"] == "Range":
                    wvlist = self.lstat.stat[name]["ScanList"]
                    interation = self.comboBox_1.currentText()
                    for i, wv in enumerate(wvlist):
                        if meta["TERMINATE"]:
                            self.lstat.expmsg(
                                "[{name}][scan_range] Received signal TERMINATE, trying graceful Thread exit".format(name=name))
                            break
                        response = self.remote.set_wavelength(interation, wv)
                        self.lstat.fmtmsg(response)
                        self.lstat.stat[name]["PumpWavelength"] = wv
                        self.lstat.stat[name]["iPumpWavelength"] = i
                        func(meta=meta)
                else:
                    self.lstat.expmsg(
                        "[{name}][scan_range] Range is set manually, so no action has been taken".format(name=name))
                    self.lstat.stat[name]["PumpWavelength"] = config["ManualTarget"]
                    self.lstat.stat[name]["iPumpWavelength"] = 0
                    func(meta=meta)

            return iterate

        self.scan_range = scan_range

        def shutter_swich_acquire(func,  meta=''):
            """
            decorator, when applied to func, running func twice with and without pump from this TOPAS.
            """

            def iterate(meta=dict()):
                self.shutter_close()
                time.sleep(0.5)
                lstat.expmsg("Now taking the background...")
                func(meta=meta)
                self.shutter_open()
                time.sleep(0.5)
                lstat.expmsg("Now taking the signal...")
                func(meta=meta)
            return iterate

        self.shutter_swich_acquire = shutter_swich_acquire

    def shutter_switch(self):
        name = self.name
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        response = self.remote.change_shutter()
        self.lstat.fmtmsg(response)
        self.lstat.stat[name]["ShutterIsOpen"] = response["shutterIsOpen"]
        self.lstat.dump_stat("last_stat.json")

    def shutter_close(self):
        name = self.name
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        if self.lstat.stat[name]["ShutterIsOpen"]:
            response = self.remote.change_shutter()
            self.lstat.fmtmsg(response)
            self.lstat.stat[name]["ShutterIsOpen"] = response["shutterIsOpen"]
            self.lstat.dump_stat("last_stat.json")

    def shutter_open(self):
        name = self.name
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        if not self.lstat.stat[name]["ShutterIsOpen"]:
            response = self.remote.change_shutter()
            self.lstat.fmtmsg(response)
            self.lstat.stat[name]["ShutterIsOpen"] = response["shutterIsOpen"]
            self.lstat.dump_stat("last_stat.json")

    def update_scanlist(self, config) -> list:
        name = config["Name"]
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        if config["ScanMode"] == "Range":
            self.lstat.stat[name]["ScanList"] = np.arange(config["RangeScanStart"], config["RangeScanStop"], config["RangeScanStep"]).tolist()
        else:
            self.lstat.stat[name]["ScanList"] = [config["ManualTarget"]]
        self.lstat.expmsg("Generated Wavelength Scan List: {}".format(self.lstat.stat[name]["ScanList"]))
        self.lstat.dump_stat("last_stat.json")
        return self.lstat.stat[name]["ScanList"]
