class Forge1DDataset:
    def __init__(self, stocks, parts, scale):
        self.stocks = stocks
        self.parts = parts
        self.scale = scale

    def total_parts(self):
        return sum(p.qty for p in self.parts)

    def total_stock(self):
        return sum(s.qty for s in self.stocks)

    def max_stock_length(self):
        return max(s.length for s in self.stocks)