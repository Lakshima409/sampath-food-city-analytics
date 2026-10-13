"""Sampath Food City - Interactive Sales Dashboard (Streamlit).

Reuses the same SOLID + patterns codebase as the CLI (main.py):
- Factory (monthly/weekly), Template (price), Strategy (preferences), Facade (distribution)
- No logic duplicated: all calculations go through src/ classes.
Run:  streamlit run app.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import streamlit as st

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.factory_analysis import AnalysisFactory
from src.strategy_analysis import (
    PreferenceAnalyzer,
    ProductPreferenceStrategy,
    ProductCountStrategy,
)

DATA_FILE = os.path.join("data", "sales_data.csv")

st.set_page_config(page_title="Sampath Food City - Sales Dashboard", layout="wide")


@st.cache_data
def load_clean() -> pd.DataFrame:
    raw = DataLoader(DATA_FILE).load_data()
    return DataCleaner().clean(raw)


df = load_clean()

st.title("Sampath Food City - Sales Analysis Dashboard")
st.caption("Same Factory / Template / Strategy / Facade engine as the CLI (`python main.py --all`).")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
branches = sorted(df["Branch"].unique())
months = [m for m in ("January", "February") if m in df["Month"].unique()]
categories = sorted(df["Category"].unique())

sel_branches = st.sidebar.multiselect("Branch", branches, default=branches)
sel_months = st.sidebar.multiselect("Month", months, default=months)
sel_categories = st.sidebar.multiselect("Category", categories, default=categories)
pref_mode = st.sidebar.radio("Preference metric", ["revenue", "count"], index=0)
price_category = st.sidebar.selectbox("Price-analysis category", categories,
                                      index=categories.index("Electronics") if "Electronics" in categories else 0)

filtered = df[
    df["Branch"].isin(sel_branches)
    & df["Month"].isin(sel_months)
    & df["Category"].isin(sel_categories)
]

if filtered.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

# ---------- KPI cards ----------
total = float(filtered["Sales"].sum())
mean = float(filtered["Sales"].mean())
count = int(len(filtered))
top_cat = filtered.groupby("Category")["Sales"].sum().idxmax()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales (Rs.)", f"{total:,.0f}")
c2.metric("Mean Transaction (Rs.)", f"{mean:,.2f}")
c3.metric("Transactions", f"{count}")
c4.metric("Top Category (revenue)", str(top_cat))

# ---------- Tabs ----------
tab_monthly, tab_weekly, tab_price, tab_pref, tab_dist = st.tabs(
    ["Monthly (Factory)", "Weekly (Factory)", "Price (Template)", "Preferences (Strategy)", "Distribution (Facade)"]
)

with tab_monthly:
    st.subheader("Monthly Sales per Branch (Factory)")
    monthly = AnalysisFactory.get_analyzer("monthly").analyze_data(filtered)
    st.dataframe(monthly.style.format("{:,.0f}"))
    st.bar_chart(monthly)
    st.caption("Factory: `AnalysisFactory.get_analyzer('monthly')` -> rows=Branch, cols=Month.")

with tab_weekly:
    st.subheader("Weekly Sales per Branch (Factory)")
    weekly = AnalysisFactory.get_analyzer("weekly").analyze_data(filtered)
    st.dataframe(weekly.style.format("{:,.0f}"))
    st.bar_chart(weekly)
    st.caption("Factory: `AnalysisFactory.get_analyzer('weekly')` -> rows=Branch, cols=Week.")

with tab_price:
    st.subheader(f"Average Unit Price per Month - {price_category} (Template)")
    sub = filtered[filtered["Category"] == price_category].copy()
    if sub.empty:
        st.info(f"No rows for category '{price_category}' under current filters.")
    else:
        sub["AveragePrice"] = sub.apply(
            lambda r: r["Sales"] / r["Quantity"] if r["Quantity"] else r["Price"], axis=1
        )
        price_series = sub.groupby("Month")["AveragePrice"].mean()
        order = [m for m in ("January", "February") if m in price_series.index]
        price_series = price_series.reindex(order or price_series.index)
        st.dataframe(price_series.to_frame("Avg Price (Rs.)").style.format("{:,.2f}"))
        st.line_chart(price_series)
        st.caption("Template: `PriceAnalysis` skeleton load -> preprocess -> filter -> analyze -> plot.")

with tab_pref:
    st.subheader(f"Product Preferences by {pref_mode} (Strategy)")
    strat = ProductPreferenceStrategy() if pref_mode == "revenue" else ProductCountStrategy()
    prefs = PreferenceAnalyzer(strat).execute_analysis(filtered)
    st.dataframe(prefs.to_frame("Share (%)").style.format("{:.2f}"))
    st.bar_chart(prefs)
    st.caption(f"Strategy: context `PreferenceAnalyzer` + `{type(strat).__name__}`. Most preferred: {prefs.idxmax()} ({prefs.max():.1f}%).")

with tab_dist:
    st.subheader("Total Sales Distribution (Facade)")
    st.write(
        pd.DataFrame([{
            "count": int(filtered["Sales"].count()),
            "total": float(filtered["Sales"].sum()),
            "mean": float(filtered["Sales"].mean()),
            "median": float(filtered["Sales"].median()),
            "min": float(filtered["Sales"].min()),
            "max": float(filtered["Sales"].max()),
        }]).style.format("{:,.2f}")
    )
    st.bar_chart(filtered["Sales"].value_counts(bins=20).sort_index())
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        fig, ax = plt.subplots()
        for m in ("January", "February"):
            s = filtered[filtered["Month"] == m]["Sales"]
            if not s.empty:
                sns.kdeplot(s, label=m, fill=True, alpha=0.3, ax=ax)
        ax.set_title("Distribution KDE (Jan vs Feb)")
        ax.set_xlabel("Sales Amount (Rs.)")
        ax.legend()
        st.pyplot(fig)
    except Exception as ex:
        st.info(f"KDE skipped: {ex}")
    st.caption("Facade: `SalesFacade.analyze_sales()` hides load -> clean -> filter -> stats -> plot.")
