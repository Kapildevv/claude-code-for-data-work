select
    product_id,
    product_name,
    category,
    supplier_id,
    reorder_point,
    case_pack
from {{ ref('products') }}
