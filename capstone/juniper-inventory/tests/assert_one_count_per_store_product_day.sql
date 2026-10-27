-- A store counts each product once per count day.
select count_date, store_id, product_id, count(*) as counts
from {{ ref('stg_stock_counts') }}
group by 1, 2, 3
having count(*) > 1
