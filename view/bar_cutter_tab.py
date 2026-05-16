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
)
from PySide6.QtCore import Qt, Signal


class BarCutterTab(QWidget):
    file_selected = Signal(str, str)

    DEFAULT_STOCK_PATH = "data/input/bar_stocks.csv"
    DEFAULT_DEMAND_PATH = "data/input/bar_demands.csv"

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
            lambda: self._browse_file("Demand CSV", self._demand_input))
        
        self._stock_browse_btn.clicked.connect(
            lambda: self._browse_file("Stock CSV", self._stock_input))
        
        self._reload_btn.clicked.connect(
            lambda: ...
        )

        self._edit_btn.clicked.connect(
            lambda: ...
        )

        self._save_btn.clicked.connect(
            lambda: ...
        )

        self._solve_btn.clicked.connect(
            lambda: ...
        )

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

        
        self._demand_preview_table = QTableWidget()
        self._stock_preview_table = QTableWidget()
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
        layout = QGridLayout()

        output_preview = QTextEdit()
        output_preview.setReadOnly(True)

        layout.addWidget(output_preview)
        
        group_box.setLayout(layout)
        return group_box
    
    def _browse_file(self, title: str, widget: QLineEdit):
        path, _ = QFileDialog.getOpenFileName(self, title, "", "CSV Files (*.csv)")

        if path:
            widget.setText(path)
            self.file_selected.emit(title, path)

    def update_input_preview(self, title: str, headers: Sequence[str], rows: Sequence[Sequence[str]]):
        widget = self._preview_widgets.get(title)

        if widget is None:
            raise ValueError(f"Unknown preview title: {title!r}")
        
        if not rows:
            widget.setRowCount(0)
            return


        widget.setRowCount(len(rows))
        widget.setColumnCount(len(headers))
        widget.setHorizontalHeaderLabels(headers)

        for r, _ in enumerate(rows):
            for c, _ in enumerate(headers):
                value = rows[r][c]
                widget.setItem(r, c, QTableWidgetItem(value))
        
        widget.resizeColumnsToContents()

