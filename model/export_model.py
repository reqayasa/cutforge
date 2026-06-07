from dataclasses import dataclass

@dataclass(frozen=True)
class CutPlanExportRow:
    group: str
    usage_id: str
    stock_id: str
    stock_length: float
    demand_id: str
    cut_length: float
    waste: float | None