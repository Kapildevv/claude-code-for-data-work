---
name: profile-data
description: Use when asked to profile, inspect or check a data file, such as a new CSV in data/raw/. Reports the row count, the column names and types, and the nulls in each column.
argument-hint: <path to a data file>
allowed-tools:
  - Bash(uv run python profile.py *)
  - PowerShell(uv run python profile.py *)
---

# Profile a data file

Profile one file the same way every time, so that two analysts' profiles can be compared line by line.

1. Take the path from the request: $ARGUMENTS. If it is empty, use the file the request names, looking in `data/raw/`.
2. Run `uv run python profile.py <path>` from the project root. If the project has no `profile.py`, load the file with DuckDB and count the rows, the columns and the nulls in each column instead.
3. Copy the first line of the output, the one with the row and column counts, into the reply unchanged.
4. List the columns that have nulls, each with its count. If none has a null, write `none`.
5. Do not clean, fix or delete anything, and never write to `data/raw/`. This skill only reads.

Finish with the profile in exactly this shape, and nothing after it:

    File: <path>
    Rows: <count>   Columns: <count>
    Nulls: <column (count), ...> or none
    Types: <column type, ...>
