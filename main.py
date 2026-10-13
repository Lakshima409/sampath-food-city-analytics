"""CLI entry point - menu + argparse commands."""
import argparse
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.factory_analysis import AnalysisFactory
from src.template_analysis import PriceAnalysis
from src.strategy_analysis import PreferenceAnalyzer
from src.strategy_analysis import ProductPreferenceStrategy, ProductCountStrategy
from src.facade_analysis import SalesFacade
from src.visualizer import Visualizer
DATA_FILE = os.path.join("data", "sales_data.csv")
REPORTS = "reports"

def ensure_reports():
    os.makedirs(REPORTS, exist_ok=True)

def load_clean():
    raw = DataLoader(DATA_FILE).load_data()
    cleaned = DataCleaner().clean(raw)
    print(f"Loaded {len(cleaned)} clean transactions.")
    return cleaned
def do_monthly(show=False):
    ensure_reports()
    data = load_clean()
    result = AnalysisFactory.get_analyzer("monthly").analyze_data(data)
    print("\n--- Monthly Sales per Branch (Rs.) ---")
    print(result.to_string())
    print(f"\nGrand total: Rs.{result.values.sum():,.2f}")
    out = os.path.join(REPORTS, "monthly_sales.png")
    Visualizer().bar_chart(result, "Monthly Sales Analysis", save_path=out, show=show)
    print(f"Chart saved -> {out}")
    return result

def do_weekly(show=False):
    ensure_reports()
    data = load_clean()
    result = AnalysisFactory.get_analyzer("weekly").analyze_data(data)
    print("\n--- Weekly Sales per Branch (Rs.) ---")
    print(result.to_string())
    out = os.path.join(REPORTS, "weekly_sales.png")
    Visualizer().bar_chart(result, "Weekly Sales Analysis", save_path=out, show=show)
    print(f"Chart saved -> {out}")
    return result

def do_price(category="Electronics", show=False):
    ensure_reports()
    out = os.path.join(REPORTS, "price_analysis.png")
    result = PriceAnalysis(category=category).execute(DATA_FILE, save_path=out)
    print(f"\n--- Average Price per Month ({category}) ---")
    print(result.to_string())
    print(f"Chart saved -> {out}")
    return result

def do_preferences(by="revenue", show=False):
    ensure_reports()
    data = load_clean()
    strat = ProductPreferenceStrategy() if by == "revenue" else ProductCountStrategy()
    result = PreferenceAnalyzer(strat).execute_analysis(data)
    print(f"\n--- Product Preferences by {by} (%) ---")
    print(result.to_string())
    print(f"\nMost preferred: {result.idxmax()} ({result.max():.1f}%)")
    out = os.path.join(REPORTS, "preferences.png")
    Visualizer().pie_chart(result, "Product Preference Analysis", save_path=out, show=show)
    print(f"Chart saved -> {out}")
    return result

def do_distribution(show=False):
    ensure_reports()
    out = os.path.join(REPORTS, "distribution.png")
    kde_out = os.path.join(REPORTS, "distribution_kde.png")
    stats = SalesFacade(DATA_FILE).analyze_sales(save_path=out)
    print("\n--- Total Sales Distribution ---")
    for k, v in stats.items():
        print(f"{k:>8}: {v:,.2f}")
    raw = DataLoader(DATA_FILE).load_data()
    Visualizer().kde_by_month(DataCleaner().clean(raw), save_path=kde_out, show=show)
    print(f"Charts saved -> {out}, {kde_out}")
    return stats

def menu():
    actions = {"1": ("Monthly sales (Factory)", do_monthly),
               "2": ("Weekly sales (Factory)", do_weekly),
               "3": ("Price analysis (Template)", do_price),
               "4": ("Preferences (Strategy)", do_preferences),
               "5": ("Distribution (Facade)", do_distribution),
               "0": ("Exit", None)}
    while True:
        print("\n===== Sampath Food City - Sales Analysis =====")
        for k, (label, _) in actions.items():
            print(f"  {k}. {label}")
        c = input("Select option: ").strip()
        if c == "0":
            print("Goodbye!")
            break
        e = actions.get(c)
        if not e:
            print("Invalid choice.")
            continue
        try:
            e[1]()
        except Exception as ex:
            print(f"Error: {ex}")
        input("\nPress Enter to continue...")

def main():
    p = argparse.ArgumentParser(description="Sampath Food City Sales Analysis")
    p.add_argument("--monthly", action="store_true")
    p.add_argument("--weekly", action="store_true")
    p.add_argument("--price", nargs="?", const="Electronics", default=None)
    p.add_argument("--preferences", nargs="?", const="revenue", default=None,
                   choices=["revenue", "count"])
    p.add_argument("--distribution", action="store_true")
    p.add_argument("--show", action="store_true")
    p.add_argument("--all", action="store_true")
    a = p.parse_args()
    ran = False
    if a.monthly or a.all:
        do_monthly(show=a.show); ran = True
    if a.weekly or a.all:
        do_weekly(show=a.show); ran = True
    if a.price is not None or a.all:
        do_price(a.price or "Electronics", show=a.show); ran = True
    if a.preferences is not None or a.all:
        do_preferences(a.preferences or "revenue", show=a.show); ran = True
    if a.distribution or a.all:
        do_distribution(show=a.show); ran = True
    if not ran:
        menu()

if __name__ == "__main__":
    main()


