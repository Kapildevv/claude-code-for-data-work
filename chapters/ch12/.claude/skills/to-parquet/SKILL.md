---
name: to-parquet
description: Use when the nightly CSV files in data/raw/ must become Parquet, the first step of the weekly pipeline. Writes one Parquet file per CSV into data/parquet/ and reports the rows in each.
argument-hint: <folder with the CSV files, usually data/raw>
allowed-tools:
  - Bash(uv run python ${CLAUDE_SKILL_DIR}/scripts/to_parquet.py *)
  - PowerShell(uv run python ${CLAUDE_SKILL_DIR}/scripts/to_parquet.py *)
---

# Convert the nightly CSV files to Parquet

Run one command from the project root. Never join it to another with `cd` or `&&`, and never write conversion code yourself.

1. Take the folder from the request: $ARGUMENTS. If it is empty, use `data/raw`.
2. Run `uv run python ${CLAUDE_SKILL_DIR}/scripts/to_parquet.py <folder>`.
3. Copy the script's output into the reply unchanged. If the script fails, copy its message and stop.
4. Never write to `data/raw/`. The script only reads it.
