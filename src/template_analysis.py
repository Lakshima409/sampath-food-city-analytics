"""Template pattern for product price analysis.

The skeleton (load -> preprocess -> filter -> analyze -> plot) is fixed in
DataAnalysisTemplate; subclasses only fill in the varying steps.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from .data_loader import DataLoader
from .data_cleaner import DataCleaner


class DataAnalysisTemplate(ABC):
    """Template base class."""

    def __init__(self) -> None:
        self.data: pd.DataFrame | None = None
        self.filtered_data: pd.DataFrame | None = None

    def load_data(self, file_path: str) -> None:
        raw = DataLoader(file_path).load_data()
        self.data = DataCleaner().clean(raw)

    def preprocess_data(self) -> None:
        """Hook - default does nothing."""

    def filter_data(self) -> None:
        """Hook - default keeps everything."""

    @abstractmethod
    def analyze_data(self) -> pd.Series:
        """Compute the result."""

    @abstractmethod
    def plot_data(self, result: pd.Series, save_path: str | None = None) -> None:
        """Visualise the result."""

    def execute(self, file_path: str, save_path: str | None = None) -> pd.Series:
        """The template method - fixed workflow, varying steps."""
        self.load_data(file_path)
        self.preprocess_data()
        self.filter_data()
        result = self.analyze_data()
        self.plot_data(result, save_path=save_path)
        return result


class PriceAnalysis(DataAnalysisTemplate):
    """Average unit price per month for one category (default Electronics)."""

    def __init__(self, category: str = "Electronics") -> None:
        super().__init__()
        self.category = category

    def preprocess_data(self) -> None:
        assert self.data is not None
        # AveragePrice = Sales / Quantity (guard divide-by-zero)
        self.data["AveragePrice"] = self.data.apply(
            lambda r: r["Sales"] / r["Quantity"] if r["Quantity"] else r["Price"],
            axis=1,
        )

    def filter_data(self) -> None:
        assert self.data is not None
        self.filtered_data = self.data[self.data["Category"] == self.category]
        if self.filtered_data.empty:
            raise ValueError(f"No rows found for category '{self.category}'.")

    def analyze_data(self) -> pd.Series:
        assert self.filtered_data is not None
        result = self.filtered_data.groupby("Month")["AveragePrice"].mean()
        order = [m for m in ("January", "February") if m in result.index]
        return result.reindex(order or result.index)

    def plot_data(self, result: pd.Series, save_path: str | None = None) -> None:
        from .visualizer import Visualizer

        Visualizer().line_chart(
            result,
            title=f"Average Price Analysis ({self.category})",
            xlabel="Month",
            ylabel="Average Price (Rs.)",
            save_path=save_path,
        )
