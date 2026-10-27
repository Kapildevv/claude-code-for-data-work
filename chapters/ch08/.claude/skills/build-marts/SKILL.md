---
name: build-marts
description: Use when the Parquet files in data/parquet/ must become the weekly KPI tables, after to-parquet. Builds warehouse.duckdb with clean sales, returns and the weekly marts under the rules in references/kpi-rules.md.
allowed-tools:
  - Bash(uv run python .claude/skills/build-marts/scripts/build_marts.py)
  - PowerShell(uv run python .claude/skills/build-marts/scripts/build_marts.py)
---

# Build the marts

1. Read `references/kpi-rules.md` in this skill's folder.
2. Run `uv run python .claude/skills/build-marts/scripts/build_marts.py` from the project root, as one command. Never join it to another with `cd` or `&&`, and never write SQL yourself.
3. If the script exits with an error or prints FAIL on a check line, copy that line, name the rule from step 1 that it breaks, and stop. Do not edit the script, the files in `models/` or the rules.
4. Otherwise copy the script's output into the reply unchanged, then add one sentence that names the rules, by number, behind the period's net sales and returns rate.
