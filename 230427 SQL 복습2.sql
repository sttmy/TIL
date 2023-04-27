use sakila;

-- 1. 등급별 영화 수 합계, 평균, 최대, 최소, rating 별로 그룹화, rental_rate 별로 그룹화, 평균렌탈비용 내림차순 조회, film
select rating, count(*), sum(rental_rate), avg(rental_rate), max(rental_rate), min(rental_rate), rental_rate
	from film
    group by rating, rental_rate
    order by avg(rental_rate) desc;

-- 2. 등급별 영화 갯수, 등급, 평균 rental_rate 조회하고 평균 rental_rate 내림차순 조회
select rating, count(*), avg(rental_rate)
	from film
    group by rating, rental_rate
    order by rental_rate desc;
    
  
-- 3. 분류가 family인 film 테이블에서 서브쿼리를 이용해 조회, film, film_category, category 테이블 활용
select *
	from film F
    join film_category FC
    on F.film_id = FC.film_id
		join category C
        on FC.category_id = C.category_id
			where lower(C.name) = 'family';

select * from film where film_id in(
select film_id from film_category where category_id in(
select category_id from category where lower(name) = 'family'
));

-- tch
select film_id, title, release_year from film
where film_id in (
select film_id from film_category where category_id in
(select category_id from category where name = 'Family')
);


-- 4. action 영화 이름, 영화수, 합계(rental_rate), 평균, 최소, 최대 집계, film, film_category테이블 활용, category
select C.name, title, count(*), sum(rental_rate) 합계, avg(rental_rate) 평균, min(rental_rate) 최소, max(rental_rate) 최대
from film, category C
where film_id in(
select film_id from film_category where category_id in(
select category_id from category where lower(name) = 'action'
));

-- tch
select C.name, count(F.film_id) 영화수, sum(F.rental_rate) 합계, avg(F.rental_rate) 평균, max(F.rental_rate), min(F.rental_rate)
from film F, film_category FC
join category C on FC.category_id = C.category_id
where FC.film_id = F.film_id
group by C.name, F.rental_rate
having C.name='Action'
order by 평균 desc;

-- 5. 가장 대여비가 높은 영화 분류 조회 2개 (name, sum(ifnull)을 사용 payment테이블에서 amount합계
-- name은 category_name으로, 합계는 revenue로 별칭
-- category, film_category, inventory, payment, rental 테이블 join 후 name으로 그룹분석 후 revenue로 내림차순
select C.name, sum(FC.film_id) revenue
	from category C
    join film_category FC
    on C.category_id = FC.category_id
		join inventory I        
        on FC.film_id = I.film_id
			join rental R
			on I.inventory_id = R.inventory_id
				join payment P
                on R.rental_id = P.rental_id
				-- on R.customer_id = P.customer_id
	group by C.name
    order by revenue desc;
    
-- tch
select C.name category_name, sum(ifnull(P.amount, 0)) revenue  -- payment amount값이 없으면 0으로 입력
	from category C
	left join film_category FC on C.category_id = FC.category_id
		 left join film F on FC.film_id = F.film_id
			left join inventory I on F.film_id = I.film_id
				left join rental R on I.inventory_id = R.inventory_id
					left join payment P on R.rental_id = P.rental_id
	group by C.name
    order by revenue desc;


-- join과 left join의 차이!!!
-- join(=inner join), left join(=left outer join)


-- 6. 위의 쿼리문 결과를 뷰로 생성, v_cat_revenue로 하고 뷰를 조회
create view v_cat_revenue
	as select C.name, sum(FC.film_id) revenue
			from category C
			join film_category FC
			on C.category_id = FC.category_id
				join inventory I        
				on FC.film_id = I.film_id
					join rental R
					on I.inventory_id = R.inventory_id
						join payment P
						on R.customer_id = P.customer_id
			group by C.name
			order by revenue desc;

select * from v_cat_revenue;

-- tch
create or replace view v_cat_revenue as
select C.name category_name, sum(ifnull(P.amount, 0)) revenue  -- payment amount값이 없으면 0으로 입력
	from category C
	left join film_category FC on C.category_id = FC.category_id
		left join film F on FC.film_id = F.film_id
			left join inventory I on F.film_id = I.film_id
				left join rental R on I.inventory_id = R.inventory_id
					left join payment P on R.rental_id = P.rental_id
	group by C.name
    order by revenue desc;

select * from v_cat_revenue limit 10;