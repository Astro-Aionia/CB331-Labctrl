import sys
import time
from threading import Thread
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtWidgets

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from .ui.stm_boxcar import Ui_STMBoxcarExperiment
from labctrl.components.linear_stages.servo.factory import FactoryServoStage
from labctrl.components.TOPAS.factory import FactoryTOPAS
from labctrl.components.lockin_and_boxcars.ziUHF.factory import FactoryZiUHF
from labctrl.widgets.message_box import MessageWidget
from labctrl.widgets.canvas import CanvasWidget

app_name = "STMBoxcar"
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name = app_config["DelayLine"]
boxcar_name = app_config["Boxcar"]
tp_static_name = app_config["PumpStatic"]
tp_dynamic_name = app_config["PumpDynamic"]

class STMBoxcarExpData:
    def __init__(self, lcfg, lstat):
        self.lcfg = lcfg
        self.stat = lstat
        self.delays = lstat.stat[delay_stage_name]["ScanList"]
        self.sig = np.zeros((len(self.delays), 1), dtype=np.float64)
        self.sigsum = np.zeros((len(self.delays), 1), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        tosave = self.sig
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.sigsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.delays)
        np.savetxt(filename, tosave, delimiter=',')

class STMBoxcarExperiment(QMainWindow, Ui_STMBoxcarExperiment):
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
        tp_dynamic_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["TOPAS"][tp_dynamic_name]
        }
        self.tp_dynamic = factory.generate_bundle(tp_dynamic_bundle_config)
        self.tp_dynamic.change_shutter()
        time.sleep(0.1)
        self.tp_dynamic.change_shutter()

        factory = FactoryTOPAS(lcfg, lstat)
        tp_static_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["TOPAS"][tp_static_name]
        }
        self.tp_static = factory.generate_bundle(tp_static_bundle_config)
        self.tp_static.change_shutter()
        time.sleep(0.1)
        self.tp_static.change_shutter()

        factory = FactoryZiUHF()
        detector_bundle_config = {
            "BundleType": "PyQt6",
            "Config": lcfg.config["lockin_and_boxcars"][boxcar_name]
        }
        self.boxcar = factory.generate_bundle(lcfg, lstat)

        self.message_box = MessageWidget(lstat)

        self.data = STMBoxcarExpData(lcfg, lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

        self.canvas = CanvasWidget()

        # setup UI
        b1 = QtWidgets.QGridLayout(self.StageWidget)
        b1.addWidget(self.linear_stage)
        b2 = QtWidgets.QGridLayout(self.MessageWidget)
        b2.addWidget(self.message_box)
        b3 = QtWidgets.QGridLayout(self.DelayCurveWidget)
        b3.addWidget(self.canvas)
        self.lineEdit.setText(lcfg.config["apps"][app_name]["SaveFileName"])

        @self.linear_stage.scan_range
        def unit_operation(meta=dict()):
            if self.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg(
                    "PumpProbe operation received signal TERMINATE, trying graceful Thread exit")
                return
            lstat.expmsg("Retriving signal from sensor...")
            sig = self.boxcar.get_value()
            lstat.expmsg("Adding latest signal to dataset...")
            stat = lstat.stat[delay_stage_name]
            self.data.sig[stat["iDelay"], :] = sig
            self.data.sigsum[stat["iDelay"], :] += sig
            self.canvas.update_plot(self.data.delays[:stat["iDelay"]+1], self.data.sig[:stat["iDelay"]+1, 0])
            if stat["iDelay"] + 1 == len(stat["ScanList"]):
                lstat.expmsg("End of delay scan round {rd}, exporting data...".format(rd=stat["CurrentRound"]))
                self.data.export("acq_data/" + self.lineEdit.text() + "-Round{rd}".format(rd=stat["CurrentRound"]) + ".csv")
            QApplication.processEvents()

        def task():
            lstat.expmsg("Allocating memory for experiment")
            self.data = STMBoxcarExpData(lcfg, lstat)
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

        def __tp_static_shutter():
            self.tp_static.change_shutter()
            if lstat.stat[tp_static_name]["ShutterIsOpen"]:
                self.lineEdit_1.setText("On")
            else:
                self.lineEdit_1.setText("Off")

        self.pushButton_3.clicked.connect(__tp_static_shutter)

        def __tp_dynamic_shutter():
            self.tp_dynamic.change_shutter()
            if lstat.stat[tp_dynamic_name]["ShutterIsOpen"]:
                self.lineEdit_2.setText("On")
            else:
                self.lineEdit_2.setText("Off")

        self.pushButton_4.clicked.connect(__tp_dynamic_shutter)

        def __set_filename():
            lcfg.config["apps"][app_name]["SaveFileName"] = self.lineEdit.text()

        self.lineEdit.editingFinished.connect(__set_filename)

def app_run():
    STMBoxcar = QApplication(sys.argv)
    mainWindow = STMBoxcarExperiment(lcfg=lcfg, lstat=lstat)
    mainWindow.show()
    sys.exit(STMBoxcar.exec())