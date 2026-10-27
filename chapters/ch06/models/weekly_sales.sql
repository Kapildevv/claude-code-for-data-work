-- model: weekly_sales
with sales as (
    select distinct
        order_id,
        order_date,
        quantity,
        cast(unit_price as decimal(10,2)) as unit_price
    from read_csv('data/raw/sales.csv')
    where quantity >= 1
),
gross as (
    select
        date_trunc('week', order_date)::date as week_start,
        sum(quantity * unit_price) as gross_sales
    from sales
    group by 1
),
returned as (
    select
        date_trunc('week', r.return_date)::date as week_start,
        sum(r.quantity * s.unit_price) as returns_value
    from read_csv('data/raw/returns.csv') as r
    join sales as s using (order_id)
    group by 1
)
select
    g.week_start,
    g.gross_sales,
    coalesce(r.returns_value, 0) as returns_value,
    g.gross_sales - coalesce(r.returns_value, 0) as net_sales
from gross as g
left join returned as r using (week_start)
order by g.week_start
