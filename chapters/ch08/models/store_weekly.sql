-- model: store_weekly
with gross as (
    select
        date_trunc('week', order_date)::date as week_start,
        store_id,
        sum(quantity * unit_price) as gross_sales
    from sales_clean
    group by 1, 2
),
returned as (
    select
        date_trunc('week', return_date)::date as week_start,
        store_id,
        sum(return_value) as returns_value
    from returns_clean
    group by 1, 2
)
select
    g.week_start,
    g.store_id,
    st.store_name,
    g.gross_sales,
    coalesce(r.returns_value, 0) as returns_value,
    g.gross_sales - coalesce(r.returns_value, 0) as net_sales
from gross as g
left join returned as r using (week_start, store_id)
join stores as st using (store_id)
order by g.week_start, g.store_id
