import sys
sys.path.append('..')
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QFileDialog, QDialog
from .ui.file_dialog import Ui_FileDialog

class FileSelect(QDialog, Ui_FileDialog):
    def __init__(self, parent=None, mode=QFileDialog.FileMode.AnyFile, filter_ = str("All files (*)")):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.dialog = QtWidgets.QFileDialog(parent=parent)
        self.dialog.setFileMode(mode)
        self.dialog.setNameFilter(filter_)
        self.lineEdit.setReadOnly(True)
        self.pushButton.clicked.connect(lambda: self.select())

    def select(self):
        if self.dialog.exec():
            # filename = self.dialog.selectedFiles()[0]
            # print(filename)
            self.lineEdit.setText(self.dialog.selectedFiles()[0])
        # return filename

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = FileSelect()
    mainWindow.show()
    sys.exit(app.exec())