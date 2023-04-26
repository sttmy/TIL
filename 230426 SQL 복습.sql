-- actor, film, customer, staff, rental, inventory count

use sakila;

select count(*) from actor;   -- 200
select count(*) from film;  -- 1000
select count(*) from customer;  -- 599
select count(*) from staff;  -- 2
select count(*) from rental;  -- 16044
select count(*) from inventory;  -- 4581


-- 1. 배우 이름을 합쳐서 '배우' 라는 컬럼으로 조회, 대문자로 바꾸기
select * from actor; -- first_name/ last_name/ last_update
select concat(upper(first_name), ' ',upper(last_name)) as 'actor'
	from actor;
    
-- tch
select upper(concat(first_name, ' ', last_name)) as '배우'
	from actor;


-- 2.'son'으로 끝나는 성을 가진 배우 조회
select * from actor
	where last_name like '%son';

-- tch
select * from actor
	where upper(last_name) like '%SON';


-- 3. 배우들이 출연한 영화 조회, 배우 이름을 합쳐서 '배우' 컬럼, title, release year까지 세가지 조회
select upper(concat(A.first_name, ' ', A.last_name)) as 'actor', 
	F.title, F.release_year
	from actor A, film_actor FA, film F;
    
select upper(concat(A.first_name, ' ', A.last_name)) as 'actor', 
	F.title, F.release_year
	from actor A, film_actor FA, film F
    join film_actor, film
    on A.actor_id = FA.actor_id and FA.film_id = F.film_id;
    -- --- 실패

-- tch 
select upper(concat(A.first_name, ' ', A.last_name)) as 'actor', 
	F.title, F.release_year
	from actor A, film_actor FA, film F
    where A.actor_id = FA.actor_id and FA.film_id = F.film_id;

	
-- 4. 같은 last name별 배우 숫자
select last_name, count(*) as 'num' from actor
	group by last_name;
    
-- + 명수 내림차순, 성 기준으로는 오름차순
select last_name, count(*) as 'num' from actor
	group by last_name
    order by num desc, last_name asc;


-- 5. country table, id와 국가 조회, Australia, Germany
desc country;
select count(*) from country; -- 109개

select country_id, country from country
	where country = 'Australia' or country = 'Germany';

-- tch 
select country_id, country from country
	where country in ('Australia', 'Germany');

-- 6. staff 성과 이름을 합치고 staff로 하고, address 테이블을 합침,
-- address, district, postal_code, city_id 조회
select concat(first_name, ' ', last_name) as 'staff',
	address, district, postal_code, city_id
    from staff S, address A 
    where S.address_id = A.address_id;

-- tch
select concat(first_name, ' ', last_name) as 'staff',
	address, district, postal_code, city_id
    from staff S
    left join address A 
    on S.address_id = A.address_id;


-- 7. payment table, staff 이름 기준으로 2005년도 7월 매출 조회
select * from payment;   -- payment_date, amount

select concat(first_name, ' ', last_name) 'staff', sum(amount) 'total'
	from staff, payment
    where date(payment_date) in ('2005-07-01', '2005-07-31')
    group by staff;

select date(payment_date), sum(amount) 
	from payment;

-- tch
select concat(first_name, ' ', last_name) 'staff', sum(amount) 'total'
	from staff S
    left join payment P
    on S.staff_id = P.staff_id
    where month(P.payment_date) = 7 and year(P.payment_date) = 2005
    group by staff;    
    
select concat(first_name, ' ', last_name) 'staff', sum(amount) 'total'
	from staff S
    left join payment P
    on S.staff_id = P.staff_id
    where date(P.payment_date) between '2005-07-01' and '2005-07-31'
    group by staff;
describe payment;


-- 8. 영화별 출연 배우의 수, film, film_actor 활용, title, 배우 수 출력
select F.title, count(actor_id) actor
	from film F
    left join film_actor FA
    on F.film_id = FA.film_id
    group by title;

-- tch
select F.title, count(*) actor
	from film F
    left join film_actor FA
    on F.film_id = FA.film_id
    group by title
    order by actor desc;


-- 9.영화제목이 halloween nuts, 배우이름이 성과 이름이 합쳐서 나오도록
-- 서브쿼리, 조건절에 쿼리를 새로 만들어야 함.
select concat(A.first_name,' ', A.last_name) actor
	from actor A, film F
    left join film_actor FA
    on A.actor_id = FA.actor_id and F.film_id = FA.film_id
    where F.title = 'Halloween nuts';

-- tch
select concat(first_name,' ', last_name) actor
	from actor
	where actor_id in
		(select actor_id 
				from film_actor 
				where film_id in
						(select film_id
								from film
								where lower(title) = lower('Halloween nuts')));

-- 10. 국가가 canada인 고객 이름을 서브쿼리로 찾기
-- 고객 성과 이름을 합치고, email
-- customer, address, city, country 테이블 활용, 서브쿼리 3번
select concat(first_name,' ', last_name) customer, email
	from customer    
    where address_id in
		(select address_id
				from address
                where city_id in
					(select city_id
							from city
                            where country_id in
								(select country_id
										from country
                                        where lower(country) = lower('Canada'))));

-- tch
select concat(first_name,' ', last_name) customer, email from customer 
where address_id in (
select address_id from address where city_id in (
select city_id from city where country_id in (
select country_id from country where lower(country) = lower('Canada')
)));

-- 11. join을 활용해서 국가가 Canada인 고객 이름
select concat(first_name,' ', last_name) customer, email from customer C
	join address A
	on C.address_id = A.address_id
		join city CT
		on A.city_id = CT.city_id
			join country CTR
			on CT.country_id = CTR.country_id
				where lower(CTR.country) = lower('Canada');
                
-- tch
select concat(C.first_name,' ', C.last_name) customer, C.email from customer C
	join address A on C.address_id = A.address_id
    join city CT on A.city_id = CT.city_id
    join country CTR on CT.country_id = CTR.country_id
    where lower(CTR.country) = lower('Canada');
    

-- 12. 영화에서 PG등급, G등급 조회, rating, count(*) 수량 film
select * from film;
select rating, count(*) from film
	group by rating
    having rating in ('PG', 'G');
    
-- tch
select rating, count(*) from film
    where rating ='PG' or rating = 'G'
    group by rating;    
    
-- 13. PG등급 또는 G등급 영화 이름, rating, title, release_year
select title, rating, release_year from film
	where rating in ('PG','G');
    
-- 14. 등급별 영화갯수
select rating '등급', count(*) '영화 수' from film
	group by rating;
    
describe film;


-- 15. film테이블 , rental_rate 1~6 이하인 등급별 영화 수?
select rating, count(*) from film
	where rental_rate between 1 and 6
	group by rating;
