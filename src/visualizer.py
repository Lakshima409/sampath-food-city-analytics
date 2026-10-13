"""Matplotlib chart helpers (SRP - only plotting lives here).

Matplotlib/seaborn are optional: if unavailable, charts are skipped with a
message instead of crashing the analysis (useful on lab machines).
"""
from __future__ import annotations

import pandas as pd

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _MPL = True
except ImportError:
    plt = None  # type: ignore
    _MPL = False


class Visualizer:
    """Single place for all chart styling."""

    def _guard(self) -> bool:
        if not _MPL:
            print("  (chart skipped - install matplotlib to enable charts)")
            return False
        return True

    def _finalize(self, save_path: str | None, show: bool) -> None:
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150)
        if show:
            try:
                plt.show()
            except Exception:
                pass
        plt.close()

    def bar_chart(self, data, title, xlabel="Branch",
                  ylabel="Total Sales (Rs.)", save_path=None, show=False) -> None:
        if not self._guard():
            return
        data.plot(kind="bar", figsize=(10, 6))
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=0)
        plt.legend(title="Period", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        self._finalize(save_path, show)

    def line_chart(self, series, title, xlabel="Month",
                   ylabel="Average Price (Rs.)", save_path=None, show=False) -> None:
        if not self._guard():
            return
        plt.figure(figsize=(10, 6))
        plt.plot(series.index.astype(str), series.values, marker="o")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, linestyle="--", alpha=0.4)
        self._finalize(save_path, show)

    def pie_chart(self, series, title, save_path=None, show=False) -> None:
        if not self._guard():
            return
        plt.figure(figsize=(8, 8))
        plt.pie(series.values, labels=series.index.astype(str), autopct="%1.1f%%")
        plt.title(title)
        plt.ylabel("")
        self._finalize(save_path, show)

    def distribution_chart(self, values, title="Distribution of Total Sales Amount",
                           save_path=None, show=False) -> None:
        if not self._guard():
            return
        plt.figure(figsize=(10, 6))
        plt.hist(values, bins=30, edgecolor="k", alpha=0.7)
        plt.title(title)
        plt.xlabel("Sales Amount (Rs.)")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle="--", alpha=0.4)
        self._finalize(save_path, show)

    def kde_by_month(self, data, save_path=None, show=False) -> None:
        if not self._guard():
            return
        try:
            import seaborn as sns
            plt.figure(figsize=(10, 6))
            for month in ("January", "February"):
                subset = data[data["Month"] == month]["Sales"]
                if not subset.empty:
                    sns.kdeplot(subset, label=month, fill=True, alpha=0.3)
            plt.title("Distribution of Total Sales Amount (Jan vs Feb)")
            plt.xlabel("Sales Amount (Rs.)")
            plt.ylabel("Density")
            plt.legend()
            plt.grid(True, linestyle="--", alpha=0.4)
            self._finalize(save_path, show)
        except ImportError:
            self.distribution_chart(data["Sales"], save_path=save_path, show=show)

