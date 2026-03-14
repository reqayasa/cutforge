from solver.optimizer_1d import CuttingStock1D

class SolverController:
    def __init__(self, window):
        self.window = window
        self.connect_events()

    def connect_events(self):
        tab = self.window.forge1d_tab
        tab.solve_button.clicked.connect(self.solve_1d)

    def solve_1d(self):
        tab = self.window.forge1d_tab

        stock = tab.stock_path.text()
        demand = tab.demand_path.text()
        algo = tab.algorithm.currentText()

        print("Running Forge 1D")

        print("Stock:", stock)
        print("Demand:", demand)
        print("Algorithm:", algo)