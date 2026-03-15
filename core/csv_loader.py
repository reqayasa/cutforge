import pandas as pd

from model.forge1d_part import Forge1DPart
from model.forge1d_stock import Forge1DStock
from model.forge1d_dataset import Forge1DDataset

from core.length_scaler import LengthScaler

class Forge1DCSVLoader:
    def __init__(self):
        self.scaler = LengthScaler()

    def load(self, stock_path, demand_path):
        stocks_df = pd.read_csv(stock_path)
        demands_df = pd.read_csv(demand_path)

        stocks_df.columns = (stocks_df.columns.str.strip().str.lower())
        demands_df.columns = (demands_df.columns.str.strip().str.lower())

        # print(stocks_df.columns.tolist())
        # for c in stocks_df.columns:
        #     print(repr(c))

        self.validate_stock(stocks_df)
        self.validate_demand(demands_df)

        lengths = []

        lengths.extend(stocks_df["length"].tolist())
        lengths.extend(demands_df["length"].tolist())

        self.scaler.detect_scale(lengths)

        stocks = self.parse_stock(stocks_df)
        parts = self.parse_parts(demands_df)

        dateset = Forge1DDataset(
            stocks,
            parts,
            self.scaler.scale
        )

        return dateset
    
    def validate_stock(self, df):
        required = ["stock_id", "length", "qty"]

        for col in required:
            if col not in df.columns:
                raise ValueError(f"stocks.csv missing column: {col}")

    def validate_demand(self, df):
        required = ["part_id", "length", "qty"]

        for col in required:
            if col not in df.columns:
                raise ValueError(f"demand.csv missing column: {col}")
            
    def parse_stock(self, df):
        stocks = []
        
        for _, row in df.iterrows():
            length_int = self.scaler.to_int(row["length"])

            stock = Forge1DStock(
                row["stock_id"],
                length_int,
                int(row["qty"])
            )

            stocks.append(stock)
        
        return stocks
            
    def parse_parts(self, df):
        parts = []
        
        for _, row in df.iterrows():
            length_int = self.scaler.to_int(row["length"])

            part = Forge1DPart(
                row["part_id"],
                length_int,
                int(row["qty"])
            )

            parts.append(part)
        
        return parts