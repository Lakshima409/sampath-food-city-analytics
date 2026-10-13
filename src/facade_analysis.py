"""Facade pattern for total-sales-distribution analysis.

One simple interface (SalesFacade.analyze_sales) hides the
load -> filter -> stats -> plot subsystem.
"""
from __future__ import annotations

import pandas as pd

from .data_loader import DataLoader
from .data_cleaner import DataCleaner


class _DataFilter:
    """Subsystem: keep positive sales, optionally restrict months."""

    def filter_data(self, data: pd.DataFrame, months: list[str] | None = None) -> pd.DataFrame:
        filtered = data[data["Sales"] > 0]
        if months:
            filtered = filtered[filtered["Month"].isin(months)]
        return filtered


class _DataPlotter:
    """Subsystem: histogram / KDE of the Sales column."""

    def plot_data(self, data: pd.DataFrame, save_path: str | None = None) -> None:
        from .visualizer import Visualizer

        Visualizer().distribution_chart(data["Sales"], save_path=save_path)


class SalesFacade:
    """Facade - the only class client code needs to touch."""

    def __init__(self, file_path: str = "data/sales_data.csv") -> None:
        self.file_path = file_path
        self._loader = DataLoader(file_path)
        self._cleaner = DataCleaner()
        self._filter = _DataFilter()
        self._plotter = _DataPlotter()

    def analyze_sales(
        self,
        months: list[str] | None = None,
        save_path: str | None = None,
    ) -> dict:
        raw = self._loader.load_data()
        cleaned = self._cleaner.clean(raw)
        filtered = self._filter.filter_data(cleaned, months)
        if filtered.empty:
            raise ValueError("No sales records left after filtering.")
        stats = {
            "count": int(filtered["Sales"].count()),
            "total": float(filtered["Sales"].sum()),
            "mean": float(filtered["Sales"].mean()),
            "median": float(filtered["Sales"].median()),
            "min": float(filtered["Sales"].min()),
            "max": float(filtered["Sales"].max()),
        }
        self._plotter.plot_data(filtered, save_path=save_path)
        return stats
