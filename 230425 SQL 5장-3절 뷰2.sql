use bookstore;
select * from book;
describe book;

insert into book values(11, 'OpenCV 파이썬', '포웨이', 23500);
insert into book values(12, '자연어 처리 시작하기', '투시즌', 20000);
insert into book values(13, 'SQL이해', '새미디어', 22000);

select * from customer;
insert into customer values(6, '박보영', '서울 서초구', '010-9999-5555');
insert into customer values(7, '오정세', '서울 중구', '010-8888-4444');
insert into customer values(8, '이병헌', '서울 성북구', '010-7777-3333');

select * from orders;
describe orders;
set foreign_key_checks = 0;  -- 외래키 무시하게 처리
set foreign_key_checks = 1;  -- 외래키 제약조건 작동하도록 처리
insert into orders values(11, 6, 12, 23500, str_to_date('2020-02-01', '%Y-%m-%d'));
insert into orders values(12, 6, 14, 44000, str_to_date('2020-02-03', '%Y-%m-%d')); 
insert into orders values(13, 8, 13, 20000, str_to_date('2020-02-03', '%Y-%m-%d'));
insert into orders values(14, 3, 13, 20000, str_to_date('2020-02-04', '%Y-%m-%d'));
insert into orders values(15, 4, 12, 23500, str_to_date('2020-02-05', '%Y-%m-%d'));
insert into orders values(16, 5, 8, 35000, str_to_date('2020-02-07', '%Y-%m-%d'));

-- 1. v_order 뷰테이블 만들기: orderid, O.custid, username, O.bookid, saleprice, O.orderdate

create view v_order
	as select O.orderid, O.custid, C.username, O.bookid, O.saleprice, O.orderdate
		from customer C
        join orders O
        on C.custid = O.custid;
select * from v_order;

-- tch
create view v_orders
	as select O.orderid, O.custid, C.username, O.bookid, O.saleprice, O.orderdate
		from customer C, orders O, book B
        where C.custid = O.custid and B.bookid = O.bookid;

-- 2. v_order 뷰테이블에서 도서가격이 20000원 이상인 레코드로 변경
alter view v_order
	as select * from customer 
		where O.saleprice >= 20000
	with check option;

-- tch
create or replace view v_orders(custid, username, address)
	as select C.custid, username, address
    from customer C, orders O, book B
	where B.price >= 20000;

select * from v_orders;

create or replace view v_orders(custid, username, address, price)
	as select C.custid, username, address, price
    from customer C, orders O, book B
	where B.price >= 20000;

-- 3. v_cust_purchase 뷰테이블 생성, C.username '고객', sum(O.saleprice) '구매액'
-- customer C, order O, 
-- C.custid = O.custid
-- 고객 기준으로 구매액을 내림차순 순서대로

-- tch
create or replace view v_cust_purchase
	as select C.username as '고객', sum(O.saleprice) '구매액'
		from customer C, orders O
        where C.custid = O.custid
        group by 고객
        order by 구매액 desc;
select * from v_cust_purchase;
