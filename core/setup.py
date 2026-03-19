import os
import pandas as pd
import logging

def setup_environment():
    logger = logging.getLogger("cutforge")

    base_path = "data"

    input_path = os.path.join(base_path, "input")
    output_path = os.path.join(base_path, "output")
    log_path = os.path.join(base_path, "logs")

    logger.info("Checking data directories...")

    os.makedirs(input_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(log_path, exist_ok=True)

    logger.info("Input folder ready")

    stock_file = os.path.join(input_path, "forge1d_stocks.csv")
    demand_file = os.path.join(input_path, "forge1d_demand.csv")

    # create template if not exist
    if not os.path.exists(stock_file):

        df_stock = pd.DataFrame({
            "stock_id": ["S1"],
            "length": [6000],
            "qty": [10]
        })

        df_stock.to_csv(stock_file, index=False)

    if not os.path.exists(demand_file):

        df_demand = pd.DataFrame({
            "part_id": ["P1", "P2"],
            "length": [2000, 1500],
            "qty": [5, 8]
        })

        df_demand.to_csv(demand_file, index=False)
    
    logger.info("Template CSV created (if missing)")