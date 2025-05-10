import sys
import time
from threading import Thread
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtWidgets

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from .ui.SFG import Ui_SFGExperiment
from labctrl.components.linear_stages.servo.factory import FactoryServoStage
from labctrl.components.TOPAS.factory import FactoryTOPAS
from labctrl.components.cameras.EMCCD.factory import FactoryEMCCD
from labctrl.widgets.message_box import MessageWidget

app_name = "SFG"
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name = app_config["DelayLine"]
detector_name = app_config["Detector"]
topas_name = app_config["TOPAS"]

class SFGExpData:
    def __init__(self, lcfg, lstat):
        self.lcfg = lcfg
        self.stat = lstat
        self.delays = lstat.stat[delay_stage_name]["ScanList"]
        self.npixels = lcfg.config["cameras"][detector_name]["NumberOfPixels"]
        self.pixels_list = np.arange(self.npixels)
        self.xmin = np.min(self.pixels_list)
        self.xmax = np.max(self.pixels_list)
        self.ymin = np.min(self.delays)
        self.ymax = np.max(self.delays)
        self.sig = np.zeros((len(self.delays), self.npixels), dtype=np.float64)
        self.sigsum = np.zeros((len(self.delays), self.npixels), dtype=np.float64)
        self.bg = np.zeros((len(self.delays), self.npixels), dtype=np.float64)
        self.bgsum = np.zeros((len(self.delays), self.npixels), dtype=np.float64)
        self.delta = np.zeros((len(self.delays), self.npixels), dtype=np.float64)
        self.deltasum = np.zeros((len(self.delays), self.npixels), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        tosave = self.sig
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.sigsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Background.csv"
        tosave = self.bg
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Background.csv"
        tosave = self.bgsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delta.csv"
        tosave = self.delta
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Delta.csv"
        tosave = self.deltasum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.delays)
        np.savetxt(filename, tosave, delimiter=',')

class SFGExperiment(QMainWindow, Ui_SFGExperiment):
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
        self.topas.change_shutter()
        time.sleep(2)
        self.topas.change_shutter()

        factory = FactoryEMCCD(lcfg, lstat)
        detector_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["cameras"][detector_name]
        }
        self.detector = factory.generate_bundle(detector_bundle_config)

        self.message_box = MessageWidget(lstat)

        self.data = SFGExpData(lcfg, lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

        # setup UI
        b1 = QtWidgets.QGridLayout(self.StageWidget)
        b1.addWidget(self.linear_stage)
        b2 = QtWidgets.QGridLayout(self.MessageWidget)
        b2.addWidget(self.message_box)
        b3 = QtWidgets.QGridLayout(self.DetectorWidget)
        b3.addWidget(self.detector)
        b3 = QtWidgets.QGridLayout(self.TOPASWidget)
        b3.addWidget(self.topas)

        @self.linear_stage.scan_range
        @self.topas.scan_range
        def unit_operation(meta=dict()):
            if self.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg(
                    "PumpProbe operation received signal TERMINATE, trying graceful Thread exit")
                return
            lstat.expmsg("Retriving signal from sensor...")
            sig = self.detector.acquire()
            lstat.expmsg("Adding latest signal to dataset...")
            stat = lstat.stat[delay_stage_name]
            if lstat.stat[topas_name]["ShutterIsOpen"]:
                self.data.bg[stat["iDelay"],:] = sig
                self.data.bgsum[stat["iDelay"], :] += sig
            else:
                self.data.sig[stat["iDelay"], :] = sig
                self.data.sigsum[stat["iDelay"], :] += sig
                self.data.delta[stat["iDelay"], :] = sig - self.data.bg[stat["iDelay"], :]
                self.data.deltasum[stat["iDelay"], :] += self.data.delta[stat["iDelay"], :]
            QApplication.processEvents()
            self.topas.change_shutter()
            # time.sleep(2)
            lstat.expmsg("Retriving signal from sensor...")
            sig = self.detector.acquire()
            lstat.expmsg("Adding latest signal to dataset...")
            stat = lstat.stat[delay_stage_name]
            if lstat.stat[topas_name]["ShutterIsOpen"]:
                self.data.bg[stat["iDelay"], :] = sig
                self.data.bgsum[stat["iDelay"], :] += sig
            else:
                self.data.sig[stat["iDelay"], :] = sig
                self.data.sigsum[stat["iDelay"], :] += sig
                self.data.delta[stat["iDelay"], :] = sig - self.data.bg[stat["iDelay"], :]
                self.data.deltasum[stat["iDelay"], :] += self.data.delta[stat["iDelay"], :]
            if stat["iDelay"] + 1 == len(stat["ScanList"]):
                lstat.expmsg("End of delay scan round, exporting data...")
                self.data.export("acq_data/" + lcfg.config["cameras"][detector_name]["FileName"] + "-Round{rd}".format(rd=stat["CurrentRound"]) + "-Pump{wv}".format(wv=lstat.stat[topas_name]["PumpWavelength"]) + ".csv")
            QApplication.processEvents()

        def task():
            lstat.expmsg("Allocating memory for experiment")
            self.data = SFGExpData(lcfg, lstat)
            lstat.expmsg("Starting experiment")
            self.detector.reset()
            meta = dict()
            meta["TERMINATE"] = False
            unit_operation(meta=meta)
            self.flags["FINISH"] = True
            self.flags["RUNNING"] = False
            lstat.expmsg("Experiment done")

        def __start():
            self.flags["TERMINATE"] = False
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = True
            thread = Thread(target=task)
            thread.start()

        self.pushButton_1.clicked.connect(__start)

        def __stop():
            lstat.expmsg("Terminating current job")
            self.flags["TERMINATE"] = True
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = False

        self.pushButton_2.clicked.connect(__stop)

def app_run():
    SFG = QApplication(sys.argv)
    mainWindow = SFGExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.show()
    sys.exit(SFG.exec())