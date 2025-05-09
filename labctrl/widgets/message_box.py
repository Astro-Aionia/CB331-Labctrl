from PyQt6.QtWidgets import QWidget, QApplication
from .ui.message_box import Ui_ExperimentMessage

class MessageWidget(QWidget, Ui_ExperimentMessage):
    def __init__(self, lstat, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.lstat = lstat
        self.lstat.object.update.connect(lambda : self.update_text())
        self.update_text()

    def update_text(self):
        self.textEdit.setText(self.lstat.message)
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())
        QApplication.processEvents()
