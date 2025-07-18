import numpy as np
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from .remote import RemoteServoStage

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget
from .bundle_widget import Ui_ServoStage
from labctrl.widgets.file_dialog import FileSelect

def calc_pos(pos:float, direction: str, unit:str, zero_point:float):
    if unit == "mm":
        zp = 0
        position = pos
    elif unit == "ps":
        zp = zero_point
        position = pos*0.299792458/2
    else:
        print("Invalid unit, the default unit mm is applied.")
        position = pos
    if direction == "Positive":
        return zp + position
    elif direction == "Negative":
        return zp - position
    else:
        print("Invalid direction, the default direction Positive is applied.")
        return zp + position
    
def calc_dis(dis:float, direction: str, unit:str):
    if unit == "mm":
        distance = dis
    elif unit == "ps":
        distance = dis*0.299792458/2
    else:
        print("Invalid unit, the default unit mm is applied.")
        distance = dis
    if direction == "Positive":
        return distance
    elif direction == "Negative":
        return -distance
    else:
        print("Invalid direction, the default direction Positive is applied.")
        return distance

class BundlePyQt6ServoStage(QWidget, Ui_ServoStage):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat, parent=None) -> None:
        QWidget.__init__(self, parent=parent)
        self.config: dict = bundle_config["Config"]
        self.name = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat

        update_config = self.lcfg.update_config  # Alias for easier access
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        self.remote = RemoteServoStage(config)

        self.update_scanlist(config)

        # UI setup and initialize parameters
        self.setupUi(self)
        self.lineEdit_1.setReadOnly(True)
        self.lineEdit_1.setText("{:.3f}".format(self.config["ManualPosition"]))
        self.lineEdit_2.setText(str(self.config["DrivingSpeed"]))
        self.lineEdit_8.setText(str(self.config["ZeroPointAbsolutePosition"]))
        self.lineEdit_3.setText("0.0")
        self.lineEdit_4.setText("0.0")
        self.lineEdit_5.setText(str(self.config["RangeScanStart"]))
        self.lineEdit_6.setText(str(self.config["RangeScanStop"]))
        self.lineEdit_7.setText(str(self.config["RangeScanStep"]))
        self.lineEdit_9.setText(str(self.config["ScanRound"]))

        if self.config["ScanMode"] == "Range":
            self.comboBox.setCurrentText("Range")
        elif self.config["ScanMode"] == "ExtFile":
            self.comboBox.setCurrentText("ExtFile")
        else:
            pass

        if config["WorkingUnit"] == "mm":
            self.workUnit.setCurrentText("mm")
            self.label_9.setText("mm")
            self.label_10.setText("mm")
            self.label_15.setText("mm")
        elif config["WorkingUnit"] == "ps":
            self.workUnit.setCurrentText("ps")
            self.label_9.setText("ps")
            self.label_10.setText("ps")
            self.label_15.setText("ps")

        self.filedialog = FileSelect()
        self.delay_selcet = QtWidgets.QGridLayout(self.FileDialog)
        self.delay_selcet.addWidget(self.filedialog)
        self.filedialog.lineEdit.setText(self.config["LoadedExternalScanList"])

        @update_config
        def __set_velocity():
            config["DrivingSpeed"] = float(self.lineEdit_2.text())
            response = self.remote.set_velocity(config["DrivingSpeed"])
            self.lstat.fmtmsg(response)

        self.lineEdit_2.editingFinished.connect(__set_velocity)

        @update_config
        def __set_zero_point():
            config["ZeroPointAbsolutePosition"] = float(self.lineEdit_8.text())

        self.lineEdit_8.editingFinished.connect(__set_zero_point)

        @update_config
        def __set_workunit(comboxStatus: str):
            workunit = self.workUnit.currentText()
            config["WorkingUnit"] = workunit
            self.label_9.setText(workunit)
            self.label_10.setText(workunit)
            self.label_15.setText(workunit)

        self.workUnit.currentTextChanged.connect(__set_workunit)

        @update_config
        def __movepos(buttonStatus: bool):
            target_distance = calc_dis(float(self.lineEdit_3.text()),config["WorkingDirection"],config["WorkingUnit"])
            response = self.remote.moveinc(target_distance)
            config["ManualPosition"] = response["position"]
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_1.clicked.connect(__movepos)

        @update_config
        def __moveneg(buttonStatus: bool):
            target_distance = calc_dis(float(self.lineEdit_3.text()),config["WorkingDirection"],config["WorkingUnit"])
            response = self.remote.moveinc(-target_distance)
            config["ManualPosition"] = response["position"]
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_2.clicked.connect(__moveneg)

        @update_config
        def __moveabs(buttonStatus: bool):
            config["ManualPosition"] = calc_pos(float(self.lineEdit_4.text()),config["WorkingDirection"],config["WorkingUnit"],config["ZeroPointAbsolutePosition"])
            response = self.remote.moveabs(config["ManualPosition"])
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_3.clicked.connect(__moveabs)

        @update_config
        def __home(buttonStatus: bool):
            config["ManualPosition"] = config["ZeroPointAbsolutePosition"]
            response = self.remote.moveabs(config["ZeroPointAbsolutePosition"])
            self.update_position()
            self.lstat.fmtmsg(response)

        self.pushButton_4.clicked.connect(__home)

        @update_config
        def __set_scan_mode(comboxStatus: str):
            config["ScanMode"] = self.comboBox.currentText()
            self.update_scanlist(config)

        self.comboBox.currentTextChanged.connect(__set_scan_mode)

        @update_config
        def __set_scan_round():
            config["ScanRound"] = int(self.lineEdit_9.text())

        self.lineEdit_9.editingFinished.connect(__set_scan_round)

        @update_config
        def __set_scan_list(backSignal=None):
            config["RangeScanStart"] = float(self.lineEdit_5.text())
            config["RangeScanStop"] = float(self.lineEdit_6.text())
            config["RangeScanStep"] = float(self.lineEdit_7.text())
            config["LoadedExternalScanList"] = self.filedialog.lineEdit.text()
            self.update_scanlist(config)

        self.lineEdit_5.editingFinished.connect(__set_scan_list)
        self.lineEdit_6.editingFinished.connect(__set_scan_list)
        self.lineEdit_7.editingFinished.connect(__set_scan_list)
        self.filedialog.lineEdit.textChanged.connect(__set_scan_list)

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
                            target_position = calc_pos(pos,config["WorkingDirection"],config["WorkingUnit"],config["ZeroPointAbsolutePosition"])
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
                    func(meta=meta)

            return iterate

        self.scan_range = scan_range

    def update_scanlist(self, config) -> list:
        name = config["Name"]
        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()
        if config["ScanMode"] == "Range":
            self.lstat.stat[name]["ScanList"] = np.arange(config["RangeScanStart"], config["RangeScanStop"], config["RangeScanStep"]).tolist()
        elif config["ScanMode"] == "ExtFile":
            self.lstat.stat[name]["ScanList"]  = np.loadtxt(config["LoadedExternalScanList"]).tolist()
        else:
            self.lstat.stat[name]["ScanList"] = [config["ManualPosition"]]
        self.lstat.expmsg("Generated Position Scan List: {}".format(self.lstat.stat[name]["ScanList"]))
        self.lstat.dump_stat("last_stat.json")
        return self.lstat.stat[name]["ScanList"]

    def update_position(self):
        self.lineEdit_1.setText("{:.3f}".format(self.config["ManualPosition"]))