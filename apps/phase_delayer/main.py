import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from labctrl.components.lockin_and_boxcars.phase_delayer.factory import FactoryPhaseDelayer

app_name = "phase_delayer"
app_config: dict = lcfg.config["apps"][app_name]
delayer_name = app_config["Delayer"]

class PhaseDelayExperiment(QMainWindow):
    def __init__(self,lcfg: LabConfig, lstat: LabStat, parent = None):
        QMainWindow.__init__(self, parent=parent)
        factory = FactoryPhaseDelayer()
        delayer_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["lockin_and_boxcars"][delayer_name]
        }
        self.delayer = factory.generate_bundle(lcfg, lstat)

        self.setCentralWidget(self.delayer)

if __name__ == "mainWindow":
    Delayer = QApplication(sys.argv)
    mainWindow = PhaseDelayExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.show()
    sys.exit(Delayer.exec())
else:
    def app_run():
        Delayer = QApplication(sys.argv)
        mainWindow = PhaseDelayExperiment(lcfg=lcfg, lstat=lstat)
        mainWindow.show()
        sys.exit(Delayer.exec())

    mainWindow = PhaseDelayExperiment(lcfg=lcfg, lstat=lstat)