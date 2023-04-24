/* 4장 2절: join*/ 
use market_db;

-- ---------------- inner join: 교집합 ----------------
-- buy테이블과 member테이블 join (동일정보 컬럼: mem_id)
-- buy테이블 기준으로 member테이블을 붙임. buy에 없는 member는 사라짐
select * from buy 
	inner join member
    on buy.mem_id = member.mem_id
    where buy.mem_id = 'GRL';

select mem_id, mem_name, prod_name, addr, concat(phone1, phone2) as '연락처'
	from buy inner join member
		on buy.mem_id = member.mem_id;
        -- 오류: select 뒤 mem_id를 어느 테이블에서 가져와야 할 지 명시 필요

select buy.mem_id, mem_name, prod_name, addr, concat(phone1, phone2) as '연락처'
	from buy inner join member
		on buy.mem_id = member.mem_id;
-- select 뒤 변수, 어느 테이블에서 가져와야 하는지 모두 명시가 필요하지만 코드가 복잡해짐
-- 따라서 join하는 테이블의 별칭을 만들어서 간소화함

select B.mem_id, M.mem_name, B.prod_name, M.addr, concat(M.phone1, M.phone2) as '연락처'
	from buy B   -- buy의 별칭은 B
		inner join member M   -- member테이블의 별칭은 M
		on B.mem_id = M.mem_id;

-- 중복 제외, 1번이라도 구매한 회원만 추리기: distinct
select distinct M.mem_id, M.mem_name, M.addr
	from buy B   -- buy의 별칭은 B
		inner join member M   -- member테이블의 별칭은 M
		on B.mem_id = M.mem_id
        order by M.mem_id;

-- ---------------- outer join: left A기준 / right B기준 ----------------
-- 데이터가 없어도 join된 모든 데이터 출력 (없으면 null값 부여) left outer join
select M.mem_id, M.mem_name, B.prod_name, M.addr
	from buy B
		left outer join member M
        on M.mem_id = B.mem_id
        order by M.mem_id;
        
-- join된 모든 데이터 출력 (없으면 null값 부여)
select M.mem_id, M.mem_name, B.prod_name, M.addr
	from member M
		right outer join buy B
        on M.mem_id = B.mem_id
        order by M.mem_id;

-- 구매이력 없는 회원만 추리기: 멤버아이디, product name, 멤버이름, 멤버주소    
select distinct M.mem_id, M.mem_name, B.prod_name, M.addr
	from member M
		left outer join buy B
        on M.mem_id = B.mem_id
        where B.prod_name is null
        order by M.mem_id;
        

-- ---------------- 기타 join: A행 * B행 모두 크로스로 join -----------------
-- 내용적인 의미는 없지만 대용량 데이터를 만들 때 사용
select * from buy
	cross join member;

select count(*) from world.city;    
select count(*) from sakila.inventory
	cross join world.city;

-- ---------------- self join 자체조인: ----------------------------
create table emp_table (
	emp char(4), manager char(4), phone varchar(8));
    
insert into emp_table value ('대표', null, '0000');
insert into emp_table value ('영업이사', '대표', '1111');
insert into emp_table value ('관리이사', '대표', '2222');
insert into emp_table value ('정보이사', '대표', '3333');
insert into emp_table value ('영업과장', '영업이사', '1111-1');
insert into emp_table value ('경리부장', '관리이사', '2222-1');
insert into emp_table value ('인사부장', '관리이사', '2222-2');
insert into emp_table value ('개발팀장', '정보이사', '3333-1');
insert into emp_table value ('개발주임', '정보이사', '3333-1-1');

-- 같은 emp_table에서 가져오지만, 별칭을 다르게 
select A.emp '직원', B.emp '직속상관', B.phone '직속상관연락처'
	from emp_table A
    inner join emp_table B
    on A.manager = B.emp;

select A.emp '직원', B.emp '직속상관', B.phone '직속상관연락처'
	from emp_table A
    inner join emp_table B
    on A.manager = B.emp
    where A.emp = '경리부장';
    
    
-- ------------------------- 실습 --------------------------------
use bookstore;

-- 1. 구매고객이 8000원 이상 도서를 2권 이상 주문한 고객 이름, 수량, 판매금액을 조회
select * from orders;
select * from customer;

select C.username, O.orderid, sum(O.saleprice)
	from orders O
    left join customer C
    on O.custid = C.custid
    group by O.custid;

-- tch
select C.username, O.custid, count(*) as '수량', sum(O.saleprice) as '판매액'
	from orders O
    left join customer C
    on O.custid = C.custid
    where O.saleprice >=8000
    group by custid
	having count(*) >=2;