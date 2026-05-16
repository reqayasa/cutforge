import unittest

from model.solver_model import (
    SolveResult,
    GroupSolveResult,
    StockUsage,
    CutAssignment,
    UnmetDemand,
)
from service.reporting import build_report


class TestReporting(unittest.TestCase):

    def test_builds_stock_rows(self):
        result = SolveResult(
            groups=[
                GroupSolveResult(
                    group="A",
                    usages=[
                        StockUsage(
                            stock_id="s1",
                            stock_length=500,
                            cuts=[
                                CutAssignment("d1", 100),
                                CutAssignment("d2", 150),
                            ],
                            waste=250,
                        )
                    ],
                    unmet=[],
                )
            ]
        )

        report = build_report(result)

        self.assertEqual(len(report.stock_rows), 1)

        row = report.stock_rows[0]

        self.assertEqual(row.group, "A")
        self.assertEqual(row.stock_id, "s1")
        self.assertEqual(row.stock_length, 500)
        self.assertEqual(row.used_length, 250)
        self.assertEqual(row.waste, 250)
        self.assertEqual(row.cut_count, 2)

    def test_builds_unmet_rows(self):
        result = SolveResult(
            groups=[
                GroupSolveResult(
                    group="A",
                    usages=[],
                    unmet=[
                        UnmetDemand(
                            demand_id="d1",
                            length=100,
                            quantity=2,
                        )
                    ],
                )
            ]
        )

        report = build_report(result)

        self.assertEqual(len(report.unmet_rows), 1)

        row = report.unmet_rows[0]

        self.assertEqual(row.group, "A")
        self.assertEqual(row.demand_id, "d1")
        self.assertEqual(row.length, 100)
        self.assertEqual(row.quantity, 2)

    def test_empty_result(self):
        result = SolveResult(groups=[])

        report = build_report(result)

        self.assertEqual(report.stock_rows, [])
        self.assertEqual(report.unmet_rows, [])