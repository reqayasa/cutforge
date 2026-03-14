from PySide6.QtWidgets import QMainWindow, QTabWidget

from view.forge1d_tab import Forge1DTab
from view.forge2d_tab import Forge2DTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cut Forge")
        self.resize(900, 600)

        self.tabs = QTabWidget()

        self.forge1d_tab = Forge1DTab()
        self.forge2d_tab = Forge2DTab()

        self.tabs.addTab(self.forge1d_tab, "Forge 1D")
        self.tabs.addTab(self.forge2d_tab, "Forge 2D")

        self.setCentralWidget(self.tabs)