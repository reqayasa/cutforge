from typing import Sequence

from PySide6.QtWidgets import (
    QWidget, 
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QTextEdit,
    QTableView,
)
from PySide6.QtCore import Qt, Signal

from view.qt_model.table_model import StockReportTableModel, UnmetReportTableModel
from view.qt_model.editor_model import CsvTableModel


class BarCutterTab(QWidget):
    file_selected = Signal(str, str)
    solve_requested = Signal()
    reload_requested = Signal()
    export_requested = Signal()

    DEFAULT_STOCK_PATH = "data/input/test_stock.csv"
    DEFAULT_DEMAND_PATH = "data/input/test_demand.csv"

    INPUT_DEMAND = "demand"
    INPUT_STOCK = "stock"

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_signal()

        # Mapping
        self._preview_widgets = {
            self.INPUT_DEMAND: self._demand_preview_table, 
            self.INPUT_STOCK: self._stock_preview_table,
        }

    def _build_ui(self):
        layout = QVBoxLayout()

        self._solve_btn = QPushButton("SOLVE")
        self._solve_btn.setFixedHeight(60)
        self._solve_btn.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self._input_group("IMPORT DATA"))
        layout.addWidget(self._input_preview_group("INPUT"))
        layout.addWidget(self._setting_group("SETTING"))
        layout.addWidget(self._solve_btn)
        layout.addWidget(self._output_preview_group("OUTPUT"))

        self.setLayout(layout)
    
    def _connect_signal(self):
        self._demand_browse_btn.clicked.connect(
            lambda: self._browse_file("Demand CSV", self._demand_input, self.INPUT_DEMAND)
        )

        self._stock_browse_btn.clicked.connect(
            lambda: self._browse_file("Stock CSV", self._stock_input, self.INPUT_STOCK)
        )

        self._reload_btn.clicked.connect(
            self.reload_requested.emit
        )

        self._edit_btn.clicked.connect(
            lambda: ...
        )

        self._save_btn.clicked.connect(
            lambda: ...
        )

        self._solve_btn.clicked.connect(
            self.solve_requested.emit
        )

        self._export_btn.clicked.connect(
            self.export_requested.emit
        )
    
    # UI Component

    def _input_group(self, title) -> QGroupBox:
        group_box = QGroupBox(title)
        layout = QGridLayout()

        self._demand_input = QLineEdit(self.DEFAULT_DEMAND_PATH)
        self._stock_input = QLineEdit(self.DEFAULT_STOCK_PATH)

        self._demand_browse_btn = QPushButton("Browse")
        self._stock_browse_btn = QPushButton("Browse")

        layout.addWidget(QLabel("Demand CSV"), 0, 0)
        layout.addWidget(self._demand_input, 0, 1)
        layout.addWidget(self._demand_browse_btn, 0, 2)

        layout.addWidget(QLabel("Stock CSV"), 1, 0)
        layout.addWidget(self._stock_input, 1, 1)
        layout.addWidget(self._stock_browse_btn, 1, 2)

        group_box.setLayout(layout)
        return group_box
    
    def _input_preview_group(self, title) -> QGroupBox:
        group_box = QGroupBox(title)
        layout = QHBoxLayout()
        control_btn_layout = QVBoxLayout()

        self._reload_btn = QPushButton("Reload")
        self._edit_btn = QPushButton("Edit")
        self._save_btn = QPushButton("Save")

        control_btn_layout.addWidget(self._reload_btn)
        control_btn_layout.addWidget(self._edit_btn)
        control_btn_layout.addWidget(self._save_btn)

        
        self._demand_preview_table = QTableView()
        self._stock_preview_table = QTableView()
        control_btn_layout.addStretch()

        layout.addWidget(self._demand_preview_table, 1)
        layout.addWidget(self._stock_preview_table, 1)
        layout.addLayout(control_btn_layout)
    
        group_box.setLayout(layout)
        return group_box
    
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
    
    # Private Method
    
    def _browse_file(self, title: str, widget: QLineEdit, input_type):
        path, _ = QFileDialog.getOpenFileName(self, title, "", "CSV Files (*.csv)")

        if path:
            widget.setText(path)
            self.file_selected.emit(input_type, path)

    # Public Method

    def update_input_preview(self, input_type: str, headers: Sequence[str], rows: Sequence[Sequence[str]]):
        widget = self._preview_widgets.get(input_type)

        if input_type == self.INPUT_DEMAND:
            self._demand_preview_table.setModel(
                CsvTableModel(headers=headers, rows=rows)
            )
        
        if input_type == self.INPUT_STOCK:
            self._stock_preview_table.setModel(
                CsvTableModel(headers=headers, rows=rows)
            )
    
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
    
    def get_file_path(self):
        return {
            "demand_path": self._demand_input.text(),
            "stock_path": self._stock_input.text()
        }

