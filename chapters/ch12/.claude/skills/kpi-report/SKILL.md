---
name: kpi-report
description: Use when Dana's weekly KPI report is due, after build-marts. Writes reports/kpi-<week>.md and two PNG charts for one week, the latest week unless the request names a Monday.
argument-hint: <Monday of the report week, such as 2026-09-21, or nothing for the latest week>
allowed-tools:
  - Bash(uv run python ${CLAUDE_SKILL_DIR}/scripts/kpi_report.py *)
  - Bash(uv run python ${CLAUDE_SKILL_DIR}/scripts/kpi_report.py)
  - PowerShell(uv run python ${CLAUDE_SKILL_DIR}/scripts/kpi_report.py *)
  - PowerShell(uv run python ${CLAUDE_SKILL_DIR}/scripts/kpi_report.py)
---

# Write the weekly KPI report

Run one command from the project root. Never join it to another with `cd` or `&&`, and never write report or chart code yourself.

1. Take the week from the request: $ARGUMENTS. If it is empty, run the script without a week and it uses the latest one.
2. Run `uv run python ${CLAUDE_SKILL_DIR}/scripts/kpi_report.py <week>`.
3. Copy the script's output into the reply unchanged: the three paths and the headline line. Quote every number exactly as printed, and do not round or recompute any of them.
4. If the script fails, copy its message and stop.
