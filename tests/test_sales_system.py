"""Tests for loading, cleaning, Factory, Template, Strategy, Facade."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")


# --- 1. Data loading ---
def test_data_loading_reads_all_rows():
    from src.data_loader import DataLoader

    data = DataLoader(DATA_FILE).load_data()
    assert len(data) == 48
    assert set(["Branch", "Month", "Sales"]).issubset(data.columns)


def test_data_loading_missing_file_raises():
    from src.data_loader import DataLoader

    with pytest.raises(FileNotFoundError):
        DataLoader("no_such_file.csv").load_data()


# --- 2. Cleaning ---
def test_cleaner_removes_duplicates_and_negatives(clean_data):
    assert (clean_data["Sales"] > 0).all()
    assert clean_data.duplicated().sum() == 0


def test_cleaner_recomputes_sales_consistently(clean_data):
    import pandas as pd

    expected = (clean_data["Quantity"] * clean_data["Price"]).round(2)
    assert ((clean_data["Sales"] - expected).abs() < 0.01).all()


def test_validator_flags_missing_column(clean_data):
    from src.data_cleaner import DataCleaner

    bad = clean_data.drop(columns=["Sales"])
    assert any("Sales" in i for i in DataCleaner().validate(bad))


# --- 3. Factory: monthly ---
def test_monthly_totals_match_csv(clean_data):
    from src.factory_analysis import AnalysisFactory

    result = AnalysisFactory.get_analyzer("monthly").analyze_data(clean_data)
    assert result.loc["Colombo", "January"] == 544000
    assert result.loc["Galle", "February"] == 721600
    assert result.values.sum() == pytest.approx(3688210.0)


def test_factory_rejects_unknown_type():
    from src.factory_analysis import AnalysisFactory

    with pytest.raises(ValueError):
        AnalysisFactory.get_analyzer("yearly")


# --- 4. Factory: weekly ---
def test_weekly_totals_match_csv(clean_data):
    from src.factory_analysis import AnalysisFactory

    result = AnalysisFactory.get_analyzer("weekly").analyze_data(clean_data)
    assert result.loc["Colombo", "W1"] == 506600
    assert result.values.sum() == pytest.approx(3688210.0)


# --- 5. Template: price ---
def test_price_analysis_electronics():
    from src.template_analysis import PriceAnalysis

    result = PriceAnalysis("Electronics").execute(DATA_FILE)
    assert result["January"] == pytest.approx(3950.0)
    assert result["February"] == pytest.approx(9483.33, abs=0.1)


def test_price_analysis_unknown_category_raises():
    from src.template_analysis import PriceAnalysis

    with pytest.raises(ValueError):
        PriceAnalysis("NoSuchCategory").execute(DATA_FILE)


# --- 6. Strategy: preferences ---
def test_preferences_revenue_shares_sum_to_100(clean_data):
    from src.strategy_analysis import PreferenceAnalyzer, ProductPreferenceStrategy

    result = PreferenceAnalyzer(ProductPreferenceStrategy()).execute_analysis(clean_data)
    assert result.sum() == pytest.approx(100.0, abs=0.05)
    assert result.idxmax() == "Electronics"


def test_preferences_count_strategy(clean_data):
    from src.strategy_analysis import PreferenceAnalyzer, ProductCountStrategy

    result = PreferenceAnalyzer(ProductCountStrategy()).execute_analysis(clean_data)
    assert result.sum() == pytest.approx(100.0, abs=0.05)


def test_strategy_is_swappable(clean_data):
    from unittest.mock import Mock

    from src.strategy_analysis import PreferenceAnalyzer

    mock = Mock()
    mock.analyze.return_value = "ok"
    assert PreferenceAnalyzer(mock).execute_analysis(clean_data) == "ok"
    mock.analyze.assert_called_once()


# --- 7. Facade: distribution ---
def test_distribution_stats():
    from src.facade_analysis import SalesFacade

    stats = SalesFacade(DATA_FILE).analyze_sales()
    assert stats["count"] == 48
    assert stats["total"] == pytest.approx(3688210.0)
    assert stats["mean"] == pytest.approx(76837.71, abs=0.1)
    assert stats["median"] == pytest.approx(50875.0)
    assert stats["min"] == pytest.approx(33000.0)


def test_facade_empty_filter_raises():
    from src.facade_analysis import SalesFacade

    with pytest.raises(ValueError):
        SalesFacade(DATA_FILE).analyze_sales(months=["NoMonth"])


# --- 8. Data integrity ---
def test_data_integrity_branches_months(clean_data):
    assert set(clean_data["Branch"].unique()) == {"Colombo", "Kandy", "Galle"}
    assert set(clean_data["Month"].unique()) == {"January", "February"}


def test_grand_total_integrity(clean_data):
    assert clean_data["Sales"].sum() == pytest.approx(3688210.0)
