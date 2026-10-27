-- Stock on hand cannot be below zero; a negative count is a keying error at the store.
{{ config(severity='warn') }}

select count_date, store_id, product_id, on_hand
from {{ ref('stg_stock_counts') }}
where on_hand < 0
