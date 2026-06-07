from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
)

class CsvTableModel(QAbstractTableModel):

    def __init__(self, headers, rows):
        super().__init__()
        self._headers = headers
        self._rows = rows

    def rowCount(self, parent=QModelIndex()):
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return None

        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None

        row = index.row()
        col = index.column()

        row_data = self._rows[row]

        key = self._headers[col]

        return str(row_data[key])

    def headerData(self, section, orientation, role):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

        return str(section + 1)

    def flags(self, index):
        return (
            Qt.ItemIsSelectable
            | Qt.ItemIsEnabled
            | Qt.ItemIsEditable
        )

    def setData(self, index, value, role):

        if role != Qt.EditRole:
            return False

        row = index.row()
        col = index.column()

        self._rows[row][col] = value

        self.dataChanged.emit(index, index)

        return True