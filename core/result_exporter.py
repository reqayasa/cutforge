import os
import csv
import shutil
from datetime import datetime

class Forge1DResultExporter:
    def __init__(self, base_output = "data/output"):
        self.base_output = base_output

    def export(self, patterns, dataset, algorithm, stock_file, demand_file):
        run_folder = self.create_run_folder()
        pattern_file = os.path.join(
            run_folder,
            f"cutting_patterns_{algorithm}.csv"
            )
        
        summary_file = os.path.join(
            run_folder,
            "cutting_summary.csv"
        )

        self.export_patterns(pattern_file, patterns, dataset)
        self.export_summary(summary_file, patterns)
        self.copy_inputs(run_folder, stock_file, demand_file)

        return run_folder
    
    
    def create_run_folder(self):
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = os.path.join(self.base_output, ts)
        os.makedirs(folder, exist_ok=True)
        return folder
    
    def export_patterns(self, path, patterns, dataset):
        scale = dataset.scale

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "pattern_id",
                "parts",
                "used_length",
                "waste"
            ])

            for i, p in enumerate(patterns, start=1):
                parts_real = [x / scale for x in p.parts]

                used = p.used_length() / scale
                waste = p.remaining() / scale

                writer.writerow([
                    i,
                    "|".join(map(str, parts_real)),
                    used,
                    waste
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