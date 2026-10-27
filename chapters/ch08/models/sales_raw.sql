-- model: sales_raw
select
    order_id,
    order_date,
    store_id,
    customer_id,
    product_id,
    quantity,
    cast(unit_price as decimal(10,2)) as unit_price
from read_parquet('data/parquet/sales.parquet')
