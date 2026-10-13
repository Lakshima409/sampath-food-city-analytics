"""Factory pattern for branch-based sales analyses (monthly + weekly).

OCP: add a new analyzer without touching existing code - just register
it in AnalysisFactory. LSP: every analyzer is substitutable for DataAnalyzer.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class DataAnalyzer(ABC):
    """Abstraction high-level code depends on (DIP)."""

    @abstractmethod
    def analyze_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return an aggregated pivot table."""


class MonthlySalesAnalyzer(DataAnalyzer):
    """Monthly sales per branch -> rows=Branch, cols=Month."""

    def analyze_data(self, data: pd.DataFrame) -> pd.DataFrame:
        monthly = data.groupby(["Branch", "Month"])["Sales"].sum().unstack(fill_value=0)
        # Keep calendar order Jan -> Feb when present
        order = [m for m in ("January", "February") if m in monthly.columns]
        other = [c for c in monthly.columns if c not in order]
        return monthly[order + other]


class WeeklySalesAnalyzer(DataAnalyzer):
    """Weekly sales per branch -> rows=Branch, cols=Week."""

    def analyze_data(self, data: pd.DataFrame) -> pd.DataFrame:
        weekly = data.groupby(["Branch", "Week"])["Sales"].sum().unstack(fill_value=0)
        ordered = sorted(weekly.columns, key=str)
        return weekly[ordered]


class AnalysisFactory:
    """Factory - centralises object creation (SRP)."""

    _registry: dict[str, type[DataAnalyzer]] = {
        "monthly": MonthlySalesAnalyzer,
        "weekly": WeeklySalesAnalyzer,
    }

    @staticmethod
    def get_analyzer(analyzer_type: str) -> DataAnalyzer:
        try:
            return AnalysisFactory._registry[analyzer_type.lower()]()
        except KeyError as exc:
            raise ValueError(
                f"Unknown analyzer type '{analyzer_type}'. "
                f"Choose from {sorted(AnalysisFactory._registry)}."
            ) from exc

    @staticmethod
    def available() -> list[str]:
        return sorted(AnalysisFactory._registry)
