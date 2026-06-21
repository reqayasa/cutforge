from service import read_csv, resolve_headers, parse_row
from service.data_export import write_csv
from model.raw_input_model import RawDemandRow, RawStockRow
from model.internal_model import SolveOptions, NormalizeOptions
from config import HEADER_ALIASES
from view.qt_model.editor_model import CsvTableModel


class BarCutterController():

    def __init__(self, view, service):
        self._view = view
        self._service = service

        self._raw_demands: list[RawDemandRow] = []
        self._raw_stocks: list[RawStockRow] = []
        self._solve_report = None

        self._view.demand_load_requested.connect(self._on_demand_load)
        self._view.stock_load_requested.connect(self._on_stock_load)
        self._view.solve_requested.connect(self._on_solve_requested)
        self._view.export_requested.connect(self._on_export)

    def _read_data(self, path: str) :
        return read_csv(path)

    def _on_demand_load(self, path: str):
        headers, rows = read_csv(path)
        mapping = resolve_headers(headers, HEADER_ALIASES)
        self._raw_demands = [parse_row(r, mapping, RawDemandRow) for r in rows]
        self._view.set_demand_model(CsvTableModel(headers, rows))

    def _on_stock_load(self, path: str):
        headers, rows = read_csv(path)
        mapping = resolve_headers(headers, HEADER_ALIASES)
        self._raw_stocks = [parse_row(r, mapping, RawStockRow) for r in rows]
        self._view.set_stock_model(CsvTableModel(headers, rows))

    def _on_solve_requested(self):
        setting = self._view.get_setting()
        normalize_options = NormalizeOptions(
            max_precision = int(setting["precision"])
        )
        solve_options = SolveOptions(
            kerf = setting["kerf"]
        )

        solve_report =  self._service.solve(
            raw_demands = self._raw_demands,
            raw_stocks = self._raw_stocks,
            normalize_options = normalize_options,
            solve_options = solve_options
        )
        self._solve_report = solve_report

        self._view.update_output_preview(solve_report)

    def _on_export(self):
        if self._solve_report is None:
            return

        write_csv(self._solve_report)