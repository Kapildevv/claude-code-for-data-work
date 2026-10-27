-- model: weekly_sales
with gross as (
    select
        date_trunc('week', order_date)::date as week_start,
        count(*) as orders,
        sum(quantity) as units,
        sum(quantity * unit_price) as gross_sales
    from sales_clean
    group by 1
),
returned as (
    select
        date_trunc('week', return_date)::date as week_start,
        count(*) as returns,
        count(*) filter (where is_late) as late_returns,
        sum(return_value) as returns_value
    from returns_clean
    group by 1
)
select
    g.week_start,
    g.orders,
    g.units,
    g.gross_sales,
    coalesce(r.returns_value, 0) as returns_value,
    g.gross_sales - coalesce(r.returns_value, 0) as net_sales,
    round(coalesce(r.returns_value, 0) / g.gross_sales, 4) as returns_rate,
    coalesce(r.returns, 0) as returns,
    coalesce(r.late_returns, 0) as late_returns
from gross as g
left join returned as r using (week_start)
order by g.week_start
