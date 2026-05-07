# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the ziUHF lock-in amplifier
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

from labctrl.labstat import LabStat
from labctrl.labconfig import LabConfig
from .bundle_PyQt6 import BundleSinglePointDetector

class FactorySinglePointDetector:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat
        self.generated = dict()

    def generate_bundle(self, bundle_config: dict):
        name = bundle_config["Config"]["Name"]
        if name in self.generated:
            print("[SANITY] FactorySinglePointDetector: BundleSinglePointDetector with name {} already generated before!".format(name))
        foo = BundleSinglePointDetector(bundle_config, self.lcfg, self.lstat)
        self.generated[name] = foo
        return foo

        # def __test_online():
        #     try:
        #         lstat.fmtmsg(remote.online())
        #     except Exception as inst:
        #         print(type(inst), inst.args)
        #         lstat.expmsg(
        #             "[Error] Nothing from remote, server is probably down.")
        #
        # bundle.pushButton.clicked.connect(__test_online)
