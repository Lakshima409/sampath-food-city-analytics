# tox result (2026-10-13, real run)
Command: python -m tox
- py312: OK - 17 passed in 7.31s in fresh isolated env
  (deps reinstalled: pytest, pandas, matplotlib, seaborn)
- py311: SKIP - interpreter not installed on this machine
  (skip_missing_interpreters = true in tox.ini)
- Exit code 0, congratulations :)
Paste-ready for report Testing section:
py312: 17 passed | py311: skipped (no interpreter)
Full log: see terminal output starting
"py312: install_deps> python -I -m pip install ..."
