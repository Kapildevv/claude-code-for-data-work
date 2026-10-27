---
description: Dana's weekly report, from the nightly CSV files to reports/
argument-hint: <Monday of the report week, or nothing for the latest week>
---

Run these three skills one after the other, each with the Skill tool, and stop at the first one that reports an error. Write no code of your own.

1. Skill `to-parquet`, with the argument `data/raw`.
2. Skill `build-marts`.
3. Skill `kpi-report`, with the argument $ARGUMENTS (no argument means the latest week).

When all three have finished, write Dana two sentences: the report week's net sales and returns rate, and the path of the report. Quote the numbers exactly as `kpi-report` printed them.
