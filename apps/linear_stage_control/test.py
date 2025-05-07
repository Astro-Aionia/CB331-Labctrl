import sys
# sys.path.append("..\..")

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtWidgets

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from apps.linear_stage_control.ui.linear_stage_control import Ui_LinearStageControlExperiment
from labctrl.components.servo.factory import FactoryServoStage

app_name = "linear_stage_control"
print(lcfg.config)
# app_config: dict = lcfg.config["apps"][app_name]
# delay_stage_name = app_config["DelayLine"]