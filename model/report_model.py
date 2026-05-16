from dataclasses import dataclass

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

@dataclass(frozen=True)
class SolveReport:
    stock_rows: list[StockReportRow]
    unmet_rows: list[UnmetReportRow]