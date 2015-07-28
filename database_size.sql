select sum(4 + bit_length(label) + 8 + 8)/8 from matches
--100
select sum(4 + bit_length(name) + bit_length(country) + 8 + 8)/8 from persons
--972441453
select sum(4 + bit_length(label) + 4 + bit_length(category))/8 from products
--423534546
select sum(4 + 4 + 4 + 8 + 8)/8 from transactions
--131262439

select (100 + 972441453 + 423534546 + 131262439)/(1024*1024*1024.0) as GB