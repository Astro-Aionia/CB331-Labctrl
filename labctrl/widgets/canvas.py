import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from .ui.canvas import Ui_MplCanvas

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = fig.add_subplot(1, 1, 1)
        plt.tight_layout()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

class CanvasWidget(QWidget, Ui_MplCanvas):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.data_canvas = MplCanvas()
        self.toolbox = NavigationToolbar(self.data_canvas)
        hbox = QtWidgets.QVBoxLayout(self.widget)
        hbox.addWidget(self.toolbox)
        hbox.addWidget(self.data_canvas)

    def update_plot(self, *args, **kwargs):
        self.data_canvas.ax.clear()
        self.data_canvas.ax.plot(*args, **kwargs)
        self.data_canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CanvasWidget()
    mainWindow.show()
    sys.exit(app.exec())