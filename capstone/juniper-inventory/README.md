# juniper-inventory

Stock counts, supplier deliveries and the weekly reorder list for Juniper Lane Goods'
twelve stores (a fictional company; all data is invented). dbt on DuckDB.

## Run it

```text
uv sync            # Python 3.14, dbt-core and dbt-duckdb as pinned in uv.lock
uv run dbt build   # loads seeds/, builds the models, runs the tests
```

The database is `inventory.duckdb` in this folder (`profiles.yml` is here too, so nothing goes
in `~/.dbt`). `dbt build` currently finishes with two warnings; see *Known issues*.

## Layout

| Path | What |
|---|---|
| `seeds/` | the warehouse feed: `suppliers`, `products`, `stores`, `stock_counts` (one count per store and product every Monday, 2026-09-07 to 2026-09-28) and `receipts` (supplier deliveries) |
| `models/staging/` | one view per seed, renamed and typed; tests in `_staging.yml` |
| `models/marts/fct_stock_on_hand.sql` | stock at the latest count, one row per store and product |
| `models/marts/mart_reorder_list.sql` | everything at or below its reorder point, topped up to twice the reorder point in whole cases |
| `models/marts/mart_supplier_on_time.sql` | deliveries per supplier and the share that arrived within the quoted lead time |
| `tests/` | singular tests |
| `make_seeds.py` | regenerates `seeds/` byte for byte; run only to rebuild them |

## Known issues

- `assert_no_negative_on_hand` warns: some stores keyed counts in as negative numbers. The
  reorder list does not filter them yet.
- `relationships` on `stg_receipts.product_id` warns: a couple of deliveries carry product ids
  that are not in `products`.
