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
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- INPUT GROUP ---
        input_group = QGroupBox("Input Files")
        input_layout = QGridLayout()

        self.stock_path = QLineEdit("data/input/stocks.csv")
        self.demand_path = QLineEdit("data/input/demand.csv")

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
        option_group = QGroupBox()
        option_layout = QHBoxLayout()

        self.kerf_check = QCheckBox("Use Kerf")
        self.kerf_value = QDoubleSpinBox()
        self.kerf_value.setValue(3.0)
        self.kerf_value.setMaximum(100)

        self.algorithm = QComboBox()
        self.algorithm.addItem("FFD", "BFG", "Column Generation")

        option_layout.addWidget(self.kerf_check)
        option_layout.addWidget(QLabel("Kerf"))
        option_layout.addWidget(self.kerf_value)
        option_layout.addSpacing(20)
        option_layout.addWidget(QLabel("Algorithm"))
        option_layout.addWidget(self.algorithm)

        option_group.setLayout(option_layout)

        # --- PREVIEW TABLE GROUP---
        preview_group = QGroupBox("CSV Preview")
        preview_layout = QVBoxLayout()

        self.preview_table = QTableWidget()
        
        preview_layout.addWidget(self.preview_table)
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

        log_layout.addWidget(self.log_view)
        log_group.setLayout(log_layout)

        # --- ADD TO MAIN LAYOUT
        layout.addWidget(input_group)
        layout.addWidget(option_group)
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
            self.load_csv_preview(path)

    def browse_demand(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Demand CSV")

        if path:
            self.demand_path.setText(path)
            self.load_csv_preview(path)

    def load_csv_preview(self, path):
        df = pd.read_csv(path)

        self.preview_table.setRowCount(len(df))
        self.preview_table.setColumnCount(len(df.columns))
        self.preview_table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.preview_table.setItem(
                    i,
                    j,
                    QTableWidgetItem(str(df.iloc[i, j]))
            )





