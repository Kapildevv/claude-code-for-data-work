# Juniper Lane Goods: weekly KPI report

Juniper Lane Goods is a fictional outdoor-gear retailer with twelve stores. Every night the
store system drops six CSV files into `data/raw/`. This project turns them into Dana's weekly
KPI report: net sales, returns rate, top stores and top products. A new analyst should be able
to follow this file without asking anyone.

## Conventions

- Use snake_case for file names, Python functions and variables, tables and columns.
- DuckDB is the only database. Run Python with `uv run python <script>`. Add no other
  database, and no package, without asking first.
- Never write to `data/raw/`. Luis owns it and the store system replaces its files every
  night. Read from it, and write results to `out/`.

## Commands

- `uv run python make_data.py` rebuilds the synthetic nightly drop in `data/raw/`.
- `uv run python clean_sales.py` writes `out/clean_sales.csv`, without repeated orders or
  quantities below 1.
- `uv run python dq_profile.py` counts the rows that break Luis's five promises.

## Money and weeks

- DuckDB reads prices as DOUBLE. Cast them to `DECIMAL(10,2)` before multiplying or summing.
- A report week runs Monday to Sunday.

## The data and Dana's KPI definitions

The next line imports `DATASET.md`: the six files, the five promises and the KPI definitions.

@../DATASET.md

<!-- For maintainers: an import path is relative to this file, so it starts with ../ to reach the project root. -->
