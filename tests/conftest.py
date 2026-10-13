"""Shared pytest fixtures."""
import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")


@pytest.fixture
def raw_data() -> pd.DataFrame:
    from src.data_loader import DataLoader

    return DataLoader(DATA_FILE).load_data()


@pytest.fixture
def clean_data(raw_data) -> pd.DataFrame:
    from src.data_cleaner import DataCleaner

    return DataCleaner().clean(raw_data)
