import sys
import os

from labctrl.labconfig import LabConfig, lcfg
from labctrl.labstat import LabStat, lstat

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from labctrl.widgets.ui.labctrl import Ui_Labctrl
from labctrl.widgets.server import FactoryServer
from labctrl.widgets.app_button import AppButton

import apps

class Labctrl(QMainWindow, Ui_Labctrl):
    def __init__(self, lcfg: LabConfig, lstat: LabStat, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

        self.linear_stages = []

        for i, item in enumerate(lcfg.config["linear_stages"]):
            factory = FactoryServer(lcfg, lstat)
            bundle_config = {
                "BundleType": "PyQt6",
                "Class": "linear_stages",
                "Name": item
            }
            self.linear_stages.append(factory.generate_bundle(bundle_config))
            self.linear_stage_group.addWidget(self.linear_stages[i])

        self.topas = []

        for i, item in enumerate(lcfg.config["TOPAS"]):
            factory = FactoryServer(lcfg, lstat)
            bundle_config = {
                "BundleType": "PyQt6",
                "Class": "TOPAS",
                "Name": item
            }
            self.topas.append(factory.generate_bundle(bundle_config))
            self.topas_group.addWidget(self.topas[i])

        self.cameras = []

        for i, item in enumerate(lcfg.config["cameras"]):
            factory = FactoryServer(lcfg, lstat)
            bundle_config = {
                "BundleType": "PyQt6",
                "Class": "cameras",
                "Name": item
            }
            self.cameras.append(factory.generate_bundle(bundle_config))
            self.camera_group.addWidget(self.cameras[i])

        self.lockin_and_boxcars = []

        for i, item in enumerate(lcfg.config["lockin_and_boxcars"]):
            factory = FactoryServer(lcfg, lstat)
            bundle_config = {
                "BundleType": "PyQt6",
                "Class": "lockin_and_boxcars",
                "Name": item
            }
            self.lockin_and_boxcars.append(factory.generate_bundle(bundle_config))
            self.lockin_and_boxcar_group.addWidget(self.lockin_and_boxcars[i])

        self.apps = []

        for i, item in enumerate(lcfg.config["apps"]):
            self.apps.append(AppButton(app_name=item))
            self.app_group.addWidget(self.apps[i])


labctrl = QApplication(sys.argv)
mainWindow = Labctrl(lcfg=lcfg, lstat=lstat)
mainWindow.show()
sys.exit(labctrl.exec())