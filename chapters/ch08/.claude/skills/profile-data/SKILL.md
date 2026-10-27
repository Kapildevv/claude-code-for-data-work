---
name: profile-data
description: Use when asked to profile, inspect or check a data file, or the whole nightly drop in data/raw/. Reports rows, types and nulls for one file, or the rows that break Luis's five promises for the drop.
argument-hint: <path to a data file, or nothing for the whole drop>
allowed-tools:
  - Bash(uv run python .claude/skills/profile-data/scripts/profile.py *)
  - PowerShell(uv run python .claude/skills/profile-data/scripts/profile.py *)
  - Bash(uv run python .claude/skills/profile-data/scripts/dq_profile.py)
  - PowerShell(uv run python .claude/skills/profile-data/scripts/dq_profile.py)
---

# Profile data

Profile data the same way every time, so that two analysts' profiles can be compared line by line. Run each script as one command from the project root, never joined to another with `cd` or `&&`.

1. If the request names a file, or $ARGUMENTS is a path, run `uv run python .claude/skills/profile-data/scripts/profile.py <path>` and reply in the shape below.
2. If the request is about the whole drop, or $ARGUMENTS is empty, run `uv run python .claude/skills/profile-data/scripts/dq_profile.py`. It prints each file's row count and how many rows break each of Luis's five promises, and saves the same text to `out/dq_profile.txt`. Copy its output into the reply unchanged.
3. Do not clean, fix or delete anything, and never write to `data/raw/`. This skill only reads.

For one file, finish with the profile in exactly this shape, and nothing after it:

    File: <path>
    Rows: <count>   Columns: <count>
    Nulls: <column (count), ...> or none
    Types: <column type, ...>
