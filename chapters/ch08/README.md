# Chapter 8

Three new skills, each with a `scripts/` folder, chain into Dana's weekly pipeline, and `profile-data`
gets a folder of its own:

- `.claude/skills/to-parquet/` runs `scripts/to_parquet.py <folder>` (for example `data/raw`) and
  writes one Parquet file per CSV into `data/parquet/`.
- `.claude/skills/build-marts/` runs `scripts/build_marts.py`, which copies `stores` and `products`
  and runs the SQL files in `models/` in order (`sales_raw`, `sales_clean`, `returns_clean`,
  `weekly_sales`, `store_weekly`, `product_weekly`) into `warehouse.duckdb`, then prints the row
  counts, the period totals and three checks. `references/kpi-rules.md` holds the KPI rules in
  sentences; Claude reads it when this skill runs and no other skill loads it.
- `.claude/skills/kpi-report/` runs `scripts/kpi_report.py [Monday]` and writes
  `reports/kpi-<week>.md` plus two PNG charts. It needs matplotlib (`uv add matplotlib`; this
  folder's `pyproject.toml` and `uv.lock` already list it).
- `.claude/skills/profile-data/` now holds `scripts/profile.py` (chapter 2's file, moved) and
  `scripts/dq_profile.py` (chapter 4's file, moved, now saving its report to `out/dq_profile.txt`).
  Run `git mv profile.py` and `git mv dq_profile.py` from your project root, as the chapter shows.
- `.claude/commands/weekly-report.md` is rewritten as the one entry point: it names the three skills
  in order. `.claude/CLAUDE.md` and `.claude/settings.json` change in the one line and the two allow
  rules that named `dq_profile.py` at the project root.
- `models/weekly_sales.sql` grows from four columns to nine and now reads `sales_clean` and
  `returns_clean`; the other five models are new.

Every `SKILL.md` lists each script call in both shapes (`Bash(...)` and `PowerShell(...)`), keeps
colon-and-space out of its description, and tells Claude to run one command from the project root.
The scripts open `data/raw/` relative to the project root, so run them from there.

The pipeline writes `data/parquet/`, `warehouse.duckdb` and `out/dq_profile.txt`, which are
generated and not part of this folder. It also writes `reports/`; add `reports/` to your
`.gitignore` as the chapter does. `warehouse.duckdb` holds eight tables (no `customers`: no KPI
uses it, and it holds names and emails). With `python make_data.py` (the full drop) the report
week is 2026-09-21; with `python make_data.py --through 2026-09-20` the latest week is
2026-09-14.
