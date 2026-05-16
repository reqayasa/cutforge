import pytest

from service.cut_service import CutService

from model.raw_input_model import RawDemandRow, RawStockRow
from model.internal_model import NormalizeOptions, SolveOptions
from model.report_model import SolveReport


def test_cut_sercice_return_report():
    service = CutService()

    demands = [
        RawDemandRow(
            id="D1",
            group="A",
            length="1000",
            quantity="2",
        )
    ]

    stocks = [
        RawStockRow(
            id="S1",
            group="A",
            length="3000",
            quantity="1",
        )
    ]

    report = service.solve(
        raw_demands=demands,
        raw_stocks=stocks,
        normalize_options=NormalizeOptions(),
        solve_options=SolveOptions(kerf="0"),
    )


    assert isinstance(report, SolveReport)

    assert len(report.stock_rows) == 1
    assert len(report.unmet_rows) == 0

    row = report.stock_rows[0]

    assert row.group == "A"
    assert row.stock_id == "S1"
    assert row.stock_length == 3000
    assert row.used_length == 2000
    assert row.cut_count == 2

def test_cut_service_creates_unmet_report():
    service = CutService()

    demands = [
        RawDemandRow(
            id="D1",
            group="A",
            length="5000",
            quantity="1",
        )
    ]

    stocks = [
        RawStockRow(
            id="S1",
            group="A",
            length="3000",
            quantity="1",
        )
    ]

    report = service.solve(
        raw_demands=demands,
        raw_stocks=stocks,
        normalize_options=NormalizeOptions(),
        solve_options=SolveOptions(),
    )

    assert len(report.stock_rows) == 0
    assert len(report.unmet_rows) == 1

    unmet = report.unmet_rows[0]

    assert unmet.group == "A"
    assert unmet.demand_id == "D1"
    assert unmet.length == 5000
    assert unmet.quantity == 1

def test_cut_service_solves_multiple_groups():
    service = CutService()

    demands = [
        RawDemandRow(
            id="D1",
            group="A",
            length="1000",
            quantity="1",
        ),
        RawDemandRow(
            id="D2",
            group="B",
            length="2000",
            quantity="1",
        ),
    ]

    stocks = [
        RawStockRow(
            id="S1",
            group="A",
            length="3000",
            quantity="1",
        ),
        RawStockRow(
            id="S2",
            group="B",
            length="3000",
            quantity="1",
        ),
    ]

    report = service.solve(
        raw_demands=demands,
        raw_stocks=stocks,
        normalize_options=NormalizeOptions(),
        solve_options=SolveOptions(),
    )

    assert len(report.stock_rows) == 2

    groups = {row.group for row in report.stock_rows}

    assert groups == {"A", "B"}

def test_cut_service_handles_empty_input():
    service = CutService()

    report = service.solve(
        raw_demands=[],
        raw_stocks=[],
        normalize_options=NormalizeOptions(),
        solve_options=SolveOptions(),
    )

    assert len(report.stock_rows) == 0
    assert len(report.unmet_rows) == 0