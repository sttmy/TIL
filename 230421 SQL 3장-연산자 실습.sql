/* 1. 산술연산자*/

select 1;
select 1+1;
select 0.1;
select 1-1;
select 100/20;
select 5.0/2;

-- book 테이블에서 price값에 연산해보기 
use bookstore;
select price*0.05 from book;
select price/2 from book;
select (price/2)*100 from book;


/* 2. 비교연산자*/
select 1 > 100;   -- False (0)
select 1 < 100;   -- True  (1)
select 10 = 10;   -- True  (1)   같다는 뜻
select 101 <> 10; -- 같지 않다
select 101 != 10; -- 같지 않다


/* 3. 논리연산자*/
select (10 >= 10) and (5 < 10);  -- True  (1)
select (10 > 10) and (5 < 10);   -- False (0)
select (10 > 10) or (5 < 10);    -- True  (1)
select not(10 > 10); 		     -- True  (1)


/* 4. 집계함수*/

-- count(*): 총 row갯수 (판매한 건수)
select count(*) from orders;
select count(*) from book;
select count(*) from customer;

select * from orders;
-- 고객이 주문한 도서의 총 판매액
select sum(saleprice) from orders;

-- 고객이 주문한 도서의 총 판매액 출력, '총매출'로 표시
select sum(saleprice) as '총매출' from orders;
select sum(saleprice) as 총매출 from orders;

-- 매출 평균
select avg(saleprice) as 매출평균 from orders;

-- 판매액 합계, 평균, 최저, 최고가 구하기
select sum(saleprice) as 총매출액,
	avg(saleprice) as 매출평균,
    max(saleprice) as 최고가,
    min(saleprice) as 최저가
from orders;


-- 1. 가격이 10000원보다 크고, 20000원 이하인 도서를 검색
select * from book;
select bookname, price
	from book
    where price between 10000 and 20000;


-- 2. 주문일자가 2021/02/01 ~ 2021/02/07 내 주문내역 검색
select * from orders;
select custid, bookid, orderdate 
	from orders
    where orderdate between '2021-02-01' and '2021-02-07';

-- 3. 도서번호가 3,4,5,6인 주문목록
select * from orders;
select bookid, orderid, saleprice
	from orders
    where bookid between 3 and 6;

-- 4. 박씨성을 가진 고객 
select * from customer;
select custid, username
	from customer 
    where username like '박%';

-- 5. 2번째글자가 '지'인 고객
select * from customer;
select custid, username
	from customer 
    where username like '_지_';

-- 6. '철학의 역사'를 출간한 출판사
select * from book;
select bookname, publisher
	from book
    where bookname = '철학의 역사';

-- 7. 도서이름에 썬으로 일치하고 20000원 이상인 도서
select * from book;
select bookname, price
	from book
    -- where bookname = '%썬' and
	where price >= 20000;







