import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from .ui.canvas import Ui_MplCanvas

colors = ['black', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'orange']

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=6, dpi=100, ax_num = 1, xlabel="X-axis", ylabel=[]):
        if len(ylabel) != ax_num:
            print("Warning: ylabel list length does not match ax_num, using default labels.")
            ylabel_list = [f"Y-axis {i}" for i in range(ax_num)]
        else:
            ylabel_list = ylabel

        self.n = ax_num
        self.fig, self.host_ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.host_ax.set_xlabel(xlabel)
        self.host_ax.set_ylabel(ylabel_list[0], color='r')
        self.host_ax.tick_params(axis='y', labelcolor='r')
        # self.host_ax.grid(True)

        self.added_axes = []
        for i in range(ax_num - 1):
            ax = self.host_ax.twinx()
            ax.spines['right'].set_position(('outward', 60 * (i)))
            ax.set_ylabel(ylabel_list[i + 1], color=colors[i % len(colors)])
            ax.tick_params(axis='y', labelcolor=colors[i % len(colors)])
            # ax.grid(True)

            self.added_axes.append(ax)

        plt.tight_layout()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

class CanvasWidget(QWidget, Ui_MplCanvas):
    def __init__(self, ax_num=1, xlabel="X-axis", ylabel=[], parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.n = ax_num
        self.data_canvas = MplCanvas(ax_num=ax_num, xlabel=xlabel, ylabel=ylabel)
        self.toolbox = NavigationToolbar(self.data_canvas)
        hbox = QtWidgets.QVBoxLayout(self.widget)
        hbox.addWidget(self.toolbox)
        hbox.addWidget(self.data_canvas)

    def update_plot(self, data = [], labels = []):
        if len(data) != self.n:
            print("Warning: Data length does not match number of axes, no operation.")
        else:
            self.data_canvas.host_ax.clear()
            self.data_canvas.host_ax.plot(data[0][0], data[0][1], 'r-', label=labels[0] if labels else "Data 1")
            # self.data_canvas.host_ax.legend()
            for i in range(self.n - 1):
                self.data_canvas.added_axes[i].clear()
                self.data_canvas.added_axes[i].plot(data[i+1][0], data[i+1][1], label=labels[i] if labels else f"Data {i+1}", color=colors[i % len(colors)])
                # self.data_canvas.added_axes[i].legend()
            self.data_canvas.draw()
        QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CanvasWidget()
    mainWindow.show()
    sys.exit(app.exec())