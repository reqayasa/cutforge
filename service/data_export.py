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

    cutting_pattern = flatten_report(report, report.unit_scale)

    export_patterns(pattern_file, cutting_pattern)

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