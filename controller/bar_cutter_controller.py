from service import CutService


class BarCutterController():

    def __init__(self, view, service):
        self._view = view
        self._service = service
        self._rows = {
            "Demand CSV": None,
            "Stock CSV": None,
        }
        self._view.file_selected.connect(self._handle_file_selected)
        # self._view.solve_btn.clicked.connect(self._handle_solve_btn_clicked)
        # self._view._reload_btn.connect(self._handle_reloade_btn_clicked)


    def solve(self):
        try:
            inputs = self.view.get_inputs()

            report = self.service.solve(**inputs)

            self.view.set_report(report)

        except Exception as exc:
            self.view.show_error(str(exc))

    def import_csv(str):
        pass

    def _handle_file_selected(self, title, path):
        rows = self.import_csv(path)

        if title not in self._rows:
            raise ValueError(f"Unknown file title: {title!r}")

        self._rows[title] = rows
        self._view.update_input_preview(title, rows)

    def _handle_solve_btn_clicked(self):
        self.solve()

    def _handle_reloade_btn_clicked(self):
        ...
