class Forge1DPattern:
    def __init__(self, stock_length):
        self.stock_length = stock_length
        self.parts = []

    def used_length(self):
        return sum(self.parts)

    def remaining(self):
        return self.stock_length - self.used_length()

    def add_part(self, part_length):
        self.parts.append(part_length)