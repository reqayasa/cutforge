import math
from decimal import Decimal

class LengthScaler:
    def __init__(self):
        self.scale = 1

    def detect_scale(self, values):
        max_decimal = 0

        for v in values:
            d = Decimal(str(v))
            decimals = abs(d.as_tuple().exponent)
            max_decimal = max(max_decimal, decimals)
            
        self.scale = 10 ** max_decimal

    def to_int(self, value):
        return int(round(float(value) * self.scale))
    
    def to_float(self, value):
        return value / self.scale