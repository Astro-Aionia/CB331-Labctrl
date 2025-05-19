import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from .ui.linear_stage_control import Ui_LinearStageControlExperiment
from labctrl.components.linear_stages.servo.factory import FactoryServoStage
from labctrl.widgets.message_box import MessageWidget

app_name = "linear_stage_control"
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name = app_config["DelayLine"]

class LinearStageControlExperiment(QMainWindow, Ui_LinearStageControlExperiment):
    def __init__(self,lcfg: LabConfig, lstat: LabStat, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # add devices and functions
        # self.lstat = lstat
        factory = FactoryServoStage(lcfg, lstat)
        delayline_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["linear_stages"][delay_stage_name]
        }
        self.linear_stage = factory.generate_bundle(delayline_bundle_config)

        # setup UI
        ui_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        ui_layout.addWidget(self.linear_stage)
        self.message_box = MessageWidget(lstat)
        ui_layout.addWidget(self.message_box)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = LinearStageControlExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.show()
    sys.exit(app.exec())
else:
    def app_run():
        app = QApplication(sys.argv)
        mainWindow = LinearStageControlExperiment(lcfg=lcfg, lstat=lstat)
        mainWindow.show()
        sys.exit(app.exec())

    mainWindow = LinearStageControlExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.setWindowIcon(QIcon("./apps/linear_stage_control/icon.ico"))