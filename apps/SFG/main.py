import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtWidgets
from charset_normalizer import detect

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from .ui.SFG import Ui_SFGExperiment
from labctrl.components.linear_stages.servo.factory import FactoryServoStage
from labctrl.components.TOPAS.Demo.factory import FactoryTOPAS
from labctrl.components.cameras.EMCCD.factory import FactoryEMCCD

app_name = "SFG"
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name = app_config["DelayLine"]
detector_name = app_config["Detector"]
topas_name = app_config["TOPAS"]

class LinearStageControlExperiment(QMainWindow, Ui_SFGExperiment):
    def __init__(self,lcfg: LabConfig, lstat: LabStat, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # add devices and functions
        factory = FactoryServoStage(lcfg, lstat)
        delayline_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["linear_stages"][delay_stage_name]
        }
        self.linear_stage = factory.generate_bundle(delayline_bundle_config)

        factory = FactoryTOPAS(lcfg, lstat)
        topas_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["TOPAS"][topas_name]
        }
        self.topas = factory.generate_bundle(topas_bundle_config)

        factory = FactoryEMCCD(lcfg, lstat)
        detector_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["cameras"][detector_name]
        }
        self.detector = factory.generate_bundle(detector_bundle_config)

        # setup UI
        b1 = QtWidgets.QGridLayout(self.StageWidget)
        b1.addWidget(self.linear_stage)
        b2 = QtWidgets.QGridLayout(self.MessageWidget)
        b2.addWidget(lstat.widget)
        b3 = QtWidgets.QGridLayout(self.DetectorWidget)
        b3.addWidget(self.detector)
        b3 = QtWidgets.QGridLayout(self.TOPASWidget)
        b3.addWidget(self.topas)

def app_run():
    app = QApplication(sys.argv)
    mainWindow = LinearStageControlExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.show()
    sys.exit(app.exec())