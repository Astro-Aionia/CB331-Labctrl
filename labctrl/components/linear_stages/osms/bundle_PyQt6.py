import numpy as np
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from .remote import RemoteOSMSStage

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget
from .bundle_widget import Ui_OSMSStage

class BundlePyQt6OSMSStage(QWidget, Ui_OSMSStage):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat, parent = None):
        QWidget.__init__(self, parent=parent)
        self.config: dict = bundle_config["Config"]
        self.name = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat

        update_config = self.lcfg.update_config  # Alias for easier access
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        self.remote = RemoteOSMSStage(config)
        self.update_scanlist(config)

        # UI setup and initialize parameters
        self.setupUi(self)
        self.lineEdit_1.setReadOnly(True)
        self.lineEdit_1.setText("{:.2f}".format(self.config["ManualPosition"]))
        self.lineEdit_2.setText(str(self.config["DrivingSpeed"]))
        self.lineEdit_3.setText("0.0")
        self.lineEdit_4.setText("0.0")
        self.lineEdit_5.setText(str(self.config["RangeScanStart"]))
        self.lineEdit_6.setText(str(self.config["RangeScanStop"]))
        self.lineEdit_7.setText(str(self.config["RangeScanStep"]))
        self.lineEdit_9.setText(str(self.config["ScanRound"]))

        if self.config["ScanMode"] == "Range":
            self.comboBox.setCurrentText("Range")
        else:
            pass

        @update_config
        def __set_velocity():
            config["DrivingSpeed"] = float(self.lineEdit_2.text())
            response = self.remote.set_velocity(config["DrivingSpeed"])
            self.lstat.fmtmsg(response)

        self.lineEdit_2.editingFinished.connect(__set_velocity)

        @update_config
        def __set_zero_point(buttonStatus: bool):
            response = self.remote.set_zero()
            self.lstat.fmtmsg(response)

        self.pushButton_5.clicked.connect(__set_zero_point)

        @update_config
        def __movepos(buttonStatus: bool):
            target_distance = float(self.lineEdit_3.text())
            response = self.remote.moveinc(target_distance)
            config["ManualPosition"] = response["position"]
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_1.clicked.connect(__movepos)

        @update_config
        def __moveneg(buttonStatus: bool):
            target_distance = -float(self.lineEdit_3.text())
            response = self.remote.moveinc(target_distance)
            config["ManualPosition"] = response["position"]
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_2.clicked.connect(__moveneg)

        @update_config
        def __moveabs(buttonStatus: bool):
            config["ManualPosition"] = float(self.lineEdit_4.text())
            response = self.remote.moveabs(config["ManualPosition"])
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_3.clicked.connect(__moveabs)

        @update_config
        def __home(buttonStatus: bool):
            config["ManualPosition"] = 0.0
            response = self.remote.autohome()
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_4.clicked.connect(__home)

        @update_config
        def __set_scan_list(backSignal=None):
            config["RangeScanStart"] = float(self.lineEdit_5.text())
            config["RangeScanStop"] = float(self.lineEdit_6.text())
            config["RangeScanStep"] = float(self.lineEdit_7.text())
            self.update_scanlist(config)

        self.lineEdit_5.editingFinished.connect(__set_scan_list)
        self.lineEdit_6.editingFinished.connect(__set_scan_list)
        self.lineEdit_7.editingFinished.connect(__set_scan_list)

        def scan_range(func, meta=''):
            """
            decorator, when applied to func, scan range for func.
            adds or alters the following meta params:
                meta[name]["Delay"] : str or float, current position
                meta[name]["iDelay"]: int, index of current position
            """
            def iterate(meta=dict()):
                round = config["ScanRound"]
                if config["ScanMode"] == "Range" or config["ScanMode"] == "ExtFile":
                    delaylist = self.lstat.stat[name]["ScanList"]
                    for rd in range(round):
                        for i, pos in enumerate(delaylist):
                            if meta["TERMINATE"]:
                                self.lstat.expmsg("[{name}][scan_range] Received signal TERMINATE, trying graceful Thread exit".format(name=name))
                                break
                            target_position = pos
                            response = self.remote.moveabs(target_position)
                            config["ManualPosition"] = target_position
                            self.update_position()
                            self.lstat.fmtmsg(response)
                            self.lstat.stat[name]["CurrentRound"] = rd
                            self.lstat.stat[name]["Delay"] = pos
                            self.lstat.stat[name]["iDelay"] = i
                            func(meta=meta)
                else:
                    self.lstat.expmsg("[{name}][scan_range] Range is set manually, so no action has been taken".format(name=name))
                    self.lstat.stat[name]["CurrentRound"] = 0
                    self.lstat.stat[name]["Delay"] = "ManualDelay"
                    self.lstat.stat[name]["iDelay"] = 0
                    for round in range(round):
                        func(meta=meta)

            return iterate

        self.scan_range = scan_range

    def update_scanlist(self, config) -> list:
        name = config["Name"]
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        if config["ScanMode"] == "Range":
            self.lstat.stat[name]["ScanList"] = np.arange(config["RangeScanStart"], config["RangeScanStop"], config["RangeScanStep"]).tolist()
        else:
            self.lstat.stat[name]["ScanList"] = [config["ManualPosition"]]
        self.lstat.expmsg("Generated Position Scan List: {}".format(self.lstat.stat[name]["ScanList"]))
        self.lstat.dump_stat("last_stat.json")
        return self.lstat.stat[name]["ScanList"]
    
    def update_position(self):
        self.lineEdit_1.setText("{:.3f}".format(self.config["ManualPosition"]))