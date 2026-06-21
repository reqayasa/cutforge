import sys
from PySide6.QtWidgets import QApplication
from view import MainWindow, BarCutterTab
from view.style import button
from controller import BarCutterController
from service.cut_service import CutService


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(button.GlobalButtonCursorStyle())

    # logger_obj = CutForgeLogger()
    # logger = logger_obj.get_logger()

    bar_cutter_tab = BarCutterTab()

    cut_service = CutService()

    bar_cutter_controller = BarCutterController(bar_cutter_tab, cut_service)

    window = MainWindow([
        ("Bar Cutter", bar_cutter_tab)
    ])

    # controller = SolverController(window)

    # logger_obj.qt_handler.log_signal.connect(
    #     window.forge1d_tab.log_view.append
    # )

    # setup_environment()
    
    window.show()

    sys.exit(app.exec())