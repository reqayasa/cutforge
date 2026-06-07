from dataclasses import dataclass
from model.solver_model import CutPiece

@dataclass(frozen=True)
class StockReportRow:
    group: str
    stock_id: str
    stock_length: int
    used_length: int
    waste: int
    cut_count: int

@dataclass(frozen=True)
class UnmetReportRow:
    group: str
    demand_id: str
    length: int
    quantity: int

# @dataclass(frozen=True)
# class SolveReport:
#     stock_rows: list[StockReportRow]
#     unmet_rows: list[UnmetReportRow]

# @dataclass(frozen=True)
# class CutReportRow:
#     demand_id: str
#     length: int

@dataclass(frozen=True)
class StockUsageReport:
    usage_id: int
    group: str
    stock_id: str
    stock_length: int
    used_length: int
    waste: int
    cuts: list[CutPiece]

@dataclass(frozen=True)
class SolveSummary:
    total_stock_count: int
    total_used_length: int
    total_waste: int
    waste_percentage: float

@dataclass(frozen=True)
class SolveReport:
    usages: list[StockUsageReport]
    unmet_rows: list[UnmetReportRow]
    unit_scale: int = 1
    # summary: SolveSummary