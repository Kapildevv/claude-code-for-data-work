-- Delivery performance per supplier: a delivery is on time when it arrives within
-- the supplier's quoted lead time.
select
    r.supplier_id,
    s.supplier_name,
    s.lead_time_days,
    count(*) as deliveries,
    count(*) filter (where r.days_to_arrive <= s.lead_time_days) as on_time,
    round(count(*) filter (where r.days_to_arrive <= s.lead_time_days) / count(*), 3) as on_time_rate,
    round(avg(r.days_to_arrive), 1) as avg_days_to_arrive
from {{ ref('stg_receipts') }} as r
join {{ ref('stg_suppliers') }} as s using (supplier_id)
group by 1, 2, 3
order by 1
