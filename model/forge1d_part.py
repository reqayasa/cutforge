class Forge1DPart:
    def __init__(self, part_id: str, length: float, qty: int):
        self.part_id = part_id
        self.length = float(length)
        self.qty = int(qty)

    def __repr__(self):
        return f"Forge1DPart(id={self.part_id}, length={self.length}, qty={self.qty})"