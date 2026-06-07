import os
import csv
import shutil
from datetime import datetime

from model.report_model import SolveReport
from model.export_model import CutPlanExportRow
from service.denormalization import denormalize_length


def write_csv(report: SolveReport):
    output_folder = create_output_folder()
    pattern_file = os.path.join(
        output_folder,
        "cutting_patterns.csv"
        )
    text_file = os.path.join(
        output_folder,
        "cutting_list_prt.txt"
    )

    cutting_pattern = flatten_report(report, report.unit_scale)

    export_patterns(pattern_file, cutting_pattern)
    export_prf(report, text_file)

    return output_folder

def flatten_report(report: SolveReport, unit_scale: int):

    rows = []

    for stock in report.usages:
        for i, cut in enumerate(stock.cuts):
            rows.append(
                CutPlanExportRow(
                    group=stock.group,
                    usage_id=stock.usage_id,
                    stock_id=stock.stock_id,
                    stock_length=denormalize_length(stock.stock_length, unit_scale),
                    demand_id=cut.demand_id,
                    cut_length=denormalize_length(cut.length, unit_scale),
                    waste=denormalize_length(stock.waste, unit_scale) if i == len(stock.cuts)-1 else None
                )
            )

    return rows

def create_output_folder():
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = os.path.join("data/output", ts)
    os.makedirs(folder, exist_ok=True)
    return folder

def export_patterns(path, patterns):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "group",
            "usage_id",
            "stock_id",
            "stock_length",
            "demand_id",
            "cut_length",
            "waste"
        ])

        for row in patterns:
            writer.writerow([
                row.group,
                row.usage_id,
                row.stock_id,
                row.stock_length,
                row.demand_id,
                row.cut_length,
                row.waste
            ])

def export_summary(self, path, patterns):
    total_stock = len(patterns)
    total_used = sum(p.used_length() for p in patterns)
    total_waste = sum(p.remaining() for p in patterns)
    efficiency = total_used / (total_used + total_waste)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["stocks_used", total_stock])
        writer.writerow(["total_used_length", total_used])
        writer.writerow(["total_waste", total_waste])
        writer.writerow(["efficiency", efficiency])


def copy_inputs(self, folder, stock_file, demand_file):
    shutil.copy(stock_file, os.path.join(folder, "stocks.csv"))
    shutil.copy(demand_file, os.path.join(folder, "demand.csv"))

def export_prf(report: SolveReport, path):
    unit_scale = report.unit_scale
    grouped_patterns = _group_patterns(report.usages)

    with open(path, "w", encoding="utf-8") as f:
        for group_name, patterns in grouped_patterns.items():
            f.write(f"=== {group_name} ===\n")

            total_stocks = 0
            total_stock_length = 0
            total_waste = 0

            for pattern in patterns:
                stock_len = denormalize_length(pattern['stock_length'], unit_scale)
                count = pattern['count']
                f.write(f"- {count} number of {stock_len}mm cut into:\n")

                for demand_id, cut_count in pattern['demand_cuts'].items():
                    cut_len = denormalize_length(cut_count['length'], unit_scale)
                    f.write(f"  > {cut_count['count']} x {cut_len}mm for {demand_id}\n")

                waste = denormalize_length(pattern['waste_per_stock'], unit_scale)
                f.write(f"  > balance {waste}mm waste\n")

                total_stocks += count
                total_stock_length += count * pattern['stock_length']
                total_waste += count * pattern['waste_per_stock']

            total_used = total_stock_length - total_waste
            utilization = (total_used / total_stock_length * 100) if total_stock_length > 0 else 0

            f.write(f"\nSummary:\n")
            f.write(f"  Total stocks: {total_stocks}\n")
            f.write(f"  Total length: {denormalize_length(total_stock_length, unit_scale)}mm\n")
            f.write(f"  Total used: {denormalize_length(total_used, unit_scale)}mm\n")
            f.write(f"  Total waste: {denormalize_length(total_waste, unit_scale)}mm\n")
            f.write(f"  Utilization: {utilization:.1f}%\n")
            f.write("\n")


def _group_patterns(usages):
    patterns_dict = {}

    for usage in usages:
        group = usage.group
        if group not in patterns_dict:
            patterns_dict[group] = {}

        pattern_key = _make_pattern_key(usage.cuts)

        if pattern_key not in patterns_dict[group]:
            patterns_dict[group][pattern_key] = {
                'stock_length': usage.stock_length,
                'count': 0,
                'demand_cuts': {},
                'waste_per_stock': usage.waste
            }

        pattern = patterns_dict[group][pattern_key]
        pattern['count'] += 1

        for cut in usage.cuts:
            if cut.demand_id not in pattern['demand_cuts']:
                pattern['demand_cuts'][cut.demand_id] = {
                    'length': cut.length,
                    'count': 0
                }
            pattern['demand_cuts'][cut.demand_id]['count'] += 1

    result = {}
    for group, patterns_map in patterns_dict.items():
        result[group] = list(patterns_map.values())

    return result


def _make_pattern_key(cuts):
    return tuple((cut.demand_id, cut.length) for cut in cuts)