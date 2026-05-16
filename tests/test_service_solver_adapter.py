import unittest
from unittest.mock import patch

from model.internal_model import GroupInput
from model.solver_model import GroupSolveResult
from service.solver_adapter import solve_all


class TestSolverAdapter(unittest.TestCase):

    @patch("service.solver_adapter.solve_group")
    def test_calls_solver_for_each_group(self, mock_solve_group):
        g1 = GroupInput(
            group="A",
            demands=[],
            stocks=[],
            kerf=0,
        )

        g2 = GroupInput(
            group="B",
            demands=[],
            stocks=[],
            kerf=0,
        )

        mock_solve_group.side_effect = [
            GroupSolveResult(
                group="A",
                usages=[],
                unmet=[]
                ),
            GroupSolveResult(
                group="B",
                usages=[],
                unmet=[]
                ),
        ]

        result = solve_all([g1, g2])

        self.assertEqual(mock_solve_group.call_count, 2)
        self.assertEqual(len(result.groups), 2)
        self.assertEqual(result.groups[0].group, "A")
        self.assertEqual(result.groups[1].group, "B")

    @patch("service.solver_adapter.solve_group")
    def test_empty_input_returns_empty_result(self, mock_solve_group):
        result = solve_all([])

        mock_solve_group.assert_not_called()
        self.assertEqual(result.groups, [])