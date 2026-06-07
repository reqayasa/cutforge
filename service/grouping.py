from model.internal_model import NormalizedInput, GroupInput
from collections import defaultdict


def group_inputs(data: NormalizedInput) -> list[GroupInput]:
    """
    Split NormalizedInput by Group

    Args:
        data (NormalizedInput): data.

    Returns:
        list[GroupInput]: data per group.
    """

    demand_map = defaultdict(list)
    stock_map = defaultdict(list)

    for demand in data.demands:
        demand_map[demand.group].append(demand)

    for stock in data.stocks:
        stock_map[stock.group].append(stock)

    groups = demand_map.keys() | stock_map.keys()

    return [
        GroupInput(
            group       = group,
            demands     = demand_map[group],
            stocks      = stock_map[group],
            kerf        = data.kerf,
            unit_scale  = data.unit_scale
        )
        for group in groups
    ]
