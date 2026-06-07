import unittest
from model.internal_model import (
    NormalizedInput, DemandItem, StockItem, GroupInput
)
from service.grouping import group_inputs
from service.solver_core import solve_group
from service.solver_adapter import solve_all


class TestSolverEndToEnd(unittest.TestCase):
    """End-to-end tests for the complete solver workflow."""

    def test_single_group_simple_solve(self):
        """Test workflow: input → grouping → solving → result."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 2),
            ],
            stocks=[
                StockItem("s1", "A", 250, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        self.assertEqual(len(result.groups), 1)
        self.assertEqual(result.groups[0].group, "A")
        self.assertEqual(len(result.groups[0].usages), 1)
        self.assertEqual(len(result.groups[0].usages[0].cuts), 2)
        self.assertEqual(result.groups[0].usages[0].waste, 50)

    def test_multiple_groups_different_materials(self):
        """Test multi-group workflow where demands/stocks split by group."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 1),
                DemandItem("d2", "B", 200, 1),
            ],
            stocks=[
                StockItem("s1", "A", 300, 1),
                StockItem("s2", "B", 500, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        self.assertEqual(len(groups), 2)

        result = solve_all(groups)

        self.assertEqual(len(result.groups), 2)
        group_a = next(g for g in result.groups if g.group == "A")
        group_b = next(g for g in result.groups if g.group == "B")

        self.assertEqual(len(group_a.usages), 1)
        self.assertEqual(group_a.usages[0].waste, 200)
        self.assertEqual(len(group_b.usages), 1)
        self.assertEqual(group_b.usages[0].waste, 300)

    def test_workflow_with_kerf_and_multiple_stocks(self):
        """Test complex scenario: kerf, multiple stocks, unmet demand."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 4),
            ],
            stocks=[
                StockItem("s1", "A", 210, 1),
                StockItem("s2", "A", 250, 1),
            ],
            kerf=10,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        group_a = result.groups[0]
        total_cuts = sum(len(usage.cuts) for usage in group_a.usages)
        total_unmet = sum(unmet.quantity for unmet in group_a.unmet)

        # s1: 210 = 100 + 10(kerf) + 100 = 2 cuts, waste 0
        # s2: 250 = 100 + 10(kerf) + 100 = 2 cuts (but only 2 cuts available), waste 50
        # Demand: 4, Met: 4 (100 + 100 from s1, then 100 + 100 from s2)
        self.assertEqual(total_cuts, 4)
        self.assertEqual(total_unmet, 0)

    def test_workflow_unmet_demand_aggregation(self):
        """Test that unmet demand from multiple groups is handled correctly."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 5),
                DemandItem("d2", "B", 200, 3),
            ],
            stocks=[
                StockItem("s1", "A", 100, 1),
                StockItem("s2", "B", 300, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        group_a = next(g for g in result.groups if g.group == "A")
        group_b = next(g for g in result.groups if g.group == "B")

        # Group A: 1 stock of 100, demand 5x100 → met 1, unmet 4
        self.assertEqual(len(group_a.unmet), 1)
        self.assertEqual(group_a.unmet[0].quantity, 4)

        # Group B: 1 stock of 300, demand 3x200 → met 1, unmet 2
        self.assertEqual(len(group_b.unmet), 1)
        self.assertEqual(group_b.unmet[0].quantity, 2)

    def test_workflow_multiple_stock_instances(self):
        """Test stock quantity expansion in workflow."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 3),
            ],
            stocks=[
                StockItem("s1", "A", 150, 3),
            ],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        group_a = result.groups[0]
        # 3 demands of 100, 3 stocks of 150 → each stock handles 1 demand
        self.assertEqual(len(group_a.usages), 3)
        for usage in group_a.usages:
            self.assertEqual(len(usage.cuts), 1)
            self.assertEqual(usage.waste, 50)

    def test_workflow_empty_groups_are_excluded(self):
        """Test that groups with no demands or stocks are excluded."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("d1", "A", 100, 1),
            ],
            stocks=[
                StockItem("s1", "A", 200, 1),
                # No demand or stock for group B
            ],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        self.assertEqual(len(result.groups), 1)
        self.assertEqual(result.groups[0].group, "A")

    def test_workflow_mixed_scenario_with_exact_fit(self):
        """Test realistic scenario: multiple groups with waste and unmet."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("d1", "Steel", 150, 2),
                DemandItem("d2", "Aluminum", 75, 4),
            ],
            stocks=[
                StockItem("s1", "Steel", 320, 1),
                StockItem("s2", "Aluminum", 310, 1),
            ],
            kerf=10,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        self.assertEqual(len(result.groups), 2)

        # Steel: 150 + 10 + 150 = 310 (2 cuts from 320 stock), waste 10
        steel_group = next(g for g in result.groups if g.group == "Steel")
        self.assertEqual(len(steel_group.usages), 1)
        self.assertEqual(len(steel_group.usages[0].cuts), 2)
        self.assertEqual(steel_group.usages[0].waste, 10)

        # Aluminum: 75 + 10 + 75 + 10 + 75 = 245, leaves 65
        # Can't fit 4th cut (75 + 10 = 85 > 65), so 3 cuts and 1 unmet
        aluminum_group = next(g for g in result.groups if g.group == "Aluminum")
        self.assertEqual(len(aluminum_group.usages), 1)
        self.assertEqual(len(aluminum_group.usages[0].cuts), 3)
        self.assertEqual(aluminum_group.usages[0].waste, 65)
        self.assertEqual(len(aluminum_group.unmet), 1)
        self.assertEqual(aluminum_group.unmet[0].quantity, 1)

    def test_workflow_preserves_demand_ids_in_cuts(self):
        """Test that demand IDs are correctly preserved through the workflow."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("order-1", "A", 100, 1),
                DemandItem("order-2", "A", 50, 1),
            ],
            stocks=[
                StockItem("s1", "A", 200, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        group_a = result.groups[0]
        cuts = group_a.usages[0].cuts

        demand_ids = {cut.demand_id for cut in cuts}
        self.assertEqual(demand_ids, {"order-1", "order-2"})

    def test_workflow_largest_demand_processed_first(self):
        """Test that larger demands are prioritized (sorted descending)."""
        normalized = NormalizedInput(
            demands=[
                DemandItem("small", "A", 50, 1),
                DemandItem("large", "A", 150, 1),
            ],
            stocks=[
                StockItem("s1", "A", 200, 1),
            ],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        group_a = result.groups[0]
        cuts = group_a.usages[0].cuts

        # Both demands fit and are sorted descending by length (150 then 50)
        self.assertEqual(len(cuts), 2)
        self.assertEqual(cuts[0].length, 150)
        self.assertEqual(cuts[1].length, 50)

    def test_workflow_empty_input(self):
        """Test handling of empty input."""
        normalized = NormalizedInput(
            demands=[],
            stocks=[],
            kerf=0,
            unit_scale=0,
        )

        groups = group_inputs(normalized)
        result = solve_all(groups)

        self.assertEqual(len(result.groups), 0)


if __name__ == "__main__":
    unittest.main()
