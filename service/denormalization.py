from decimal import Decimal


def denormalize_length(length: int, unit_scale: int) -> float:
    if unit_scale == 0:
        return float(length)
    return float(Decimal(length) / Decimal(unit_scale))
