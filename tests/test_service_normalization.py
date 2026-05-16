from decimal import Decimal

import pytest

from service.normalization import (
    NormalizationError, 
    parse_quantity, 
    parse_decimal, 
    normalize_group, 
    normalize_id,
    detect_scale,
    normalize_stock_row,
    normalize_demand_row,
    normalize_inputs
)
from model.raw_input_model import RawDemandRow, RawStockRow
from model.internal_model import NormalizeOptions, SolveOptions


class TestParseQty:

    def test_integer_string(self):
        assert parse_quantity("3") == 3

    def test_zero_is_valid(self):
        assert parse_quantity("0") == 0

    def test_decimal_zero_is_valid(self):
        assert parse_quantity("3.0") == 3

    def test_comma_decimal_zero_is_valid(self):
        assert parse_quantity("4,000") == 4

    def test_whitespace_is_allowed(self):
        assert parse_quantity("  7.0  ") == 7

    def test_non_zero_fraction_raises_error(self):
        with pytest.raises(NormalizationError):
            parse_quantity("3.2")

    def test_negative_value_raises_error(self):
        with pytest.raises(NormalizationError):
            parse_quantity("-1")

    def test_non_numeric_string_raises_error(self):
        with pytest.raises(NormalizationError):
            parse_quantity("abc")

    def test_empty_string_raises_error(self):
        with pytest.raises(NormalizationError):
            parse_quantity("")


class TestParseDecimal:

    def test_integer_string(self):
        value, rounded = parse_decimal("1200", max_precision=3)

        assert value == Decimal("1200")
        assert rounded is False

    def test_decimal_string(self):
        value, rounded = parse_decimal("12.5", max_precision=3)

        assert value == Decimal("12.5")
        assert rounded is False

    def test_comma_decimal_string(self):
        value, rounded = parse_decimal("12,5", max_precision=3)

        assert value == Decimal("12.5")
        assert rounded is False

    def test_whitespace_is_allowed(self):
        value, rounded = parse_decimal("  12.5  ", max_precision=3)

        assert value == Decimal("12.5")
        assert rounded is False

    def test_trailing_zero_is_normalized(self):
        value, rounded = parse_decimal("12.500", max_precision=3)

        assert value == Decimal("12.5")
        assert value.as_tuple().exponent == -1
        assert rounded is False

    def test_rounding_occurs_when_precision_exceeded(self):
        value, rounded = parse_decimal("12.34567", max_precision=3)

        assert value == Decimal("12.346")
        assert rounded is True

    def test_rounding_noise_from_export(self):
        value, rounded = parse_decimal("1199.999999", max_precision=3)

        assert value == Decimal("1200")
        assert rounded is True

    def test_zero_is_valid(self):
        value, rounded = parse_decimal("0", max_precision=3)

        assert value == Decimal("0")
        assert rounded is False

    def test_negative_value_is_valid_for_parser(self):
        value, rounded = parse_decimal("-0.5", max_precision=3)

        assert value == Decimal("-0.5")
        assert rounded is False

    def test_non_numeric_string_raises_error(self):
        with pytest.raises(NormalizationError):
            parse_decimal("abc", max_precision=3)

    def test_empty_string_raises_error(self):
        with pytest.raises(NormalizationError):
            parse_decimal("", max_precision=3)


class TestNormalizeGroup:

    def test_keep_existing_group(self):
        value, defaulted = normalize_group("A")

        assert value == "A"
        assert defaulted is False

    def test_strip_whitespace(self):
        value, defaulted = normalize_group("  Hollow 100x100  ")

        assert value == "Hollow 100x100"
        assert defaulted is False

    def test_empty_string_uses_default(self):
        value, defaulted = normalize_group("")

        assert value == "default"
        assert defaulted is True

    def test_whitespace_only_uses_default(self):
        value, defaulted = normalize_group("   ")

        assert value == "default"
        assert defaulted is True


class TestNormalizeId:

    def test_keep_existing_id(self):
        value, generated = normalize_id("P-01", prefix="part", index=1)

        assert value == "P-01"
        assert generated is False

    def test_strip_whitespace(self):
        value, generated = normalize_id("   P-01   ", prefix="part", index=1)

        assert value == "P-01"
        assert generated is False

    def test_empty_string_generates_id(self):
        value, generated = normalize_id("", prefix="part", index=2)

        assert value == "part-0002"
        assert generated is True

    def test_whitespace_only_generates_id(self):
        value, generated = normalize_id("   ", prefix="part", index=3)

        assert value == "part-0003"
        assert generated is True

    def test_stock_prefix_is_used(self):
        value, generated = normalize_id("", prefix="stock", index=4)

        assert value == "stock-0004"
        assert generated is True

    def test_human_facing_index(self):
        value, generated = normalize_id("", prefix="part", index=1)

        assert value == "part-0001"
        assert generated is True


