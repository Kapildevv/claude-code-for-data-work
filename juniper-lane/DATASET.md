# The nightly drop: what the store system sends

Juniper Lane Goods is a fictional outdoor-gear retailer with twelve stores. Every night the
store system writes six CSV files into `data/raw/`. Luis, who runs the store systems, owns the
drop. `make_data.py` produces it for twelve weeks of trading, Monday 2026-07-06 to Sunday
2026-09-27. All names, companies and numbers are invented.

```text
python make_data.py                        # the full twelve weeks
python make_data.py --through 2026-09-20   # the drop as it stood on an earlier night
```

Every file has a header row, comma separators, UTF-8 text and ISO dates (`YYYY-MM-DD`). An
empty field means no value. Money is in US dollars with two decimals.

## The six files

### `stores.csv`: one row per store

| Column | Meaning |
|---|---|
| `store_id` | `S01` to `S12`; unique |
| `store_name` | "Juniper Lane" and the town |
| `city`, `state`, `region` | where the store is |
| `opened_on` | the date the store opened |
| `square_feet` | sales floor size |

### `products.csv`: one row per product

| Column | Meaning |
|---|---|
| `product_id` | `P001` to `P048`; unique |
| `product_name` | the name on the shelf tag |
| `category` | Tents, Sleeping, Packs, Footwear, Apparel, Cooking, Climbing or Accessories |
| `list_price` | the shelf price |
| `unit_cost` | what Juniper Lane pays the supplier for one unit |

### `customers.csv`: one row per loyalty member

| Column | Meaning |
|---|---|
| `customer_id` | `C0001` onwards; unique |
| `first_name`, `last_name` | the member's name |
| `email` | the address for receipts; every member should have one |
| `home_store_id` | the store where the member signed up |
| `joined_on` | the sign-up date |
| `loyalty_tier` | basic, silver or gold |

Every address is at `example.com`, `example.net` or `example.org`, domains reserved for
examples, so no real inbox can receive anything.

### `dates.csv`: one row per trading day

| Column | Meaning |
|---|---|
| `date_key` | the date as a number, `20260706` |
| `date` | the date |
| `day_name` | Monday to Sunday |
| `week_start` | the Monday of that week; the weekly report groups on this |
| `iso_week`, `month`, `month_name`, `quarter` | calendar labels |
| `is_weekend` | `true` on Saturday and Sunday |

### `sales.csv`: one row per order

| Column | Meaning |
|---|---|
| `order_id` | `JL-` and six digits; one per order, never repeated |
| `order_date` | the trading day of the sale |
| `store_id` | the store that made the sale |
| `customer_id` | the loyalty member who bought |
| `product_id` | what was bought (each order in this extract is one product) |
| `quantity` | how many units; always 1 or more |
| `unit_price` | the price charged per unit, after any discount |

During Labor Day week (2026-09-07 to 2026-09-13) apparel and footwear sold at 20% off.

### `returns.csv`: one row per return

| Column | Meaning |
|---|---|
| `return_id` | `R` and five digits; unique |
| `order_id` | the order the goods came from |
| `return_date` | the day the goods came back |
| `quantity` | units returned; never more than the order's quantity |
| `reason` | the reason the customer gave |

Store policy accepts a return up to **30 days** after the order date.

## What the drop promises, and what to check

Luis's system is supposed to guarantee the following. Each promise can be checked with one
query. Whether the drop keeps every promise is for you to find out.

- Every customer has an email address.
- Every `order_id` appears once in `sales.csv`.
- Every `quantity` is 1 or more.
- Every return falls within 30 days of its order.
- Every `order_id` in `returns.csv` exists in `sales.csv`.

## Dana's weekly KPIs

Dana, the operations director, reads a report every Monday about the week before
(Monday to Sunday).

| KPI | Definition |
|---|---|
| Gross sales | quantity × unit price, summed over the week's orders |
| Returns value | returned quantity × the order's unit price, summed over returns logged in the week |
| Net sales | gross sales − returns value |
| Returns rate | returns value ÷ gross sales |
| Top stores | the three stores with the highest net sales in the week |
| Top products | the five products with the highest net sales in the week |

Rows that break a promise above are reported to Luis. In the KPIs, an order sent twice counts
once and an order with a quantity below 1 does not count at all. A late return still counts,
because the money went back to the customer; the report says how many returns were late.
