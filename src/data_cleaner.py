"""Data cleaning / preprocessing (SRP)."""
from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "Date", "Branch", "Month", "Week",
    "Category", "Product", "Quantity", "Price", "Sales",
]


class DataCleaner:
    """Clean raw sales data: dedupe, fix formats, handle missing values."""

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        cleaned = data.copy()

        # 1. Drop exact duplicate transactions
        cleaned = cleaned.drop_duplicates()

        # 2. Standardise text columns
        for col in ("Branch", "Month", "Category", "Product", "Week"):
            if col in cleaned.columns:
                cleaned[col] = cleaned[col].astype(str).str.strip()

        # 3. Standardise dates to YYYY-MM-DD where possible
        if "Date" in cleaned.columns:
            cleaned["Date"] = pd.to_datetime(cleaned["Date"], errors="coerce")

        # 4. Numeric coercion + drop rows with no sales info
        for col in ("Quantity", "Price", "Sales"):
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
        cleaned = cleaned.dropna(subset=["Sales"])
        cleaned = cleaned[cleaned["Sales"] > 0]

        # 5. Recompute Sales where Quantity & Price exist (consistency check)
        mask = cleaned["Quantity"].notna() & cleaned["Price"].notna()
        cleaned.loc[mask, "Sales"] = cleaned.loc[mask, "Quantity"] * cleaned.loc[mask, "Price"]

        # 6. Range checks - no negative quantities/prices
        cleaned = cleaned[(cleaned["Quantity"] >= 0) & (cleaned["Price"] >= 0)]

        return cleaned.reset_index(drop=True)

    def validate(self, data: pd.DataFrame) -> list[str]:
        """Return a list of data-quality issues (empty = OK)."""
        issues: list[str] = []
        for col in REQUIRED_COLUMNS:
            if col not in data.columns:
                issues.append(f"Missing column: {col}")
        if data.empty:
            issues.append("Dataset is empty.")
        if "Sales" in data.columns and (data["Sales"] < 0).any():
            issues.append("Negative sales amounts found.")
        if "Quantity" in data.columns and (data["Quantity"] < 0).any():
            issues.append("Negative quantities found.")
        return issues