class TestNormalizeDemandRow:

    def test_normal_row(self):
        row = RawDemandRow(
            id="P-01",
            group="A",
            length="1200",
            quantity="3",
        )

        data, warnings = normalize_demand_row(
            row=row,
            row_number=1,
            max_precision=3,
        )

        assert data["id"] == "P-01"
        assert data["group"] == "A"
        assert data["length"] == Decimal("1200")
        assert data["quantity"] == 3
        assert warnings == []

    def test_missing_id_is_generated(self):
        row = RawDemandRow(
            id="",
            group="A",
            length="1200",
            quantity="3",
        )

        data, warnings = normalize_demand_row(
            row=row,
            row_number=2,
            max_precision=3,
        )

        assert data["id"] == "part-0002"
        assert len(warnings) == 1

    def test_missing_group_uses_default(self):
        row = RawDemandRow(
            id="P-01",
            group="",
            length="1200",
            quantity="3",
        )

        data, warnings = normalize_demand_row(
            row=row,
            row_number=3,
            max_precision=3,
        )

        assert data["group"] == "default"
        assert len(warnings) == 1

    def test_rounding_creates_warning(self):
        row = RawDemandRow(
            id="P-01",
            group="A",
            length="1199.999999",
            quantity="3",
        )

        data, warnings = normalize_demand_row(
            row=row,
            row_number=4,
            max_precision=3,
        )

        assert data["length"] == Decimal("1200")
        assert len(warnings) == 1

    def test_zero_qty_is_valid(self):
        row = RawDemandRow(
            id="P-01",
            group="A",
            length="1200",
            quantity="0",
        )

        data, warnings = normalize_demand_row(
            row=row,
            row_number=5,
            max_precision=3,
        )

        assert data["quantity"] == 0
        assert len(warnings) == 1

    def test_invalid_length_raises_error(self):
        row = RawDemandRow(
            id="P-01",
            group="A",
            length="abc",
            quantity="3",
        )

        with pytest.raises(NormalizationError):
            normalize_demand_row(
                row=row,
                row_number=6,
                max_precision=3,
            )

    def test_non_positive_length_raises_error(self):
        row = RawDemandRow(
            id="P-01",
            group="A",
            length="0",
            quantity="3",
        )

        with pytest.raises(NormalizationError):
            normalize_demand_row(
                row=row,
                row_number=7,
                max_precision=3,
            )

    def test_invalid_qty_raises_error(self):
        row = RawDemandRow(
            id="P-01",
            group="A",
            length="1200",
            quantity="3.2",
        )

        with pytest.raises(NormalizationError):
            normalize_demand_row(
                row=row,
                row_number=8,
                max_precision=3,
            )


class TestDetectScale:

    def test_integer_values(self):
        unit_scale = detect_scale([
            Decimal("1200"),
            Decimal("6000"),
        ])

        assert unit_scale == 1

    def test_single_decimal_place(self):
        unit_scale = detect_scale([
            Decimal("12.5"),
            Decimal("6000"),
        ])

        assert unit_scale == 10

    def test_multiple_decimal_places(self):
        unit_scale = detect_scale([
            Decimal("12.5"),
            Decimal("0.25"),
            Decimal("1200"),
        ])

        assert unit_scale == 100

    def test_trailing_zero_does_not_increase_scale(self):
        unit_scale = detect_scale([
            Decimal("12.5"),
            Decimal("1200"),
        ])

        assert unit_scale == 10

    def test_zero_value_does_not_break_scale(self):
        unit_scale = detect_scale([
            Decimal("0"),
            Decimal("12.25"),
        ])

        assert unit_scale == 100

    def test_empty_values_defaults_to_one(self):
        unit_scale = detect_scale([])

        assert unit_scale == 1


class TestNormalizeStockRow:

    def test_normal_row(self):
        row = RawStockRow(
            id="S-01",
            group="A",
            length="6000",
            quantity="2",
        )

        data, warnings = normalize_stock_row(
            row=row,
            row_number=1,
            max_precision=3,
        )

        assert data["id"] == "S-01"
        assert data["group"] == "A"
        assert data["length"] == Decimal("6000")
        assert data["quantity"] == 2
        assert warnings == []

    def test_missing_id_is_generated(self):
        row = RawStockRow(
            id="",
            group="A",
            length="6000",
            quantity="2",
        )

        data, warnings = normalize_stock_row(
            row=row,
            row_number=2,
            max_precision=3,
        )

        assert data["id"] == "stock-0002"
        assert len(warnings) == 1

    def test_missing_group_uses_default(self):
        row = RawStockRow(
            id="S-01",
            group="",
            length="6000",
            quantity="2",
        )

        data, warnings = normalize_stock_row(
            row=row,
            row_number=3,
            max_precision=3,
        )

        assert data["group"] == "default"
        assert len(warnings) == 1

    def test_rounding_creates_warning(self):
        row = RawStockRow(
            id="S-01",
            group="A",
            length="5999.999999",
            quantity="2",
        )

        data, warnings = normalize_stock_row(
            row=row,
            row_number=4,
            max_precision=3,
        )

        assert data["length"] == Decimal("6000")
        assert len(warnings) == 1

    def test_zero_qty_is_valid(self):
        row = RawStockRow(
            id="S-01",
            group="A",
            length="6000",
            quantity="0",
        )

        data, warnings = normalize_stock_row(
            row=row,
            row_number=5,
            max_precision=3,
        )

        assert data["quantity"] == 0
        assert len(warnings) == 1

    def test_non_positive_length_raises_error(self):
        row = RawStockRow(
            id="S-01",
            group="A",
            length="0",
            quantity="2",
        )

        with pytest.raises(NormalizationError):
            normalize_stock_row(
                row=row,
                row_number=6,
                max_precision=3,
            )

    def test_invalid_qty_raises_error(self):
        row = RawStockRow(
            id="S-01",
            group="A",
            length="6000",
            quantity="2.5",
        )

        with pytest.raises(NormalizationError):
            normalize_stock_row(
                row=row,
                row_number=7,
                max_precision=3,
            )
        

