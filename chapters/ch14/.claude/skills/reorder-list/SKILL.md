---
name: reorder-list
description: Use when someone asks for the weekly reorder list, what to order this week, or a rebuild after a model change. Runs dbt build, then prints how many rows and units the reorder list holds and which store-product counts are negative and need a recount.
allowed-tools:
  - Bash(uv run dbt build)
  - PowerShell(uv run dbt build)
  - Bash(uv run python ${CLAUDE_SKILL_DIR}/scripts/reorder_summary.py)
  - PowerShell(uv run python ${CLAUDE_SKILL_DIR}/scripts/reorder_summary.py)
---

# Build the project and summarise the reorder list

Run each command on its own from the project root. Never join them with `cd` or `&&`, and never write SQL or Python of your own for this.

1. Run `uv run dbt build`. Copy its last line into the reply unchanged (the one that starts `Done.`). If the build reports ERROR above 0, copy the failing lines and stop.
2. Run `uv run python ${CLAUDE_SKILL_DIR}/scripts/reorder_summary.py`.
3. Copy the script's output into the reply unchanged. Quote every number exactly as printed, and do not round or recompute any of them.
4. If either command fails, copy its message and stop.
