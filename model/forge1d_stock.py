class Forge1DStock:
    def __init__(self, stock_id: str, length:float, qty:int):
        self.stock_id = stock_id
        self.length = float(length)
        self.qty = int(qty)

    def __repr__(self):
        return f"Forge1DStock(id={self.stock_id}, length={self.length}, qty={self.qty})"