import sys

import duckdb

path = sys.argv[1]
data = duckdb.read_csv(path)

print(f"{path}: {data.shape[0]:,} rows, {data.shape[1]} columns")
for name, kind in zip(data.columns, data.types):
    nulls = duckdb.sql(f'select count(*) - count("{name}") from data').fetchone()[0]
    print(f"  {name:<14}{kind!s:<10}{nulls} nulls")
