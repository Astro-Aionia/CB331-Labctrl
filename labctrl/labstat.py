from .singleton import Singleton
from datetime import datetime
import json

from PyQt6.QtCore import pyqtSignal, QObject

class ExperimentMessageObject(QObject):
    update = pyqtSignal(str)
    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)

class LabStat(metaclass=Singleton):
    """
    Singleton class to hold all the information about the current experiment.
    Also holds the front panel message widgets because these widgets are
    universal for all components
    """

    def __init__(self) -> None:
        self.msg_list = list()
        self.stat = dict()
        self.object = ExperimentMessageObject()
        self.message = ''

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
            self.msg_list.append(i)
            # if len(i) < 80: # max 80 chars a line
            #     self.msg_list.append(i)
            # else:
            #     while len(i) >= 80:
            #         self.msg_list.append(i[0:80])
            #         i = i[80:]
            #     self.msg_list.append(i)
        while len(self.msg_list) > 40:
            self.msg_list.pop(0)
        self.message = '\n'.join(self.msg_list)
        self.object.update.emit(self.message)

    def fmtmsg(self, d: dict) -> None:
        """expmsg, but accepts a dict from json"""
        param = ""
        for i in d:
            if i != "success" and i != "message":
                param = param + ', '
                param = param + str(i)
                param = param + ':'
                param = param + str(d[i])

        # msg_str = "[{time}][{success}] {message}{param}".format(
        #     time=str(datetime.now()),
        #     success="OK" if d["success"] else "Error",
        #     message=d["message"],
        #     param=param)

        msg_str = "[{time}][{success}] {message}".format(
            time=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            success="OK" if d["success"] else "Error",
            message=d["message"])

        self.expmsg(msg_str)

lstat = LabStat()
