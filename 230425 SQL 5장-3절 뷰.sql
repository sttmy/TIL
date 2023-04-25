/* 5장 3절 뷰*/
-- 뷰: 매번 select로 겹겹이 사용하는 게 아니라 저장되어 있는 것을 쉽게 활용하려 함. 바로가기 개념
select mem_id, mem_name, addr from member;

-- 뷰를 만드는 형식
use market_db;
create view v_member
	as select mem_id, mem_name, addr from member;
select * from v_member;

select mem_name, addr from v_member
	where addr in ('서울','경기');
    
create view v_memberbuy
	as select B.mem_id, M.mem_name, B.prod_name, M.addr,
				concat(M.phone1, M.phone2) '연락처'
		from buy B inner join member M 
		on B.mem_id = M.mem_id;
        
select * from v_memberbuy where mem_name = '블랙핑크';
select * from v_member where mem_name = '블랙핑크';

-- 뷰의 생성과 삭제
create view v_viewtest1
	as select B.mem_id 'Member ID', 
			  M.mem_name as "Member Name", 
			  B.prod_name "Product Name", 
			  concat(M.phone1, M.phone2) as 'Office Phone'
		from buy B inner join member M 
		on B.mem_id = M.mem_id;

select * from v_viewtest1; 
select 'Member ID', "Member Name" from v_viewtest1;
-- 오류: '', ""으로 가져올 수 없음 ``(backtick)으로 가져와야 함
select `Member ID`, `Member Name` from v_viewtest1;

-- view테이블 수정
alter view v_viewtest1
	as select B.mem_id '회원ID', 
			  M.mem_name as "회원이름", 
			  B.prod_name "제품이름", 
			  concat(M.phone1, M.phone2) as '연락처'
		from buy B inner join member M 
		on B.mem_id = M.mem_id;
        
select `회원ID`, `회원이름` from v_viewtest1;
select '회원ID', '회원이름' from v_viewtest1;

-- view테이블 삭제
drop view v_viewtest1;

-- view생성 또는 수정
create or replace view v_viewtest2
	as select mem_id, mem_name, addr from member;

describe v_viewtest2;  -- primary key까지 보여주진 않음
describe member;

show create view v_viewtest2; -- query문이 어떻게 완성이 됐는지 확인 가능
-- Form editor 

-- viewtable 수정하기
select * from v_member;
update v_member set addr = '부산' where mem_id = 'BLK';

insert into v_member(mem_id, mem_name, addr) 
	values('BTS', '방탄소년단', '경기');
-- 오류: update는 되지만 insert는 안 됨
-- not null값이 있을 수 있음 view에서 insert는 안 됨
-- 원 데이터가 모두 not null값이든지, insert를 원데이터에서 해주든지

select * from member;
drop view v_height167;
-- 조건식, 키가 167 이상인 뷰 만들어보기

create view v_height167
	as select * from member
	where height >= 167;
select * from v_height167;

-- 키가 167미만인 데이터 삭제
delete from v_height167
	where height < 167;

-- unsafe옵션: 지우기 방지 옵션    
select @@sql_safe_updates;
set sql_safe_updates=0;       -- unsafe옵션을 꺼두어야(0) 실행이 됨


-- 데이터 입력
insert into v_height167 values('TRA', '티아라', 6, '서울', null, null, 159, '2005-01-01');
select * from v_height167;
-- output에는 데이터가 입력이 되었다는 메시지가 뜨지만, 실제로 입력이 안 됨. 키167이상 조건에 맞지 않음

alter view v_height167
	as select * from member where height >= 167
    with check option;  -- 키 167 이상의 데이터는 입력이 안 되도록 하는 옵션임
insert into v_height167 values('TRA', '티아라', 6, '서울', null, null, 159, '2005-01-01');
insert into v_height167 values('TOB', '텔레토비', 4, '영국', null, null, 140, '1995-01-01');

select * from member;

-- 원본테이블 삭제 시 뷰는?
create view v_complex
	as select B.mem_id, M.mem_name, B.prod_name, M.addr
	from buy B inner join member M
    on B.mem_id = M.mem_id;

drop table if exists buy, member;
-- 원본테이블 삭제할 경우, 뷰도 내용이 삭제됨

-- ------ 원본테이블 변경될 경우, 뷰테이블도 변경됨. master권한 있는 경우에는 뷰 변경 시 원본도 변경됨..?