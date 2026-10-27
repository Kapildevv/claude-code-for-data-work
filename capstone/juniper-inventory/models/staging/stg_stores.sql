select
    store_id,
    city
from {{ ref('stores') }}
