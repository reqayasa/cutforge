import logging
from core.csv_loader import Forge1DCSVLoader
from solver.forge1d_ffd_solver import Forge1DFFDSolver
from core.result_exporter import Forge1DResultExporter
from core.logger import CutForgeLogger

class SolverController:
    def __init__(self, window):
        self.window = window

        self.logger = logging.getLogger("cutforge")

        self.loader = Forge1DCSVLoader()
        self.solver = Forge1DFFDSolver()
        self.exporter = Forge1DResultExporter()

        self.connect_events()

    def connect_events(self):
        tab = self.window.forge1d_tab
        tab.solve_button.clicked.connect(self.solve_1d)

    def solve_1d(self):
        tab = self.window.forge1d_tab

        stock_path = tab.stock_path.text()
        demand_path = tab.demand_path.text()
        algorithm  = tab.algorithm.currentText()

        self.logger.info("Loading CSV...")

        try:
            dataset = self.loader.load(stock_path, demand_path)
        except Exception as e:
            self.logger.error("Loading CSV error: %s", e)
            return
        
        try:
            patterns =self.run_solver(dataset, algorithm)
        except Exception as e:
            self.logger.error("Solver error: %s", e)
            return
        
        self.logger.info("Exporting results...")

        try:
            output_folder = self.exporter.export(
                patterns,
                dataset,
                algorithm.lower(),
                stock_path,
                demand_path,
            )
        except Exception as e:
            self.logger.error("Export error: %s", e)
            return
        
        self.update_summary(patterns)
        self.logger.info("Done. Output saved to: %s", output_folder)

    def run_solver(self, dataset, algorithm):
        if algorithm == "FFD":
            return self.solver.solve(dataset)
        else:
            raise ValueError(f"Algorithm not implemented: {algorithm}")
    
    def update_summary(self, patterns):
        tab = self.window.forge1d_tab

        total_stock = len(patterns)

        total_used = sum(p.used_length() for p in patterns)
        total_waste = sum(p.remaining() for p in patterns)

        efficiency = total_used / (total_used + total_waste)

        tab.total_parts.setText(str(total_used))
        tab.sheets_used.setText(str(total_stock))
        tab.total_waste.setText(str(total_waste))
        tab.efficiency.setText(f"{efficiency*100:.2f}%")