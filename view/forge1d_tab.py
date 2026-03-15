import logging
import pandas as pd
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
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QTextEdit,
)


class Forge1DTab(QWidget):
    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger("cutforge")

        self.init_ui()

        self.load_csv_preview(self.preview_table_stock, self.stock_path.text())
        self.load_csv_preview(self.preview_table_demand, self.demand_path.text())


    def init_ui(self):
        layout = QVBoxLayout()

        # --- INPUT GROUP ---
        input_group = QGroupBox("Input Files")
        input_layout = QGridLayout()

        self.stock_path = QLineEdit("data/input/forge1d_stocks.csv")
        self.demand_path = QLineEdit("data/input/forge1d_demand.csv")

        stock_btn = QPushButton("Browse")
        stock_btn.clicked.connect(self.browse_stock)
        demand_btn = QPushButton("Browse")
        demand_btn.clicked.connect(self.browse_demand)
        
        input_layout.addWidget(QLabel("Stock CSV"), 0, 0)
        input_layout.addWidget(self.stock_path, 0, 1)
        input_layout.addWidget(stock_btn, 0, 2)

        input_layout.addWidget(QLabel("Demand CSV"), 1, 0)
        input_layout.addWidget(self.demand_path, 1, 1)
        input_layout.addWidget(demand_btn, 1, 2)

        input_group.setLayout(input_layout)

        # --- OPTIONS GROUP---
        # option_group = QGroupBox()
        # option_layout = QHBoxLayout()

        # self.kerf_check = QCheckBox("Use Kerf")
        # self.kerf_value = QDoubleSpinBox()
        # self.kerf_value.setValue(3.0)
        # self.kerf_value.setMaximum(100)

        self.algorithm = QComboBox()
        self.algorithm.addItem("FFD", "BFG", "Column Generation")

        # option_layout.addWidget(self.kerf_check)
        # option_layout.addWidget(QLabel("Kerf"))
        # option_layout.addWidget(self.kerf_value)
        # option_layout.addSpacing(20)
        # option_layout.addWidget(QLabel("Algorithm"))
        # option_layout.addWidget(self.algorithm)

        # option_group.setLayout(option_layout)

        # --- PREVIEW TABLE GROUP---
        preview_group = QGroupBox("CSV Preview")
        preview_layout = QHBoxLayout()

        self.preview_table_stock = QTableWidget()
        self.preview_table_demand = QTableWidget()
                
        preview_layout.addWidget(self.preview_table_stock)
        preview_layout.addWidget(self.preview_table_demand)
        preview_group.setLayout(preview_layout)

        # --- SOLVE BUTTON ---
        self.solve_button = QPushButton("Solve")

        # --- RESULT SUMMARY GROUP ---
        summary_group = QGroupBox("Result Summary")
        summary_layout = QGridLayout()

        self.total_parts = QLabel("-")
        self.sheets_used = QLabel("-")
        self.total_waste = QLabel("-")
        self.efficiency = QLabel("-")
        
        summary_layout.addWidget(QLabel("Total Parts"), 0, 0)
        summary_layout.addWidget(self.total_parts, 0, 1)

        summary_layout.addWidget(QLabel("Sheets Used"), 1, 0)
        summary_layout.addWidget(self.sheets_used, 1, 1)

        summary_layout.addWidget(QLabel("Total Waste"), 2, 0)
        summary_layout.addWidget(self.total_waste, 2, 1)

        summary_layout.addWidget(QLabel("Efficiency"), 3, 0)
        summary_layout.addWidget(self.efficiency, 3, 1)

        summary_group.setLayout(summary_layout)

        # --- LOG VIEWER GROUP ---
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        self.log_view.verticalScrollBar().setValue(
            self.log_view.verticalScrollBar().maximum()
        )

        log_layout.addWidget(self.log_view)
        log_group.setLayout(log_layout)

        # --- ADD TO MAIN LAYOUT
        layout.addWidget(input_group)
        # layout.addWidget(option_group)
        layout.addWidget(preview_group)
        layout.addWidget(self.solve_button)
        layout.addWidget(summary_group)
        layout.addWidget(log_group)

        # layout.addStretch()

        self.setLayout(layout)

    def browse_stock(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Stock CSV")

        if path:
            self.stock_path.setText(path)
            self.load_csv_preview(self.preview_table_stock, path)

    def browse_demand(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Demand CSV")

        if path:
            self.demand_path.setText(path)
            self.load_csv_preview(self.preview_table_demand, path)

    def load_csv_preview(self, table_widget, path):
        try:
            df = pd.read_csv(path)
        except Exception as e:
            self.logger.error("Preview error: %s,", e)
            return

        df = df.head(50)

        table_widget.setRowCount(len(df))
        table_widget.setColumnCount(len(df.columns))
        table_widget.setHorizontalHeaderLabels(df.columns)

        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                table_widget.setItem(
                    row,
                    col,
                    QTableWidgetItem(value)
            )

        self.logger.info("%d item is loaded from %s,", len(df), path)
        
        table_widget.resizeColumnsToContents()
        