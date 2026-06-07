from PySide6.QtCore import Qt, QAbstractTableModel

class StockReportTableModel(QAbstractTableModel):

    HEADERS = [
        "ID",
        "Group",
        "Stock ID",
        "Stock Length",
        "Used Length",
        "Waste",
        "Cuts",
    ]

    def __init__(self, rows):
        super().__init__()
        self._rows = rows

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return str(section + 1)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        row = self._rows[index.row()]
        col = index.column()

        values = [
            row.usage_id,
            row.group,
            row.stock_id,
            row.stock_length,
            row.used_length,
            row.waste,
            row.cuts,
        ]

        return str(values[col])

class UnmetReportTableModel(QAbstractTableModel):

    HEADERS = [
        "Group",
        "Demand ID",
        "Length",
        "Quantity",
    ]

    def __init__(self, rows):
        super().__init__()
        self._rows = rows

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return str(section + 1)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        row = self._rows[index.row()]
        col = index.column()

        values = [
            row.group,
            row.demand_id,
            row.length,
            row.quantity,
        ]

        return str(values[col])