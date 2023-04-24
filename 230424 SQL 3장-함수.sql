use market_db;
select * from member;

-- 순서대로 정렬 p125 (default는 ascending)
select mem_id, mem_name, debut_date
	from member order by debut_date;  

-- 거꾸로 정렬 (descending)
select mem_id, mem_name, debut_date
	from member order by debut_date desc;
    
-- 조건절의 순서
select mem_id, mem_name, debut_date, height
	from member order by height desc
		where height > 164;  -- 오류
        
-- 조건절의 순서: order by보다 먼저 필요 (추려내고 정렬)
select mem_id, mem_name, debut_date, height
	from member where height > 164
	order by height desc;  

-- 키가 164이상 & 키 순서대로 & 일찍 데뷔한 그룹이 먼저 나오도록 정렬
select mem_id, mem_name, debut_date, height
	from member where height >= 164
	order by height desc, debut_date asc;

-- limit: 출력갯수를 제한. default는 1000건. 제일 하단에 위치
select * from member;
select * from member limit 3;

-- debut_date로 오름차순으로 정렬 후 3개만 출력
select mem_id, mem_name, debut_date from member 
    order by debut_date asc
    limit 3;
    
-- 키 순 내림차순으로 정렬, 2번째부터 출력: limit 순서번호, 출력갯수 p129
select mem_id, mem_name, debut_date, height from member
	order by height desc limit 2, 3;   

-- 주소 기준 오름차순 정렬
select addr from member
	order by addr;

-- 주소 중복제거, unique만 출력: distinct
select distinct addr from member
	order by addr;

-- buy table, 멤버id 순으로 정렬하고 id, amount 출력
select * from buy;
select mem_id, amount from buy
	order by mem_id;

-- 그룹별 amount 총합을 조회
select mem_id, sum(amount) from buy
	group by mem_id;

-- 컬럼이름 변경
select mem_id "회원ID", sum(amount) "총구매갯수" from buy
	group by mem_id;

-- 그룹별 총구매액 : price * amount 
select mem_id "회원ID", sum(price * amount) "총구매액" from buy
	group by mem_id;

select mem_id "회원ID", sum(price * amount) "총구매액" from buy
	group by mem_id
    order by sum(price * amount) desc;

-- 평균구매 개수: avg
select avg(amount) "평균구매갯수" from buy;

-- 그룹별 평균 구매 개수
select mem_id, avg(amount) "평균구매갯수" from buy
	group by mem_id;

-- 전체 그룹(회원)은 몇개: count
select * from member;
select count(*) from member;

-- phone number 있는 그룹(회원)은 몇개?
select count(phone1) "연락처가 있는 회원" from member;

-- 총구매금액이 1000이상인 그룹(회원) 조회
select mem_id "회원ID", sum(price*amount) "총구매금액" from buy
    where sum(price*amount) >= 1000
    group by mem_id;   -- 오류: where와 group by 함께 사용 불가

-- having절을 사용 (where 조건절과 유사한 기능, group by 뒤에 사용)
select mem_id "회원ID", sum(price*amount) "총구매금액" from buy
    group by mem_id
    having sum(price*amount) >= 1000;

-- order by: 조건 걸러내고 마지막에 사용
select mem_id "회원ID", sum(price*amount) "총구매금액" from buy
    group by mem_id
    having sum(price*amount) >= 1000
    order by sum(price*amount) desc;



/* bookstore schema로 실습 */
-- 1. bookstore DB 선택
use bookstore;

-- 2. 도서 이름순으로 검색
select * from book;
select * from book
	order by bookname;

-- 3. 도서를 가격순으로 검색하고 가격이 같으면 이름순으로 검색
select * from book
	order by price, bookname;

-- 4. 도서를 가격의 내림차순으로 검색하고 만약 가격이 같다면 출판사의 오름차순으로 검색
select * from book
	order by price desc, publisher asc;

-- 5. 주문일자를 내림차순으로 정렬
select * from orders;
select * from orders
	order by orderdate desc;

-- 6. book테이블에서 bookname에 '썬'이 들어가있고 가격이 20000원 이하인 책을 출판사 이름으로 내림차순 조회(모든 컬럼)
select * from book;
select * from book
	where bookname like '%썬%' and price <=20000
    order by publisher desc;

-- 7. order테이블에서 saleprice가 1000원 이상인 데이터를 book_id 오름차순으로 조회(모든 컬럼)
select * from orders;
select * from orders
	where saleprice >=1000
	order by bookid asc;
















