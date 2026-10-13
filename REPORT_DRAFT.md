# Sampath Food City - Sales Analysis System
## Unit 20 Report Draft (Part 1) - from real code + live results

## 1. Introduction
Manual spreadsheet analysis at Sampath Food City (Colombo/Kandy/Galle) was slow,
error-prone, and untestable. The new Python system reads one CSV
(`data/sales_data.csv`, 48 transactions, Jan-Feb 2024) and produces 5 analyses
+ charts via `python main.py --all`:
monthly/weekly per branch (bar), avg price per month (line),
preference shares (pie), sales distribution + Jan-vs-Feb KDE (hist+KDE).
Plus 17 pytest tests, tox multi-env proof, and Streamlit dashboard (`app.py`).

Run:
pip install -r requirements.txt
python main.py --all
python -m pytest -v
python -m tox
streamlit run app.py

## 2. SOLID evaluation
- SRP: DataLoader (read only), DataCleaner (clean only), Visualizer (plot only).
- OCP: new Factory analyzer or Strategy = add class + 1 registry line, no edits.
- LSP: Monthly/Weekly analyzers interchangeable via DataAnalyzer interface.
- ISP: AnalysisStrategy has one method analyze(data); Template hooks are tiny.
- DIP: main.py, tests, app.py depend on abstractions (DataAnalyzer,
  AnalysisStrategy, DataAnalysisTemplate, SalesFacade).

## 3. Patterns justification
- Factory (monthly/weekly, src/factory_analysis.py): same Branch x Period pivot,
  differing period. get_analyzer("monthly") hides class names. Unknown key raises
  ValueError (tested). Adding quarterly = 1 class, 0 CLI changes.
- Template (price, src/template_analysis.py): fixed execute() =
  load->preprocess (AveragePrice=Sales/Quantity)->filter (1 Category)->
  analyze (mean per Month)->plot (line). Electronics: Jan 3,950 / Feb 9,483.33.
- Strategy (preferences, src/strategy_analysis.py): revenue-share vs count-share
  swapped at runtime; Mock injectable (test_strategy_is_swappable). Revenue top:
  Electronics 43.98%.
- Facade (distribution, src/facade_analysis.py): analyze_sales() hides
  loader+cleaner+filter+stats+plotter, returns count/total/mean/median/min/max.

## 4. Preprocessing + validation
DataCleaner.clean(): drop dupes, strip text, coerce dates/numerics,
drop null/non-positive Sales, recompute Sales=Quantity*Price, drop negatives.
validate() flags missing columns/negatives; DataLoader raises FileNotFoundError.
