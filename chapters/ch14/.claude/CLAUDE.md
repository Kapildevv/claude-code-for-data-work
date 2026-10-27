# juniper-inventory: stock counts and the weekly reorder list

Juniper Lane Goods counts stock in its twelve stores every Monday. This dbt project turns the
warehouse feed (five CSV files in `seeds/`) into the weekly reorder list and a supplier
on-time table, on DuckDB. A new analyst should be able to maintain it from this file and the
README, which has the layout table.

## Commands

- `uv sync` installs the pinned packages. `uv run dbt build` loads the seeds, builds the
  models and runs the tests. Today it ends `PASS=31 WARN=2 ERROR=0`.
- `uv run dbt build --select mart_reorder_list+` rebuilds one mart and what depends on it.
- `uv run python .claude/skills/reorder-list/scripts/reorder_summary.py` prints how long the
  reorder list is and which counts need a recount. Run the build first.
- Ask the `inventory` MCP server (read-only, on `inventory.duckdb`) for facts about the data.
  Servers whose names start `plugin:juniper-data-kit:` come from the sales project's kit and
  point at files this repository does not have.

## Conventions

- Staging models are views, one per seed. Marts are tables. Refer to a model with `ref()`,
  never by table name.
- The project pins dbt-core 1.12.6 (dbt v1) on purpose. Do not upgrade it to dbt v2, and add
  no package without asking first.
- Never edit `seeds/`. The warehouse feed replaces those files. Fix a data problem in a
  model, and report it. Do not run `make_seeds.py` either: it rewrites those files.
- Two tests warn on purpose until the feed is fixed: a negative count and a delivery for an
  unknown product. Do not change a test's severity to make a build quiet.
