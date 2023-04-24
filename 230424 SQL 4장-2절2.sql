-- TRIM(): 문자열 좌우공백 제거, 파이썬 strip과 같음
select trim(' 안녕하세요    ');

-- 문자열 좌우 문자 제거 (both)
select trim(both '안' from '안녕하세요안');
select trim(both '안' from '안녕하세요');
select trim(both '안' from '녕하세요안안');

-- 문자열 공백 좌측만 제거
select trim(leading from ' 안녕하세요    '); 
select ltrim('        안녕하세요         ');

-- 문자열 공백 우측만 제거
select trim(trailing from '    안녕하세요    '); 
select rtrim('        안녕하세요         ');

-- 문자열 좌측 문자 제거
select trim(leading '안' from '안녕하세요안');

-- 문자열 우측 문자 제거
select trim(trailing '안' from '안녕하세요안');

-- length
select length('hello');
select character_length('hello2341ldk');
select char_length('Hello');

select length('안녕');    -- 6 : 자음 모음 총6개
select character_length('안녕');    -- 2 : 음절갯수
select char_length('안녕');    -- 2 : 음절갯수


-- 대소문자 변경: upper, lower
select upper('sql로 시작하는 하루');
select lower('A에서 Z까지!');
select upper('a에서 Z까지!'); 


-- 추출: substring
select substring('안녕하세요', 2, 3);   -- index 2번째부터 3글자
select substring('안.녕.하.세.요', 2, 3);
select substring_index('안.녕.하.세.요', '.', 2);  -- .을 기준으로 나눌때 2번째까지
select substring_index('안.녕.하.세.요', '.', -3);  -- .을 기준으로 나눌때 뒤에서부터 3번째까지
select substring_index('안녕.하.세.요', '.', 2);  -- .을 기준으로 나눌때 2번째까지

select left('안녕하세요', 2);
select right('안녕하세요', 2);

-- 결합 concat
select concat('홍길동','모험');
select concat_ws(',', '홍길동','모험');   -- ,를 끼고 합침 Word Seperator
select '홍길동','모험';
select concat_ws(':', bookname, publisher) '책제목: 출판사'
	from book;
select bookname, ":", publisher from book;

-- customer의 name과 phone을 ':'로 묶기
select group_concat(username, ':', phone) as '전화' from customer;
select concat(username, ':', phone) as '전화' from customer;
select concat_ws(':', username, phone) as '전화' from customer;

-- 현재 date / time 출력
select Now(), sysdate(), current_timestamp;
select Now(), sysdate(), current_timestamp();
select curtime(), current_time(), current_time;

-- 날짜/시간 증감함수
select adddate('2021-08-31', interval 5 day);
select adddate('2021-8-31', interval 1 month);
select addtime('2021-12-31 23:59:59', '1:1:1');
select addtime('09:00:00', '2:10:10');

-- 날짜/시간차이 계산
select datediff('2022-01-01',now());
select datediff('2023-03-06',now());
select timediff('23:23:59', '02:01:01');
select timediff('09:30:00', curtime());

-- 날짜/시간 생성
select makedate(2021, 55);   -- 2021-01-01 ~ 55일 뒤 날짜
select date_format(makedate(2021, 55), '%Y.%m.%d'); -- YYYY.mm.dd
select date_format(makedate(2021, 55), '%y.%m.%d'); -- yy.mm.dd
select date_format(makedate(2021, 55), '%y.%M.%d'); -- yy.Month.dd
select maketime(11,11,10);
select quarter('2021-04-04');   -- 분기 값 반환


-- 데이터 형식 변환 함수
select avg(saleprice) as '평균 구매가' from orders;   -- 기본: float 실수로 반환
select cast(avg(saleprice) as signed integer)
			as '평균 구매가' from orders;   -- as signed integer 정수로 반환

-- join쓰지 않고 테이블 결합
select username, saleprice
	from customer C, orders O
    where C.custid = O.custid;

-- join써서 테이블 결합: 기본값은 inner join
select username, saleprice
	from customer C join orders O
    on C.custid = O.custid;

-- 1.도서 가격이 20000원 이상인 도서를 주문한 고객의 이름, 주문 도서 이름을 출력, where 조건만 사용

select * from customer;
select * from orders;
select * from book;
select C.username, B.bookname
	from orders O join customer C
    on O.custid = C.custid;
    
-- tch
select C.username as '이름', B.bookname as '도서명'
	from customer C, orders O, book B
    where C.custid = O.custid
		and O.bookid = B.bookid 
        and B.price >= 20000;

-- 2. 고객별로 주문도서의 총판매액, 고객이름을 주문일자로 정렬 (group by 집계 후 order by로 정렬)
select sum(O.saleprice) as '총판매액', C.username as '이름', O.orderdate as '주문일자'
	from customer C, orders O
    where C.custid = O.custid
    group by O.custid
    order by O.orderdate;

-- tch
select C.username as '이름', sum(O.saleprice) as '총판매액'
	from customer C, orders O
    where C.custid = O.custid
    group by C.username 
    order by O.orderdate;
    

-- 3.outer join 외부조인 활용, 도서를 구매하지 않은 고객을 포함해 고객 이름, 전화번호와 주문도서의 판매가격을 출력
select C.username, C.phone, O.saleprice
	from customer C
    left outer join orders O
    on C.custid = O.custid;
    
-- tch
select C.username, O.saleprice
	from customer C
    left outer join orders O
    on C.custid = O.custid;