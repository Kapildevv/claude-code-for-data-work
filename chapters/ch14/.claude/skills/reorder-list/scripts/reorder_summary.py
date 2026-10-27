"""Print the size of the weekly reorder list and the counts that need a recount.

Run `uv run dbt build` first: this reads the tables that build leaves in inventory.duckdb.
"""

import sys
from pathlib import Path

import duckdb

DB = Path("inventory.duckdb")
if not DB.exists():
    sys.exit("inventory.duckdb not found. Run `uv run dbt build` from the project root first.")

con = duckdb.connect(str(DB), read_only=True)
rows, units, negative = con.sql(
    "select count(*), sum(order_quantity), count(*) filter (where on_hand < 0) from mart_reorder_list"
).fetchone()
recount = con.sql(
    "select store_id, product_id, product_name, on_hand from fct_stock_on_hand where on_hand < 0 order by 1, 2"
).fetchall()

print(f"reorder list: {rows:,} rows, {units:,} units to order")
print(f"rows ordered against a negative count: {negative}")
print(f"latest counts below zero, for a recount: {len(recount)}")
for store_id, product_id, product_name, on_hand in recount:
    print(f"  {store_id} {product_id} {product_name} ({on_hand})")
