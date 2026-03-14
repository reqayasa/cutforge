import sys
from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow
from controller.solver_controller import SolverController

app = QApplication(sys.argv)

window = MainWindow()
controller = SolverController(window)

window.show()

sys.exit(app.exec())