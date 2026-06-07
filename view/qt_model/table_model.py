from PySide6.QtCore import Qt, QAbstractTableModel
from service.denormalization import denormalize_length


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

    def __init__(self, rows, unit_scale):
        super().__init__()
        self._rows = rows
        self._unit_scale = unit_scale

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
        cutlist = []

        for cut in row.cuts:
            cutlist.append(denormalize_length(cut.length, self._unit_scale))

        values = [
            row.usage_id,
            row.group,
            row.stock_id,
            denormalize_length(row.stock_length, self._unit_scale),
            denormalize_length(row.used_length, self._unit_scale),
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

    def __init__(self, rows, unit_scale):
        super().__init__()
        self._rows = rows
        self._unit_scale = unit_scale

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
            denormalize_length(row.length, self._unit_scale),
            row.quantity,
        ]

        return str(values[col])