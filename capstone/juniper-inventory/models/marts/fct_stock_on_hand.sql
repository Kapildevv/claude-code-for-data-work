-- Stock on hand at the latest count, one row per store and product.
with latest as (
    select max(count_date) as count_date from {{ ref('stg_stock_counts') }}
)

select
    c.count_date,
    c.store_id,
    c.product_id,
    p.product_name,
    p.category,
    p.supplier_id,
    c.on_hand,
    p.reorder_point,
    c.on_hand <= p.reorder_point as needs_reorder
from {{ ref('stg_stock_counts') }} as c
join latest using (count_date)
join {{ ref('stg_products') }} as p using (product_id)
