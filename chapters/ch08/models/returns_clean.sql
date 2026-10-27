-- model: returns_clean
select
    r.return_id,
    r.order_id,
    r.return_date,
    r.quantity,
    s.store_id,
    s.product_id,
    s.order_date,
    r.quantity * s.unit_price as return_value,
    r.return_date - s.order_date > 30 as is_late
from read_parquet('data/parquet/returns.parquet') as r
join sales_clean as s using (order_id)
