"""Data loading (SRP) - only responsible for reading CSV files."""
from __future__ import annotations

import pandas as pd


class DataLoader:
    """Load sales data from a CSV file."""

    def __init__(self, file_path: str = "data/sales_data.csv") -> None:
        self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        """Read CSV and return a DataFrame.

        Raises:
            FileNotFoundError: if the CSV does not exist.
            ValueError: if the file is empty or missing required columns.
        """
        try:
            data = pd.read_csv(self.file_path)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Data file not found: {self.file_path}") from exc
        if data.empty:
            raise ValueError("Sales data file is empty.")
        return data
