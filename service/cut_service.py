from model.raw_input_model import RawDemandRow, RawStockRow
from model.internal_model import NormalizeOptions, SolveOptions
from model.report_model import SolveReport
from .normalization import normalize_inputs
from .solver_adapter import solve_all
from .grouping import group_inputs
from .reporting import build_report

class CutService:
    def solve(
            self,
            raw_demands: list[RawDemandRow],
            raw_stocks: list[RawStockRow],
            normalize_options: NormalizeOptions,
            solve_options: SolveOptions
    ) -> SolveReport:
        normalization_result = normalize_inputs(raw_demands, raw_stocks, normalize_options, solve_options)
        groups = group_inputs(normalization_result.data)
        solve_result = solve_all(groups)
        return build_report(result=solve_result)