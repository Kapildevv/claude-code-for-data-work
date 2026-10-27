---
paths:
  - "models/**/*.sql"
---

# SQL files in models/

- Write keywords in lowercase and give each clause its own line.
- Name every CTE for what it holds, such as `gross` or `returned`. Never `cte1` or `tmp`.
- Cast `unit_price` to `decimal(10,2)` before multiplying or summing, because DuckDB reads it as DOUBLE.
- Start every file with a comment line `-- model: <file name without .sql>`.
