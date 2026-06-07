import unittest

from model.internal_model import DemandItem, StockItem, GroupInput
from service.solver_core import solve_group


class TestSolverCore(unittest.TestCase):

    def test_single_stock_single_cut(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 1),
            ],
            stocks=[
                StockItem("s1", "A", 500, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(result.group, "A")
        self.assertEqual(len(result.usages), 1)
        self.assertEqual(len(result.unmet), 0)

        usage = result.usages[0]

        self.assertEqual(usage.stock_id, "s1")
        self.assertEqual(len(usage.cuts), 1)
        self.assertEqual(usage.waste, 400)

    def test_multiple_demand_quantity(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 3),
            ],
            stocks=[
                StockItem("s1", "A", 500, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 1)
        self.assertEqual(len(result.usages[0].cuts), 3)
        self.assertEqual(len(result.unmet), 0)

    def test_unmet_demand(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 300, 2),
            ],
            stocks=[
                StockItem("s1", "A", 400, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 1)
        self.assertEqual(len(result.unmet), 1)
        self.assertEqual(result.unmet[0].quantity, 1)

    def test_respects_kerf(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 2),
            ],
            stocks=[
                StockItem("s1", "A", 205, 1),
            ],
            kerf=10,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 1)
        self.assertEqual(len(result.usages[0].cuts), 1)
        self.assertEqual(len(result.unmet), 1)

    def test_empty_group(self):
        group = GroupInput(
            group="A",
            demands=[],
            stocks=[],
            kerf=0,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(result.group, "A")
        self.assertEqual(result.usages, [])
        self.assertEqual(result.unmet, [])

    def test_first_cut_does_not_consume_kerf(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 1),
            ],
            stocks=[
                StockItem("s1", "A", 150, 1),
            ],
            kerf=10,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 1)
        self.assertEqual(result.usages[0].waste, 50)

    def test_second_cut_consumes_kerf(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 2),
            ],
            stocks=[
                StockItem("s1", "A", 210, 1),
            ],
            kerf=10,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 1)
        self.assertEqual(len(result.usages[0].cuts), 2)
        self.assertEqual(result.usages[0].waste, 0)

    def test_unmet_same_demand_is_aggregated(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 3),
            ],
            stocks=[
                StockItem("s1", "A", 100, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.unmet), 1)
        self.assertEqual(result.unmet[0].demand_id, "d1")
        self.assertEqual(result.unmet[0].quantity, 2)

    def test_stock_quantity_creates_multiple_stock_instances(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 2),
            ],
            stocks=[
                StockItem("s1", "A", 100, 2),
            ],
            kerf=0,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 2)
        self.assertEqual(len(result.unmet), 0)

    def test_exact_fit_after_multiple_cuts(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 100, 3),
            ],
            stocks=[
                StockItem("s1", "A", 320, 1),
            ],
            kerf=10,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 1)
        self.assertEqual(len(result.usages[0].cuts), 3)
        self.assertEqual(result.usages[0].waste, 0)

    def test_uses_next_stock_if_first_stock_does_not_fit(self):
        group = GroupInput(
            group="A",
            demands=[
                DemandItem("d1", "A", 250, 1),
            ],
            stocks=[
                StockItem("s1", "A", 200, 1),
                StockItem("s2", "A", 300, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        result = solve_group(group)

        self.assertEqual(len(result.usages), 1)
        self.assertEqual(result.usages[0].stock_id, "s2")