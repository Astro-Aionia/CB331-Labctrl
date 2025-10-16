from .remote import ProxiedPhaseDelayer
from .utils import ignore_connection_error

from PyQt6.QtWidgets import QWidget
from .bundle_widget import Ui_PhaseDelayer

class BundlePhaseDelayer(QWidget, Ui_PhaseDelayer):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.get_delay = None
        self.set_delay = None
        self.lineEdit.setReadOnly(True)

class FactoryPhaseDelayer:
    def __init__(self):
        pass

    def generate_bundle(self, lcfg, lstat):
        bundle = BundlePhaseDelayer()

        config = lcfg.config["lockin_and_boxcars"]["phase_delayer"]
        remote = ProxiedPhaseDelayer(config)

        @ignore_connection_error
        def __manual_get_delay():
            response = remote.get_delay()
            bundle.lineEdit.setText("{delay}".format(delay=response["delay"]))
            lstat.fmtmsg(response)
        
        bundle.pushButton.clicked.connect(__manual_get_delay)

        @ignore_connection_error
        def __get_delay():
            delay = remote.get_delay()
            delay = delay["delay"]
            return int(delay)

        bundle.get_value = __get_delay

        @ignore_connection_error
        def __manual_set_delay():
            delay = int(bundle.lineEdit_2.text())
            response = remote.set_delay(delay)
            bundle.lineEdit.setText("{delay}".format(delay=response["delay"]))
            lstat.fmtmsg(response)
        
        bundle.pushButton_2.clicked.connect(__manual_set_delay)

        @ignore_connection_error
        def __set_delay(delay: int):
            remote.set_delay(delay)
            return int(delay)

        bundle.get_value = __set_delay

        return bundle