import sys

from .singleton import Singleton
from datetime import datetime
import json

from PyQt6.QtWidgets import QWidget, QApplication
from .experiment_message import Ui_ExperimentMessage

class LabStat(Ui_ExperimentMessage, QWidget):
    """
    Singleton class to hold all the information about the current experiment.
    Also holds the front panel message widgets because these widgets are
    universal for all components
    """

    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.msg_list = list()
        self.stat = dict()

        # save front end panel pages so that different threads see the same doc
        self.root_names = ["dashboard", "setup",
                          "params", "schedule", "reports", "messages", "manual"]

    def dump_stat(self, filename) -> None:
        with open(filename, 'w') as f:
            json.dump(self.stat, f, indent=4)

    def expmsg(self, t: str) -> None:
        """formats messages, then send it to front end via a callback"""
        # print(t)
        for i in t.split('\n'):
            if len(i) < 80: # max 80 chars a line
                self.msg_list.append(i)
            else:
                while len(i) >= 80:
                    self.msg_list.append(i[0:80])
                    i = i[80:]
                self.msg_list.append(i)
        while len(self.msg_list) > 40:
            self.msg_list.pop(0)
        text = '\n'.join(self.msg_list)
        self.update_exp_msg(text)

    def fmtmsg(self, d: dict) -> None:
        """expmsg, but accepts a dict from json"""
        param = ""
        for i in d:
            if i != "success" and i != "message":
                param = param + ', '
                param = param + str(i)
                param = param + ':'
                param = param + str(d[i])

        msg_str = "[{time}][{success}] {message}{param}".format(
            time=str(datetime.now()),
            success="OK" if d["success"] else "Error",
            message=d["message"],
            param=param)

        self.expmsg(msg_str)

    def update_exp_msg(self, t):
        self.textEdit.setText(t)

lstatApp = QApplication(sys.argv)
lstat = LabStat()
sys.exit(lstatApp.exec())