# import sys
# from PyQt6.QtWidgets import QApplication
# from apps.linear_stage_control.main import LinearStageControlExperiment, lcfg, lstat
#
# app = QApplication(sys.argv)
# mainWindow = LinearStageControlExperiment(lcfg=lcfg, lstat=lstat)
# mainWindow.show()
# sys.exit(app.exec())

from apps.TRSTM_SP.main import app_run

app_run()