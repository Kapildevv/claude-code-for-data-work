"""Build warehouse.duckdb from the Parquet files in data/parquet/.

Run it from the project root:

    uv run python .claude/skills/build-marts/scripts/build_marts.py

It copies the two lookup tables, then runs the SQL files in models/ in order, each into a table
named after its file. It prints the row counts, the period totals and three checks, and exits 1
if a check fails.
"""

import sys
from pathlib import Path

import duckdb

PARQUET = Path("data/parquet")
MODELS = Path("models")
LOOKUPS = ["stores", "products"]
ORDER = ["sales_raw", "sales_clean", "returns_clean", "weekly_sales", "store_weekly", "product_weekly"]

missing = [p.as_posix() for p in (PARQUET / f"{name}.parquet" for name in [*LOOKUPS, "sales", "returns"]) if not p.exists()]
if missing:
    sys.exit(f"missing {', '.join(missing)}: run the to-parquet skill first")

con = duckdb.connect("warehouse.duckdb")
for name in LOOKUPS:
    con.sql(f"create or replace table {name} as select * from read_parquet('{(PARQUET / f'{name}.parquet').as_posix()}')")
con.sql("alter table products alter list_price type decimal(10,2)")
con.sql("alter table products alter unit_cost type decimal(10,2)")
for name in ORDER:
    con.sql(f"create or replace table {name} as {(MODELS / f'{name}.sql').read_text(encoding='utf-8')}")


def one(sql: str):
    return con.sql(sql).fetchone()[0]


def money(value) -> str:
    return f"${value:,.2f}"


distinct = one("select count(*) from (select distinct * from sales_raw)")
counts = {name: one(f"select count(*) from {name}") for name in [*LOOKUPS, *ORDER]}
for name, rows in counts.items():
    note = ""
    if name == "sales_clean":
        note = f"  ({counts['sales_raw'] - distinct} repeated, {distinct - rows} below quantity 1)"
    print(f"{name:<16}{rows:>6,} rows{note}")

gross, returned, net = con.sql("select sum(gross_sales), sum(returns_value), sum(net_sales) from weekly_sales").fetchone()
print()
print("period")
print(f"  gross sales   {money(gross)}")
print(f"  returns value {money(returned)}")
print(f"  net sales     {money(net)}")
print(f"  returns rate  {returned / gross:.2%}")

returns_in = one("select count(*) from read_parquet('data/parquet/returns.parquet')")
store_net = one("select sum(net_sales) from store_weekly")
checks = [
    (f"returns_clean keeps every return ({counts['returns_clean']} of {returns_in})", counts["returns_clean"] == returns_in),
    ("gross sales minus returns value is net sales", gross - returned == net),
    ("store_weekly adds up to weekly_sales", store_net == net),
]
print()
print("checks")
for label, passed in checks:
    print(f"  {label:<50}{'ok' if passed else 'FAIL'}")
sys.exit(0 if all(passed for _, passed in checks) else 1)
