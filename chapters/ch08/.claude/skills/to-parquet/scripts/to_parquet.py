"""Convert the nightly CSV files to Parquet.

Run it from the project root with the folder that holds the CSV files:

    uv run python .claude/skills/to-parquet/scripts/to_parquet.py data/raw

Every CSV in that folder becomes <name>.parquet in data/parquet/. The source folder is only read.
"""

import argparse
import sys
from pathlib import Path

import duckdb

parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
parser.add_argument("source", help="folder with the CSV files, such as data/raw")
parser.add_argument("--out", default="data/parquet", help="folder for the Parquet files")
args = parser.parse_args()

source, out = Path(args.source), Path(args.out)
files = sorted(source.glob("*.csv"))
if not files:
    sys.exit(f"no CSV files in {source}")
if out.resolve() == source.resolve():
    sys.exit(f"{out} is the source folder: the Parquet files go somewhere else")

out.mkdir(parents=True, exist_ok=True)
for csv_file in files:
    target = out / f"{csv_file.stem}.parquet"
    duckdb.sql(f"copy (select * from read_csv('{csv_file.as_posix()}')) to '{target.as_posix()}' (format parquet)")
    rows = duckdb.sql(f"select count(*) from read_parquet('{target.as_posix()}')").fetchone()[0]
    print(f"{target.as_posix():<30}{rows:>7,} rows")
