from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from .remote import RemoteSinglePointDetector
from .utils import ignore_connection_error

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget
from .bundle_widget import Ui_SinglePointDetector

class BundleSinglePointDetector(QWidget, Ui_SinglePointDetector):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat, parent=None) -> None:
        QWidget.__init__(self, parent=parent)
        self.config: dict = bundle_config["Config"]
        self.name = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat
        self.get_value = None
        self.get_data = None
        
        update_config = self.lcfg.update_config  # Alias for easier access
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        self.remote = RemoteSinglePointDetector(config)

        self.setupUi(self)
        self.label.setText(name)
        self.valueSignal.setReadOnly(True)
        self.dataSignal.setReadOnly(True)
        self.valueRef.setReadOnly(True)
        self.dataRef.setReadOnly(True)
        self.avgTimeEdit.setText(str(self.config["AveragingTime"]))

        @ignore_connection_error
        @update_config
        def __set_averaging_time():
            try:
                new_avg_time = float(self.avgTimeEdit.text())
                if new_avg_time <= 0:
                    raise ValueError("Averaging time must be positive.")
                self.config["AveragingTime"] = new_avg_time
                lstat.fmtmsg(f"Averaging time set to {new_avg_time:.6f} seconds.")
            except ValueError as e:
                lstat.expmsg(f"Invalid input for averaging time: {e}")
                self.avgTimeEdit.setText(str(self.config["AveragingTime"]))

        self.avgTimeEdit.editingFinished.connect(__set_averaging_time)

        @ignore_connection_error
        @update_config
        def __manual_take_value(buttonStatus: bool):
            rc = self.remote.get_value(self.config["AveragingTime"])
            value = rc["value"]
            reference = rc["reference"]
            self.valueSignal.setText("{:e}".format(value))
            self.valueRef.setText("{:e}".format(reference))
            lstat.fmtmsg(f"Manually retrieved value: {value:.6e}, reference: {reference:.6e}")
        
        self.valueButton.clicked.connect(__manual_take_value)

        @ignore_connection_error
        @update_config
        def __manual_take_data(buttonStatus: bool):
            rc = self.remote.get_data(self.config["AveragingTime"])
            data = rc["data"]
            reference = rc["reference"]
            self.dataSignal.setText(str(data))
            self.dataRef.setText(str(reference))
            lstat.fmtmsg(f"Manually retrieved data: {data}, reference: {reference}")
        
        self.dataButton.clicked.connect(__manual_take_data)

        @ignore_connection_error
        def __get_value(averaging_time=0.1):
            rc = self.remote.get_value(averaging_time)
            value = rc["value"]
            reference = rc["reference"]
            return [float(value), float(reference)]
        
        @ignore_connection_error
        def __get_data(averaging_time=0.1):
            rc = self.remote.get_data(averaging_time)
            data = rc["data"]
            reference = rc["reference"]
            return [data, reference]
        
        self.get_value = __get_value
        self.get_data = __get_data