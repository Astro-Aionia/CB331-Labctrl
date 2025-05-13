import sys
from labctrl.labstat import LabStat, lstat
from labctrl.labconfig import LabConfig, lcfg
from PyQt6.QtWidgets import QApplication
from labctrl.components.lockin_and_boxcars.ziUHF.factory import FactoryZiUHF

factory = FactoryZiUHF()
app = QApplication(sys.argv)
uhf = factory.generate_bundle(lcfg=lcfg, lstat=lstat)
uhf.show()
sys.exit(app.exec())