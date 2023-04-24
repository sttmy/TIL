-- 데이터 삽입: INSERT

use market_db;

create table hongong1 (toy_id int, toy_name char(4), age int);
insert into hongong1 value(1, '우디', 25);
select * from hongong1;
insert into hongong1(toy_id, toy_name) value(2, '버즈');
insert into hongong1(toy_name, age, toy_id) value('제시', 20, 3);

-- 삭제: 
-- set sql_safe_updates = 0;
-- delete from hongong1 where toy_name = '우디';


create table hongong2(
	toy_id int auto_increment primary key,   -- auto_increment 자동증가
    toy_name char(4),
    age int);
select * from hongong2;
insert into hongong2 value(null, '보핍', 25);
insert into hongong2 value(null, '슬랭키', 22);
insert into hongong2 value(null, '렉스', 21);

-- 마지막 인덱스 id 확인
select last_insert_id(); 

-- 테이블 속성값 변경, 100부터 시작
alter table hongong2 auto_increment=100;
insert into hongong2 value(null, '재남', 35);
select * from hongong2;


create table hongong3(
	toy_id int auto_increment primary key,   
    toy_name char(4),
    age int);
    
-- 1000부터 시작
alter table hongong3 auto_increment = 1000;

-- auto_increment 3씩 증가하도록 변경
-- @@ : 시스템변수
set @@auto_increment_increment =3;
show global variables;  -- 시스템변수 목록 확인

insert into hongong3 value(null, '토마스', 20);
insert into hongong3 value(null, '제임스', 23);
insert into hongong3 value(null, '고든', 25);
select * from hongong3;


-- market_db에서 작업하는데, world의 테이블 일부에 접근
select * from world.city;

-- 전체 행 갯수: count
select count(*) from world.city;

-- describe p145
Desc world.city;
desc world.city;

select * from world.city limit 5;  -- index 0번째부터 5개

-- city테이블의 데이터를 market_db로 가져오려 함
create table city_popul(
	city_name char(35), 
    population int);
    
select * from city_popul;

insert into city_popul
	select Name, population from world.city;
    
select * from city_popul limit 5;


-- 데이터 수정: UPDATE 
select * from city_popul
	where city_name='Seoul';
update city_popul     -- update할 테이블
	set city_name = '서울'
    where city_name = 'Seoul' ;  -- Seoul 컬럼을 서울로 바꿔라
select * from city_popul
	where city_name='서울';

-- New York을 찾아서 뉴욕으로 바꾸고 인구를 0으로 변경
select * from city_popul
	where city_name='New York';
update city_popul
	set city_name = '뉴욕', population = 0 
    where city_name = 'New York';
select * from city_popul
	where city_name='뉴욕';
    
-- 모든 도시의 인구수를 1만 단위로 변경
select * from city_popul limit 5;
update city_popul
	set population = population / 10000;
select * from city_popul limit 5;


-- 데이터 삭제: DELETE
delete from city_popul
	where city_name like 'New%';  -- 11개가 지워짐

-- update는 DB자체를 변경하므로 주의 필요, 조건문 없이 이름바꾸면 위험
update city_popul
	set city_name = '서울';
select * from city_popul;

-- ---------------- create table ------------------
create table big_table1(select * from world.city, sakila.country);
create table big_table2(select * from world.city, sakila.country);
create table big_table3(select * from world.city, sakila.country);

select count(*) from big_table1;

-- p151 데이터 삭제하는 방법: delete, drop, truncate. 사용 주의 필요. 행단위 삭제 가능한 delete를 주로 사용
delete from big_table1;
select * from big_table1; -- delete하면 테이블을 지웠지만 테이블 틀은 남아있음. 조건문 사용 가능

drop table big_table2;
select * from big_table2; -- drop하면 테이블 자체를 빼버림, 시간도 매우 짧게 소요

truncate big_table3;
select * from big_table3; -- truncate해도 테이블 틀은 남아있음, 시간 짧게 소요. 조건문 못씀

