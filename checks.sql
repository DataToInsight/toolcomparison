select date_trunc('day', moment), products_id % 3, count(*), sum(during_match)
from (
	select *, case when exists (select * from matches where start<=moment and moment<=finish) then 1 else 0 end as during_match from transactions
	) as a
group by 1,2
order by 1,2 asc

select date_trunc('day', moment), category, count(*), sum(during_match)
from (
	select *, case when exists (select * from matches where start<=moment and moment<=finish) then 1 else 0 end as during_match from transactions
	) as a left join products on a.products_id = products.id
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

select persons_id_buyer, count(*) from transactions group by 1 order by 2 desc fetch first 10 rows only

select p.label, p.price*t.price_factor
from transactions t left join products p on t.products_id=p.id 
order by 2 desc fetch first 10 rows only

-- (8+432/8+8+104/8)*10000000 + (8+8+8+8+8)*37503554 + (8+360/8+616/8+8+8)*15000000 + (80/8+8+8)*8
-- = 