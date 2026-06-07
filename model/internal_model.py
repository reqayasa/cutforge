from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class DemandItem:
    id: str
    group: str
    length: int
    quantity: int
    
@dataclass(frozen=True)
class StockItem:
    id: str
    group: str
    length: int
    quantity: int

@dataclass(frozen=True)
class NormalizedInput:
    demands: list[DemandItem]
    stocks: list[StockItem]
    kerf: int
    unit_scale: int

@dataclass(frozen=True)
class GroupInput:
    group: str
    demands: list[DemandItem]
    stocks: list[StockItem]
    kerf: int
    unit_scale: int

@dataclass(frozen=True)
class NormalizeOptions:
    max_precision: int = 3

@dataclass(frozen=True)
class SolveOptions:
    kerf: str = "0"

@dataclass
class WarningKind(str, Enum):
    ROUNDED_LENGTH = "rounded_length"
    ROUNDED_KERF = "rounded_kerf"
    EMPTY_ROWS_DROPPED = "empty_rows_dropped"
    DUPLICATE_ROWS_MERGED = "duplicate_rows_merged"

@dataclass(frozen=True)
class NormalizationWarning:
    kind: WarningKind
    affected_rows: int

@dataclass(frozen = True)
class NormalizationResult:
    data: NormalizedInput
    warnings: list[NormalizationWarning]   


