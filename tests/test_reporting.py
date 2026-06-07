import pytest

from model.solver_model import (
    SolveResult,
    GroupSolveResult,
    StockUsage,
    CutPiece,
    UnmetDemand,
)

from service.reporting import build_report


def test_build_stock_rows():
    result = SolveResult(
        groups=[
            GroupSolveResult(
                group="A",
                usages=[
                    StockUsage(
                        stock_id="S1",
                        stock_length=500,
                        cuts=[
                            CutPiece("D1", 100),
                            CutPiece("D2", 150),
                        ],
                        waste=250,
                    )
                ],
                unmet=[],
            )
        ]
    )

    report = build_report(result)

    assert len(report.usages) == 1

    row = report.usages[0]

    assert row.group == "A"
    assert row.stock_id == "S1"
    assert row.stock_length == 500
    assert row.used_length == 250
    assert row.waste == 250

    assert row.cuts == [
        CutPiece(
            demand_id="D1",
            length=100,
        ),
        CutPiece(
            demand_id="D2",
            length=150,
        ),
    ]


def test_build_unmet_rows():
    result = SolveResult(
        groups=[
            GroupSolveResult(
                group="A",
                usages=[],
                unmet=[
                    UnmetDemand(
                        demand_id="D1",
                        length=100,
                        quantity=2,
                    )
                ],
            )
        ]
    )

    report = build_report(result)

    assert len(report.unmet_rows) == 1

    row = report.unmet_rows[0]

    assert row.group == "A"
    assert row.demand_id == "D1"
    assert row.length == 100
    assert row.quantity == 2


def test_empty_result():
    result = SolveResult(groups=[])

    report = build_report(result)

    assert report.usages == []
    assert report.unmet_rows == []