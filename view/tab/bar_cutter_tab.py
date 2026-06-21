from typing import Sequence

from PySide6.QtWidgets import (
    QWidget, 
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableView,
)
from PySide6.QtCore import Signal

from view.qt_model.table_model import StockReportTableModel, UnmetReportTableModel
from view.component import InputPanel


class BarCutterTab(QWidget):
    demand_load_requested = Signal(str)
    stock_load_requested  = Signal(str)
    solve_requested = Signal()
    export_requested = Signal()

    DEFAULT_STOCK_PATH = "data/input/test_stock.csv"
    DEFAULT_DEMAND_PATH = "data/input/test_demand.csv"

    INPUT_DEMAND = "demand"
    INPUT_STOCK = "stock"

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_signal()

    def _build_ui(self):
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        self._demand_panel = InputPanel("INPUT DEMAND", self.DEFAULT_DEMAND_PATH, QTableView())
        self._stock_panel  = InputPanel("INPUT STOCK",  self.DEFAULT_STOCK_PATH, QTableView())

        self._solve_btn = QPushButton("SOLVE")
        self._solve_btn.setFixedHeight(60)

        input_layout.addWidget(self._demand_panel)
        input_layout.addWidget(self._stock_panel)
        input_layout.addWidget(self._setting_group("SETTING"))
        layout.addLayout(input_layout)
        layout.addWidget(self._solve_btn)
        layout.addWidget(self._output_preview_group("OUTPUT"))

        self.setLayout(layout)
    
    def _connect_signal(self):
        self._demand_panel.load_requested.connect(self.demand_load_requested)
        self._stock_panel.load_requested.connect(self.stock_load_requested)
        self._solve_btn.clicked.connect(self.solve_requested.emit)
        self._export_btn.clicked.connect(self.export_requested.emit)
    

    # UI Component
    
    def _setting_group(self, title) -> QGroupBox:
        group_box = QGroupBox(title)
        layout = QGridLayout()

        self._kerf = QLineEdit("0")
        self._precision = QLineEdit("2")

        layout.addWidget(QLabel("Kerf"), 0, 0)
        layout.addWidget(self._kerf, 0, 1)

        layout.addWidget(QLabel("Precision"), 1, 0)
        layout.addWidget(self._precision, 1, 1)

        group_box.setLayout(layout)
        return group_box
    
    def _output_preview_group(self, title) -> QGroupBox:
        group_box = QGroupBox(title)
        layout = QHBoxLayout()
        table_layout = QVBoxLayout()
        control_btn_layout = QVBoxLayout()

        self._export_btn = QPushButton("Export")

        control_btn_layout.addWidget(self._export_btn)
        
        self._stock_table = QTableView()
        self._unmet_table = QTableView()

        table_layout.addWidget(self._stock_table)
        table_layout.addWidget(self._unmet_table)
        layout.addLayout(table_layout)
        layout.addLayout(control_btn_layout)
        
        group_box.setLayout(layout)
        return group_box

    # Public Method
    
    def update_output_preview(self, report):
        self._stock_table.setModel(
            StockReportTableModel(report.usages, report.unit_scale)
        )

        self._unmet_table.setModel(
            UnmetReportTableModel(report.unmet_rows, report.unit_scale)
        )

    def get_setting(self):
        return {
            "kerf": self._kerf.text(),
            "precision": self._precision.text()
        }
    
    def set_demand_model(self, model):
        self._demand_panel.set_model(model)

    def set_stock_model(self, model):
        self._stock_panel.set_model(model)

    def get_demand_path(self) -> str:
        return self._demand_panel.get_path()

    def get_stock_path(self) -> str:
        return self._stock_panel.get_path()
