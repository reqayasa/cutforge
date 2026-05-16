from dataclasses import dataclass

@dataclass(frozen=True)
class RawDemandRow:
    id: str = ""
    group: str = ""
    length: str = ""
    quantity: str = ""
    
@dataclass(frozen=True)
class RawStockRow:
    id: str = ""
    group: str = ""
    length: str = ""
    quantity: str = ""
    
