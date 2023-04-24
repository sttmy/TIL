/* 4장 */

use market_db;

-- 데이터 크기에 따라 테이블 각 컬럼이 담아내는 자릿수의 용량 설정을 해줘야 함
-- ----- 숫자형 -----

-- tinyint < smallint < int < bigint
-- --- tinyint: -128~127 (2^7)    2^3-1
-- --- smallint: -32768~32767 (-2^15~2^15-1)    2^4-1
-- --- int:  -2,147,483,648 ~ 2,147,483,647 (-2^31~2^31-1)     2^5-1
-- --- bigint: -9,223,372,036,854,775,808~9,223,372,036,854,775,8087 (-2^63~2^63-1)     2^6-1

create table hongong4 (
	tinyint_col tinyint,    
    smallint_col smallint,
    int_col int,
    bigint_col bigint
    );

insert into hongong4 value(127, 32767, 2147483647, 9000000000000000000);
select * from hongong4;
insert into hongong4 value(127, 32767, 2147483647, 90000000000000000000);

-- 예시
drop table if exists buy, member;
create table member (
	mem_id char(8) not null primary key,
    mem_name varchar(10) not null,       -- 이름 가변
    mem_number tinyint not null,
    addr char(2) not null,
    phone1 char(3),
    phone2 char(8),
    -- height smallint,    -- 키 보통 127이 넘으므로 tinyint를 그냥 넣으면 안 됨
    height tinyint unsigned,   -- unsigned 부호를 해제하면 0~255까지 사용 가능
    debut_date date
    );
    
-- ----- 문자형 -----
-- char: 고정문자형, char(최대255자)
-- varchar: 가변문자형, var(최대16383자?)
-- TEXT, BLOB 

drop table if exists buy, member;
create table member (
	mem_id char(8) not null primary key,   
    mem_name varchar(10) not null,       
    mem_number tinyint not null,
    addr char(2) not null,
    phone1 char(3),
    phone2 char(8),
    height tinyint unsigned,   
    debut_date date
    );

create database netflix_db;
use netflix_db;
create table movie(
	movie_id int,
    movie_title varchar(30),
    movie_director varchar(30),
    movie_star varchar(30),
    movie_script longtext,  -- 42억개 문자 저장 가능 옵션
    movie_film longblob  -- BLOB: Binary Large OBject 바이너리 데이터, 4G 
    );

-- ----- 실수형 -----
-- float로 사용


-- 변수의 사용
use market_db;
set @myVar1 = 5;
set @myVar2 = 4.25;

select @myVar1;
select @myVar2;

select @myVar1 + @myVar2;

set @txt = '가수이름 ==>';
set @height = 166;
select @txt, mem_name from member 
	where height > @height;
    
set @count = 3;
select mem_name, height
	from member
    order by height
    limit @count;      -- 오류, limit는 숫자를 직접 입력해야 함. 변수사용 불가
    
prepare mysql from 'select mem_name, height
	from member
    order by height
    limit ?';
execute mysql using @count;
-- prepare, 실행하진 않지만 쿼리를 구동 준비만 해둠
-- execute, 실제 실행문으로 실행


-- 데이터 형변환
select avg(price) '평균가격' from buy;
select cast(avg(price) as signed) '평균가격' from buy;   -- as signed 정수로 변환
select convert(avg(price), signed) '평균가격' from buy;   -- cast와 같음

select cast('2022$12$12' as date);
select cast('2022/12/12' as date);
select cast('2022%12%12' as date);
select cast('2022@12@12' as date);

-- p170
-- 단가*수량 
select * from buy;
select num, 
	concat(cast(price as char), 'X', cast(amount as char), '=') '가격X수량', 
	price * amount    -- 문자형을 concat으로 감싸줘야 함
	from buy;

select '100' + '200';
-- 자동으로 형변환해서 숫자로 기록함
-- 100200으로 출력되게 하려면 concat으로 묶어줌
select concat('100', '200');
select concat(100, '200'); 
-- 문자형, 숫자형 만나면 문자형으로 인식

-- 문자와 숫자 비교
select 1 > '2mega';   -- 숫자+문자: 정수 2로 자동 변환되어 1>2 연산
select 3 > '2MEGA';   -- 숫자+문자: 정수 2로 자동 변환되어 3>2 연산
select 0 = 'MEGA2';   -- 문자+숫자: 문자는 0으로 자동 변환되어 처리



