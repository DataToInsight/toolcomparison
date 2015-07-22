select date_trunc('day', moment), products_id % 3, count(*), sum(during_match)
from (
	select *, case when exists (select * from matches where start<=moment and moment<=finish) then 1 else 0 end as during_match from transactions
	) as a
group by 1,2
order by 1,2 asc

	select * from matches
	select min(moment) from transactions	

select distinct id % 3, category
from products
order by category

select count(*) from matches
select count(*) from persons
select count(*) from products
select count(*) from transactions