-- What to order this week: every store and product at or below its reorder point,
-- topped up to twice the reorder point and rounded up to whole cases.
-- A negative count is a keying error at the store, so it is left out here and
-- goes for a recount instead (the reorder-list skill prints those rows).
select
    s.store_id,
    s.product_id,
    s.product_name,
    s.supplier_id,
    sup.supplier_name,
    s.on_hand,
    s.reorder_point,
    p.case_pack,
    cast(ceil((2 * s.reorder_point - s.on_hand) / p.case_pack) * p.case_pack as integer) as order_quantity
from {{ ref('fct_stock_on_hand') }} as s
join {{ ref('stg_products') }} as p using (product_id)
join {{ ref('stg_suppliers') }} as sup on sup.supplier_id = s.supplier_id
where
    s.needs_reorder
    and s.on_hand >= 0
order by s.store_id, s.product_id
