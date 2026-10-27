select
    supplier_id,
    supplier_name,
    lead_time_days
from {{ ref('suppliers') }}
