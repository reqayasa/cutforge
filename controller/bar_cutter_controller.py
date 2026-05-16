from service import read_csv, resolve_headers, parse_row
from model.raw_input_model import RawDemandRow, RawStockRow
from model.internal_model import SolveOptions, NormalizeOptions


class BarCutterController():

    HEADER_ALIASES = {
        "id": {
            "id",
            "part",
            "part_id",
            "partid",
            "id_part",
            "mark",
            "name",
        },

        "group": {
            "group",
            "category",
            "type",
            "section",
        },

        "length": {
            "length",
            "len",
            "panjang",
            "cut_length",
        },

        "quantity": {
            "qty",
            "quantity",
            "jumlah",
            "count",
            "pcs",
        },
    }

    REQUIRED_FIELDS = {
        "length",
        "quantity",
    }


    def __init__(self, view, service):
        self._view = view
        self._service = service

        self._raw_demands: list[RawDemandRow] = []
        self._raw_stocks: list[RawStockRow] = []

        self._view.file_selected.connect(self._on_file_selected)
        self._view.solve_requested.connect(self._on_solve_btn_clicked)


    def read_data(self, path: str) :
        return read_csv(path)

    def _on_file_selected(self, input_type, path):
        (headers, rows) = self.read_data(path)

        mapping = resolve_headers(headers, self.HEADER_ALIASES)

        if input_type == "demand":
            self._raw_demands = [
                parse_row(row, mapping, RawDemandRow)
                for row in rows
            ]
        
        if input_type == 'stock':
            self._raw_stocks = [
                parse_row(row, mapping, RawStockRow)
                for row in rows
]

        self._view.update_input_preview(input_type, headers=headers, rows=rows)

    def _on_solve_btn_clicked(self):
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

        self._view.update_output_preview(solve_report)