class TestNormalizeInputs:

    def test_basic_normalization(self):
        raw_demands = [
            RawDemandRow(
                id="P-01",
                group="A",
                length="1200.5",
                quantity="2",
            )
        ]

        raw_stocks = [
            RawStockRow(
                id="S-01",
                group="A",
                length="6000",
                quantity="1",
            )
        ]

        result = normalize_inputs(
            raw_demands=raw_demands,
            raw_stocks=raw_stocks,
            normalize_options=NormalizeOptions(max_precision=3),
            solve_options=SolveOptions(kerf="0.5"),
        )

        assert result.data.unit_scale == 10
        assert result.data.kerf == 5

        assert result.data.demands[0].length == 12005
        assert result.data.demands[0].quantity == 2

        assert result.data.stocks[0].length == 60000
        assert result.data.stocks[0].quantity == 1

    def test_scale_detects_max_precision_across_all_values(self):
        raw_demands = [
            RawDemandRow(
                id="P-01",
                group="A",
                length="12.5",
                quantity="1",
            )
        ]

        raw_stocks = [
            RawStockRow(
                id="S-01",
                group="A",
                length="100.25",
                quantity="1",
            )
        ]

        result = normalize_inputs(
            raw_demands=raw_demands,
            raw_stocks=raw_stocks,
            normalize_options=NormalizeOptions(max_precision=3),
            solve_options=SolveOptions(kerf="0"),
        )

        assert result.data.unit_scale == 100
        assert result.data.demands[0].length == 1250
        assert result.data.stocks[0].length == 10025

    def test_kerf_affects_scale_detection(self):
        raw_demands = [
            RawDemandRow(
                id="P-01",
                group="A",
                length="1200",
                quantity="1",
            )
        ]

        raw_stocks = [
            RawStockRow(
                id="S-01",
                group="A",
                length="6000",
                quantity="1",
            )
        ]

        result = normalize_inputs(
            raw_demands=raw_demands,
            raw_stocks=raw_stocks,
            normalize_options=NormalizeOptions(max_precision=3),
            solve_options=SolveOptions(kerf="0.25"),
        )

        assert result.data.unit_scale == 100
        assert result.data.kerf == 25

    def test_warnings_are_collected(self):
        raw_demands = [
            RawDemandRow(
                id="",
                group="",
                length="1199.999999",
                quantity="0",
            )
        ]

        raw_stocks = [
            RawStockRow(
                id="",
                group="",
                length="6000",
                quantity="0",
            )
        ]

        result = normalize_inputs(
            raw_demands=raw_demands,
            raw_stocks=raw_stocks,
            normalize_options=NormalizeOptions(max_precision=3),
            solve_options=SolveOptions(kerf="0"),
        )

        assert len(result.warnings) >= 1


def test_normalize_pipeline_end_to_end():
    raw_demands = [
        RawDemandRow(
            id="",
            group="",
            length="1199.999999",
            quantity="2",
        ),
        RawDemandRow(
            id="P-02",
            group="A",
            length="500",
            quantity="0",
        ),
    ]

    raw_stocks = [
        RawStockRow(
            id="",
            group="",
            length="6000",
            quantity="1",
        ),
    ]

    result = normalize_inputs(
        raw_demands=raw_demands,
        raw_stocks=raw_stocks,
        normalize_options=NormalizeOptions(max_precision=3),
        solve_options=SolveOptions(kerf="0.5"),
    )

    assert result.data.unit_scale == 10
    assert result.data.kerf == 5

    assert result.data.demands[0].id == "part-0001"
    assert result.data.demands[0].group == "default"
    assert result.data.demands[0].length == 12000
    assert result.data.demands[0].quantity == 2

    assert result.data.demands[1].id == "P-02"
    assert result.data.demands[1].length == 5000
    assert result.data.demands[1].quantity == 0

    assert result.data.stocks[0].id == "stock-0001"
    assert result.data.stocks[0].group == "default"
    assert result.data.stocks[0].length == 60000

    assert len(result.warnings) >= 1