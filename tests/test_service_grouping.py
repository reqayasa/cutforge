import unittest

from model.internal_model import (
    DemandItem,
    StockItem,
    NormalizedInput,
)
from service.grouping import group_inputs


class TestGrouping(unittest.TestCase):

    def test_groups_are_partitioned(self):
        data = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 2),
                DemandItem("d2", "B", 120, 1),
            ],
            stocks=[
                StockItem("s1", "A", 600, 1),
                StockItem("s2", "B", 700, 1),
            ],
            kerf=3,
            unit_scale=1,
        )

        groups = group_inputs(data)

        self.assertEqual(len(groups), 2)

        by_group = {g.group: g for g in groups}

        self.assertEqual(len(by_group["A"].demands), 1)
        self.assertEqual(len(by_group["A"].stocks), 1)

        self.assertEqual(len(by_group["B"].demands), 1)
        self.assertEqual(len(by_group["B"].stocks), 1)

    def test_kerf_is_preserved(self):
        data = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 1),
            ],
            stocks=[
                StockItem("s1", "A", 500, 1),
            ],
            kerf=4,
            unit_scale=1,
        )

        groups = group_inputs(data)

        self.assertEqual(groups[0].kerf, 4)

    def test_group_with_only_demand_is_kept(self):
        data = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 1),
            ],
            stocks=[],
            kerf=0,
            unit_scale=1,
        )

        groups = group_inputs(data)

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].group, "A")
        self.assertEqual(len(groups[0].demands), 1)
        self.assertEqual(len(groups[0].stocks), 0)

    def test_group_with_only_stock_is_kept(self):
        data = NormalizedInput(
            demands=[],
            stocks=[
                StockItem("s1", "B", 600, 2),
            ],
            kerf=0,
            unit_scale=1,
        )

        groups = group_inputs(data)

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].group, "B")
        self.assertEqual(len(groups[0].demands), 0)
        self.assertEqual(len(groups[0].stocks), 1)

    def test_empty_input_returns_empty_list(self):
        data = NormalizedInput(
            demands=[],
            stocks=[],
            kerf=0,
            unit_scale=1,
        )

        groups = group_inputs(data)

        self.assertEqual(groups, [])