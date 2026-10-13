
## 5. Implementation snippets
- Monthly: AnalysisFactory.get_analyzer("monthly").analyze_data(cleaned)
- Price: PriceAnalysis("Electronics").execute(DATA_FILE, save_path=out)
- Preferences: PreferenceAnalyzer(ProductPreferenceStrategy()).execute_analysis(cleaned)
- Distribution: SalesFacade(DATA_FILE).analyze_sales(save_path=out)
- Dashboard app.py reuses the same 4 classes behind filters + tabs.

## 6. Testing (real outputs 2026-10-13)
pytest: 17 passed in ~7s (Python 3.12.10, pytest 9.1.1).
Key pins: 48 rows; Colombo-Jan 544,000; Galle-Feb 721,600;
Colombo-W1 506,600; Electronics Jan 3,950 / Feb 9483.33;
prefs sum 100, top Electronics 43.98%; facade count 48, total 3688210,
mean 76837.71, median 50875, min 33000; grand total 3688210.
tox: py312 reinstalls pytest+pandas+matplotlib+seaborn fresh and reruns suite
(see TOX_RESULTS.md; py311 skipped - interpreter absent, skip_missing_interpreters).
Why pytest+tox: pytest = asserts+fixtures+mock; tox = clean-room proof.

## 7. Chart discussion
Monthly: all branches grew Jan->Feb (Colombo 544k->748k, Galle 520k->721k,
Kandy 509k->644k). Weekly: Colombo W1+W3, Galle W4-heavy, Kandy W2/W4.
Price Electronics +140% (mix to high-ticket Feb rows e.g. 261,000).
Preferences revenue: Electronics 43.98, Dairy 24.63, Beverages 18.31,
Bakery 13.08. Distribution right-skewed: mean 76,838 >> median 50,875.

## 8. Conclusion
CLI + 6 PNGs + 17 tests + tox proof + dashboard on one engine.
Each SOLID item + pattern traces to file + test + chart.
Next: quarterly Factory analyzer, profit-share Strategy, DB DataLoader.
Files: main.py, app.py, src/*.py, data/sales_data.csv, tests/, reports/,
tox.ini, requirements.txt, TOX_RESULTS.md.
