select
    receipt_id,
    supplier_id,
    store_id,
    product_id,
    ordered_on,
    received_on,
    quantity,
    received_on - ordered_on as days_to_arrive
from {{ ref('receipts') }}
