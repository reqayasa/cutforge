from PySide6.QtWidgets import QProxyStyle
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class GlobalButtonCursorStyle(QProxyStyle):
    def polish(self, widget):
        from PySide6.QtWidgets import QPushButton
        super().polish(widget)
        if isinstance(widget, QPushButton):
            widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))