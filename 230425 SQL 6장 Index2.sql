/* 6장 3절 인덱스의 실제 사용*/
-- 인덱스 생성과 제거

use market_db;
select * from member;
show index from member;
show table status like 'member';
-- data_length: 16384, 1page
-- index_length: 보조인덱스의 크기 unique가 없으므로 없음

-- p313
create index idx_member_addr
	on member(addr);
analyze table member;
show table status like 'member';
-- index_length: 16384(16KB) 늘어남

create unique index idx_member_number
	on member(mem_number);
-- 오류: 데이터 내 중복값이 있음

create unique index idx_member_name
	on member(mem_name);
-- 현재는 중복값이 없지만, 나중에는 중복이 있을 수 있으므로 name같은 것은 사용하지 않는 게 바람직
show index from member;

-- 중복된 값을 넣었을 경우 어떻게 되나?
insert into member values ("MOO",'마마무',2, '태국', '001', '12341234', 155, '2020.10.10.');
-- 오류. 같은 이름이 있으므로 안 들어감
analyze table member;
show index from member;
show table status like 'member';


-- p316 -------------------------------------------
select * from member;

select mem_id, mem_name, addr 
	from member
    where mem_name = '에이핑크';
-- execution plan: single row가 찍혀 있으면, index 사용해서 검색했다고 보면 됨

-- 단순보조 인덱스로 mem_number를 지정해 둠
create index idx_member_mem_number
	on member(mem_number);
analyze table member; -- index 적용 
-- msg_text: OK

-- mem_name 고유보조인덱스 / mem_number 단순보조인덱스 (중복있음?)
select mem_name, mem_number
	from member
	where mem_number >= 7;
-- execution plan: index range scan 단순보조인덱스 사용해서 찾음

select mem_name, mem_number
	from member
	where mem_number >= 1;
-- execution plan: full table scan 전체 다 뒤짐. 인덱스 사용하지 않음. 자동으로 full scan

select mem_name, mem_number
	from member
	where mem_number *2 >= 14;
-- 연산이 들어가면 인덱스를 사용하지 않음. full table scan
-- index 쓰게 하려면? column 자체에는 연산을 빼줌
select mem_name, mem_number
	from member
	where mem_number >= 14 / 2;
-- index range scan

    
