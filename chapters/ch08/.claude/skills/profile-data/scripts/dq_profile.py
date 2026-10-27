"""Count each nightly file's rows, then the rows that break Luis's five promises.

Run from the project root. It reads data/raw/, prints the counts and saves the same text to
out/dq_profile.txt. It never writes to data/raw/ and always exits 0.
"""

from pathlib import Path

import duckdb

TABLES = ["customers", "products", "stores", "dates", "sales", "returns"]

con = duckdb.connect()
for table in TABLES:
    con.sql(f"create view {table} as select * from read_csv('data/raw/{table}.csv')")

PROMISES = [
    ("customers with no email",
     "select count(*) from customers where email is null"),
    ("sales rows sent twice",
     "select count(*) - count(distinct order_id) from sales"),
    ("sales rows with a quantity below 1",
     "select count(*) from sales where quantity < 1"),
    ("returns after the 30-day window",
     """select count(*) from returns r
        join (select distinct order_id, order_date from sales) s using (order_id)
        where r.return_date - s.order_date > 30"""),
    ("returns with no matching order",
     """select count(*) from returns r
        where not exists (select 1 from sales s where s.order_id = r.order_id)"""),
]

lines = []
for table in TABLES:
    rows = con.sql(f"select count(*) from {table}").fetchone()[0]
    lines.append(f"{table:<10}{rows:>7,} rows")

lines.append("")
for label, sql in PROMISES:
    broken = con.sql(sql).fetchone()[0]
    lines.append(f"{label:<38}{broken:>5}  {'kept' if broken == 0 else 'broken'}")

report = "\n".join(lines)
print(report)
Path("out").mkdir(exist_ok=True)
Path("out/dq_profile.txt").write_text(report + "\n", encoding="utf-8")
print("\nsaved to out/dq_profile.txt")
