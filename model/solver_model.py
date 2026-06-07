from dataclasses import dataclass


@dataclass(frozen=True)
class CutPiece:
    demand_id: str
    length: int

@dataclass(frozen=True)
class StockUsage:
    stock_id: str
    stock_length: int
    cuts: list[CutPiece]
    waste: int

@dataclass(frozen=True)
class UnmetDemand:
    demand_id: str
    length: int
    quantity: int

@dataclass(frozen=True)
class GroupSolveResult:
    group: str
    usages: list[StockUsage]
    unmet: list[UnmetDemand]

@dataclass(frozen=True)
class SolveResult:
    groups: list[GroupSolveResult]
    kerf: int = 0
    unit_scale: int = 0