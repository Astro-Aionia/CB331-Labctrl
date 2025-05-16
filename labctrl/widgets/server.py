import json
import os
import requests
from PyQt6.QtWidgets import QWidget
from .ui.server import Ui_Server

from labctrl.labstat import LabStat
from labctrl.labconfig import LabConfig

class ServerWidget(QWidget, Ui_Server):
    def __init__(self, config, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.name.setText(config["Name"])
        self.host.setText(config["Host"])
        self.port.setText(str(config["Port"]))
        self.server_path = ''

        def __set_host():
            config["Host"] = self.host.text()

        self.host.editingFinished.connect(__set_host)

        def __set_port():
            config["Port"] = int(self.port.text())

        self.port.editingFinished.connect(__set_port)

        def __test():
            try:
                print("http://{host}:{port}/".format(host=config["Host"], port=config["Port"]))
                response = requests.get("http://{host}:{port}/".format(host=config["Host"], port=config["Port"]))
                rc = response.content.decode()
                if json.loads(rc)["success"]:
                    self.status.setText("ON")
                else:
                    self.status.setText("OFF")
            except requests.exceptions.ConnectionError as err:
                print(err)
                self.status.setText("OFF")

        self.test.clicked.connect(__test)

        def __start():
            if "server.bat" in os.listdir(self.server_path):
                os.system(self.server_path+"server.bat")
            else:
                os.system(self.server_path+"proxy.bat")
          
        self.start.clicked.connect(__start)

class FactoryServer:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat
        self.generated = dict()

    def generate_bundle(self, bundle_config: dict):
        device = bundle_config["Class"]
        name = bundle_config["Name"]
        config = self.lcfg.config[device][name]
        name = bundle_config["Name"]
        if name in self.generated:
            print("[SANITY] FactoryLinearStage: BundleLinearStage with name {} already generated before!".format(name))
        foo = ServerWidget(config)
        foo.server_path = f"./servers/{device}/{name}/"
        self.generated[name] = foo
        return foo