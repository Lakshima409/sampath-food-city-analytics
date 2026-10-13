"""Strategy pattern for product-preference analysis.

The context (PreferenceAnalyzer) delegates the algorithm to a swappable
strategy, so new preference metrics can be added without modifying it (OCP).
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class AnalysisStrategy(ABC):
    """Strategy interface (ISP - tiny, focused)."""

    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> pd.Series:
        """Return preference shares indexed by category/product."""


class ProductPreferenceStrategy(AnalysisStrategy):
    """Share of total revenue per product category (percentage)."""

    def analyze(self, data: pd.DataFrame) -> pd.Series:
        totals = data.groupby("Category")["Sales"].sum()
        return (totals / totals.sum() * 100).round(2).sort_values(ascending=False)


class ProductCountStrategy(AnalysisStrategy):
    """Share of transactions per product category (percentage)."""

    def analyze(self, data: pd.DataFrame) -> pd.Series:
        counts = data["Category"].value_counts(normalize=True) * 100
        return counts.round(2)


class PreferenceAnalyzer:
    """Context - depends on the abstraction, not concretions (DIP)."""

    def __init__(self, strategy: AnalysisStrategy) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: AnalysisStrategy) -> None:
        self.strategy = strategy

    def execute_analysis(self, data: pd.DataFrame) -> pd.Series:
        return self.strategy.analyze(data)
