import os

import duckdb

RAW = "data/raw/sales.csv"
OUT = "out/clean_sales.csv"

raw = duckdb.read_csv(RAW)
deduped = duckdb.sql("select distinct * from raw")
clean = duckdb.sql("""
    select order_id, order_date, store_id, customer_id, product_id,
           quantity, unit_price::decimal(10, 2) as unit_price
    from deduped
    where quantity >= 1
    order by order_id
""")

os.makedirs("out", exist_ok=True)
clean.write_csv(OUT)

print(f"{RAW}: {raw.shape[0]:,} rows read")
print(f"removed {raw.shape[0] - deduped.shape[0]:,} exact duplicate rows")
print(f"removed {deduped.shape[0] - clean.shape[0]:,} rows with a quantity below 1")
print(f"{OUT}: {clean.shape[0]:,} rows written")
