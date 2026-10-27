-- model: sales_clean
select distinct *
from sales_raw
where quantity >= 1
