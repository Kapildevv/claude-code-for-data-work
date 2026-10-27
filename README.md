# Claude Code for Data Work: companion files

The files for the book *Claude Code for Data Work* by Kapil Dev V. The book builds a `.claude/`
folder for one data project, a chapter at a time; this repository holds that project, its
synthetic data generator, the finished files after each chapter, and the second repository the
last chapter onboards.

## Start here

Copy the starter project out of this repository into a folder of your own, put it under git,
and generate the data. On Windows (PowerShell):

```text
New-Item -ItemType Directory -Force C:\work | Out-Null
Copy-Item -Recurse claude-code-for-data-work\juniper-lane C:\work\juniper-lane
cd C:\work\juniper-lane
git init -b main
uv sync
uv run python make_data.py
```

On macOS or Linux, `mkdir -p ~/work && cp -r claude-code-for-data-work/juniper-lane ~/work/` does
the copy; the other commands are the same. You need Python 3.14 and `uv`.

Work in your copy, never in this repository: the finished chapters below sit beside the
starter here, and Claude would read them.

## What is here

| Folder | What it holds |
|---|---|
| `juniper-lane/` | the starter project: `make_data.py` writes the nightly drop of six CSV files into `data/raw/`; `DATASET.md` describes them and the weekly KPIs |
| `chapters/chNN/` | the project's files as they stand at the end of chapter NN, to compare with yours |
| `capstone/juniper-inventory/` | the dbt-on-DuckDB repository that chapter 14 onboards |

## The data

Juniper Lane Goods, its stores, people and numbers are invented. `make_data.py` uses a fixed
seed, so your files match the book's byte for byte; every email address is at a domain reserved
for examples. The data carries a few problems on purpose: finding them is part of the book.

## Licence and trademarks

The code and data are MIT-licensed (see `LICENSE`). This repository and the book are
independent: they are not affiliated with, endorsed by or sponsored by Anthropic. Claude and
Claude Code are trademarks of Anthropic. dbt is a trademark of dbt Labs, Inc.; DuckDB is a
trademark of the DuckDB Foundation.
