import sys
from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow
from controller.solver_controller import SolverController
from core.logger import CutForgeLogger
from core.setup import setup_environment


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logger_obj = CutForgeLogger()
    logger = logger_obj.get_logger()

    window = MainWindow()
    controller = SolverController(window)

    logger_obj.qt_handler.log_signal.connect(
        window.forge1d_tab.log_view.append
    )

    setup_environment()
    
    window.show()

    sys.exit(app.exec())