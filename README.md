# sampath-food-city-analytics

Classic CLI rebuild: SOLID + Factory/Template/Strategy/Facade + pytest + tox.
Features: monthly sales, weekly sales, price analysis, preferences, distribution.
Run: pip install -r requirements.txt ; python main.py --all
Tests: pytest -v  (17 tests) ; tox
Layout: main.py, src/, data/sales_data.csv, tests/, reports/

# sampath-food-city-analytics

Classic CLI rebuild: SOLID + Factory/Template/Strategy/Facade + pytest + tox.

## Features

- Monthly sales per branch analysis
- Weekly sales per branch analysis
- Price analysis per category
- Product preference analysis (revenue share & count)
- Sales distribution statistics & KDE plots
- Interactive Streamlit dashboard

## Run

```powershell
pip install -r requirements.txt
python main.py --all
# or
streamlit run app.py
```

## Tests

```powershell
pytest -v    # runs 17 tests
tox          # runs tests across py311 & py312
```

## Layout

```
src/
  data_cleaner.py   # Data cleaning / preprocessing (SRP)
  data_loader.py    # Data loading (SRP)
  facade_analysis.py  # Facade pattern for total-sales-distribution
  factory_analysis.py   # Factory pattern for branch-based analyses
  strategy_analysis.py  # Strategy pattern for preference analysis
  template_analysis.py  # Template pattern for product price analysis
  visualizer.py   # Matplotlib chart helpers

data/
  sales_data.csv  # Synthetic sales data (30 rows, branches: Colombo/Kandy/Galle)

tests/
  test_sales_system.py  # 17 pytest tests

reports/          # Generated analysis charts (.png)

.gitignore        # Excludes pycache, venv, caches, temp files

README.md         # This file

requirements.txt  # Dependencies: pandas, matplotlib, seaborn, pytest, tox, streamlit

tox.ini           # Tox configuration for multi-python testing
```

## Patterns Used

- **SOLID principles** throughout
- **Factory pattern** - AnalysisFactory creates Monthly/Weekly analyzers (OCP: add new analyzers without modifying existing code)
- **Strategy pattern** - PreferenceAnalyzer delegates to swappable strategies (ProductPreferenceStrategy vs ProductCountStrategy)
- **Template pattern** - DataAnalysisTemplate defines fixed workflow (load → preprocess → filter → analyze → plot), subclasses vary steps
- **Facade pattern** - SalesFacade hides the load→filter→stats→plot subsystem behind a single interface

## Data

`sales_data.csv` contains synthetic sales data with 30 rows across 3 branches (Colombo, Kandy, Galle), 2 months (January, February), 4 categories (Beverages, Bakery, Dairy, Electronics), and various products. No real customer or business data is included.

## License

Copyright © 2026 Lakshima Madurangi. All rights reserved.

This repository is publicly available for viewing and portfolio evaluation purposes only. No permission is granted to copy, modify, redistribute, or use the source code, in whole or in part, without prior written permission from the copyright holder, except where applicable law permits otherwise.

Third-party components and dependencies remain subject to their respective licences.
