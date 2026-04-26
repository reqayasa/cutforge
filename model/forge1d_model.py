from dataclasses import dataclass, field

@dataclass
class Part:
    id: str
    length: int
    qty: int

    def remove(self) -> bool:
        if self.qty > 0:
            self.qty -= 1
            return True
        return False

@dataclass
class Stock:
    id: str
    length: int
    qty: int

    def remove(self) -> bool:
        if self.qty > 0:
            self.qty -= 1
            return True
        return False

@dataclass
class Pattern:
    stock_id: str
    stock_length: int
    parts: list[tuple[str, int]] = field(default_factory=list)

    def used_length(self) -> int:
        return sum(length for _, length in self.parts)

    def remaining(self) -> int:
        return self.stock_length - self.used_length()

    def add_part(self, part: Part):
        # store snapshot (safe, no mutation issues)
        self.parts.append((part.id, part.length))