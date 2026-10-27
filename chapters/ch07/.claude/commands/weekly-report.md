---
description: Dana's weekly numbers from models/weekly_sales.sql
---

Run the query in `models/weekly_sales.sql` against `data/raw/` with DuckDB, for example with
`uv run python -c "import duckdb; print(duckdb.sql(open('models/weekly_sales.sql').read()).fetchall()[-1])"`.

The last row is the latest week. Write Dana two sentences: the week that starts on that date,
then its gross sales, returns value and net sales. Quote the numbers exactly as the query
printed them, and do not round or recompute any of them.
