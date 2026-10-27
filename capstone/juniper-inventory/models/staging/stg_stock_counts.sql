select
    count_date,
    store_id,
    product_id,
    on_hand
from {{ ref('stock_counts') }}
