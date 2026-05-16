from PySide6.QtWidgets import QMainWindow, QTabWidget

from view.bar_cutter_tab import BarCutterTab

class MainWindow(QMainWindow):
    def __init__(self, tabs):
        super().__init__()

        self.setWindowTitle("Cut Forge")
        self.resize(700, 700)

        tab_widget = QTabWidget()

        for title, widget in tabs:
            tab_widget.addTab(widget, title)

        self.setCentralWidget(tab_widget)