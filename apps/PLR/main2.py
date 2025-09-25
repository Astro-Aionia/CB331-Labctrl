import sys
import time
from threading import Thread
import numpy as np

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from .ui.PLR import Ui_PLRExperiment
from labctrl.components.linear_stages.osms.factory import FactoryOSMSStage
from labctrl.components.lockin_and_boxcars.ziUHF.factory import FactoryZiUHF
from labctrl.widgets.message_box import MessageWidget
from labctrl.widgets.canvas import CanvasWidget

app_name = "PLR"
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name = app_config["DelayLine"]
boxcar_name = app_config["Boxcar"]

class PLRExpData:
    def __init__(self, lcfg, lstat):
        self.lcfg = lcfg
        self.stat = lstat
        self.delays = lstat.stat[delay_stage_name]["ScanList"]
        self.sig = np.zeros((len(self.delays), 1), dtype=np.float64)
        self.sigsum = np.zeros((len(self.delays), 1), dtype=np.float64)
        self.ref = np.zeros((len(self.delays), 1), dtype=np.float64)
        self.refsum = np.zeros((len(self.delays), 1), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        tosave = self.sig
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.sigsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Ref.csv"
        tosave = self.ref
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Ref.csv"
        tosave = self.refsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.delays)
        np.savetxt(filename, tosave, delimiter=',')

class PLRExperiment(QMainWindow, Ui_PLRExperiment):
    def __init__(self,lcfg: LabConfig, lstat: LabStat, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # add devices and functions
        factory = FactoryOSMSStage(lcfg, lstat)
        delayline_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["linear_stages"][delay_stage_name]
        }
        self.linear_stage = factory.generate_bundle(delayline_bundle_config)

        factory = FactoryZiUHF()
        detector_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["lockin_and_boxcars"][boxcar_name]
        }
        self.boxcar = factory.generate_bundle(lcfg, lstat)

        self.message_box = MessageWidget(lstat)

        self.data = PLRExpData(lcfg, lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

        self.canvas_delay = CanvasWidget(ax_num=2, xlabel="Delay (ps)", ylabel=["Signal", "Reference"])
        self.canvas_wv = CanvasWidget(ax_num=2, xlabel="Wavelength (nm)", ylabel=["Signal", "Reference"])

        # setup UI
        b1 = QtWidgets.QGridLayout(self.StageWidget)
        b1.addWidget(self.linear_stage)
        b2 = QtWidgets.QGridLayout(self.MessageWidget)
        b2.addWidget(self.message_box)
        b3 = QtWidgets.QGridLayout(self.CurveWidget)
        b3.addWidget(self.canvas_delay)
        self.lineEdit.setText(lcfg.config["apps"][app_name]["SaveFileName"])

        @lcfg.update_config
        def __set_averaging_time():
            lcfg.config["apps"][app_name]["AveragingTime"] = float(self.lineEdit_2.text())
            lstat.expmsg("Averaging time set to {at:.3f} s".format(at=lcfg.config["apps"][app_name]["AveragingTime"]))

        self.lineEdit_2.editingFinished.connect(__set_averaging_time)

        @self.linear_stage.scan_range
        def unit_operation(meta=dict()):
            if self.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg(
                    "PumpProbe operation received signal TERMINATE, trying graceful Thread exit")
                return
            lstat.expmsg("Retriving signal from sensor...")
            time.sleep(1)
            value = self.boxcar.get_value(averaging_time=lcfg.config["apps"][app_name]["AveragingTime"])
            sig = value[0]
            ref = value[1]
            lstat.expmsg("Adding latest signal to dataset...")
            stat = lstat.stat[delay_stage_name]
            self.data.sig[stat["iDelay"], 0] = sig
            self.data.sigsum[stat["iDelay"], 0] += sig
            self.data.ref[stat["iDelay"], 0] = ref
            self.data.refsum[stat["iDelay"], 0] += ref
            
            new_delay_data = [[self.data.delays[:stat["iDelay"]+1], self.data.sig[:stat["iDelay"]+1, 0]], [self.data.delays[:stat["iDelay"]+1], self.data.ref[:stat["iDelay"]+1, 0]]]
        
            self.canvas_delay.update_plot(new_delay_data, labels=["Signal", "Reference"])
            if stat["iDelay"] + 1 == len(stat["ScanList"]):
                lstat.expmsg("End of delay scan round {rd}, exporting data...".format(rd=stat["CurrentRound"]))
                self.data.export("acq_data/" + self.lineEdit.text() + "-Round{rd}".format(rd=stat["CurrentRound"]))
            QApplication.processEvents()

        def task():
            lstat.expmsg("Allocating memory for experiment")
            self.data = PLRExpData(lcfg, lstat)
            lstat.expmsg("Starting experiment")
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

        # def __tp_static_shutter():
        #     self.tp_static.change_shutter()
        #     if lstat.stat[tp_static_name]["ShutterIsOpen"]:
        #         self.lineEdit_1.setText("On")
        #     else:
        #         self.lineEdit_1.setText("Off")

        # self.pushButton_3.clicked.connect(__tp_static_shutter)

        # def __tp_dynamic_shutter():
        #     self.tp_dynamic.change_shutter()
        #     if lstat.stat[tp_dynamic_name]["ShutterIsOpen"]:
        #         self.lineEdit_2.setText("On")
        #     else:
        #         self.lineEdit_2.setText("Off")

        # self.pushButton_4.clicked.connect(__tp_dynamic_shutter)

        def __set_filename():
            lcfg.config["apps"][app_name]["SaveFileName"] = self.lineEdit.text()

        self.lineEdit.editingFinished.connect(__set_filename)

if __name__ == "mainWindow":
    PLR = QApplication(sys.argv)
    mainWindow = PLRExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.show()
    sys.exit(PLR.exec())
else:
    def app_run():
        PLR = QApplication(sys.argv)
        mainWindow = PLRExperiment(lcfg=lcfg, lstat=lstat)
        mainWindow.show()
        sys.exit(PLR.exec())

    mainWindow = PLRExperiment(lcfg=lcfg, lstat=lstat)