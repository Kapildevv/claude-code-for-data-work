#!/usr/bin/env bash
# Dana's weekly report with nobody at the keyboard. Exit 0 means a fresh report exists and nothing was refused.
set -euo pipefail
export MSYS_NO_PATHCONV=1                      # Git Bash on Windows would rewrite "/weekly-report" as a path
cd "$(dirname "$0")/.."                        # the project root, wherever the scheduler started this script
mkdir -p out
touch out/.weekly_started

claude -p "/weekly-report" \
    --model haiku \
    --max-turns 15 \
    --output-format json \
    --permission-mode dontAsk \
    --allowedTools "Skill" \
    --strict-mcp-config > out/weekly_report.json

grep -q '"is_error":false' out/weekly_report.json
grep -q '"permission_denials":\[\]' out/weekly_report.json
report=$(ls reports/kpi-*.md | sort | tail -n 1)
[ "$report" -nt out/.weekly_started ]
echo "$(basename "$report"): $(grep -m 1 '^| Net sales' "$report")"
