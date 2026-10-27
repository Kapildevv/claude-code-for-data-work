# KPI rules for Juniper Lane's weekly report

These are the definitions behind Dana's numbers. The SQL files in `models/` implement them and
this file explains them. When a number looks wrong, compare the SQL with these rules before you
change either.

## Definitions

1. **Clean sales.** Take every row of `sales`, drop the exact repeats (a till sometimes sends a
   batch twice), then drop rows with a quantity below 1. A negative quantity is a keying error:
   report it, never count it.
2. **Gross sales** of a week: quantity times unit price, summed over the clean sales whose
   `order_date` falls in the week. A week runs Monday to Sunday.
3. **Returns value** of a week: quantity times unit price for each return whose `return_date`
   falls in the week, joined to the **clean** sales for the price and the store. A return after
   the 30-day window still counts, because the money was refunded. The report says how many
   returns were late.
4. **Net sales** is gross sales minus returns value. The **returns rate** is returns value
   divided by gross sales.
5. **Stores and products.** A store's (or product's) net sales in a week are its gross sales that
   week minus the value of the returns logged that week against its orders. The report lists the
   top 3 stores and the top 5 products by net sales; ties go to the lower id.

Money is `DECIMAL(10,2)`. DuckDB reads `unit_price` as DOUBLE, so the first model casts it.

## Checks the build must pass

- `returns_clean` has one row for every row of `returns`. More rows means a join to the raw
  sales counted a re-sent order twice.
- Gross sales minus returns value equals net sales for the whole period.
- `store_weekly` adds up to `weekly_sales`.
