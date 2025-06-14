# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the ziUHF lock-in amplifier
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

from .remote import ProxiedUHF
from .utils import ignore_connection_error

from PyQt6.QtWidgets import QWidget
from .bundle_widget import Ui_ManualBoxcar

class BundleZiUHF(QWidget, Ui_ManualBoxcar):
    """
    This class is responsible for holding references to the PyQt6 UI Widgets
    of a single ziUHF lock-in amplifier.
    """

    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.get_value = None
        self.lineEdit.setReadOnly(True)


class FactoryZiUHF:
    def __init__(self) -> None:
        pass

    def generate_bundle(self, lcfg, lstat):
        bundle = BundleZiUHF()

        config = lcfg.config["lockin_and_boxcars"]["ziUHF"]
        remote = ProxiedUHF(config)

        # def __test_online():
        #     try:
        #         lstat.fmtmsg(remote.online())
        #     except Exception as inst:
        #         print(type(inst), inst.args)
        #         lstat.expmsg(
        #             "[Error] Nothing from remote, server is probably down.")
        #
        # bundle.pushButton.clicked.connect(__test_online)

        @ignore_connection_error
        def __manual_take_sample():
            response = remote.get_value()
            bundle.lineEdit.setText("{:e}".format(response["value"]))
            lstat.fmtmsg(response)
        
        bundle.pushButton.clicked.connect(__manual_take_sample)

        def __get_value():
            value = remote.get_value()
            value = value["value"]
            return float(value)

        bundle.get_value = __get_value

        return bundle