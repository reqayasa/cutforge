from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)


class InputPanel(QGroupBox):
    load_requested = Signal(str)  # Emit path
    
    def __init__(self, title: str, default_path: str, view: QWidget):
        super().__init__(title)
        self._default_path = default_path
        self._view = view
        self._build_ui()
        self._connect_signals()

    
    def _build_ui(self):
        layout = QVBoxLayout()
        file_row = QHBoxLayout()
        btn_row = QHBoxLayout()

        self._path_input = QLineEdit(self._default_path)
        self._browse_btn = QPushButton("Browse")
        self._reload_btn = QPushButton("Reload")
        self._edit_btn   = QPushButton("Edit")
        self._save_btn   = QPushButton("Save")

        file_row.addWidget(QLabel("File"))
        file_row.addWidget(self._path_input, 1)
        file_row.addWidget(self._browse_btn)

        btn_row.addWidget(self._reload_btn)
        btn_row.addWidget(self._edit_btn)
        btn_row.addWidget(self._save_btn)
        btn_row.addStretch()

        layout.addLayout(file_row)
        layout.addLayout(btn_row)
        layout.addWidget(self._view)
        self.setLayout(layout)

    def _connect_signals(self):
        self._browse_btn.clicked.connect(self._on_browse)
        self._reload_btn.clicked.connect(
            lambda: self.load_requested.emit(self.get_path())
        )

    def _on_browse(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv)")
        if path:
            self._path_input.setText(path)
            self.load_requested.emit(path)

    # Public API
    def get_path(self) -> str:
        return self._path_input.text()

    def set_model(self, model):
        self._view.setModel(model)