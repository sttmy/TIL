/* 5장 테이블과 뷰 */

create database naver_db;
-- (member, buy 테이블 만들기 GUI로)

use naver_db;
drop table if exists buy, member;

CREATE TABLE member (
    mem_id CHAR(8) NOT NULL PRIMARY KEY,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED NULL
);
describe member;  -- 표를 요약해 보여줌

-- primary key를 별도로 지정 (다시해보기)
drop table if exists member;
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED,
    primary key(mem_id)
);
describe member;  

-- alter쿼리 사용해서 primary key 지정(다시해보기)
-- constraint 
drop table if exists member;
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED
);
alter table member
	add constraint 
    primary key (mem_id);
describe member;  


-- again, primary key에 별칭 달아줌
drop table if exists member;
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED,
    constraint primary key PK_member_mem_id (mem_id)
);
describe member;  


-- 다시 만들기
drop table if exists member;
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED
);

CREATE TABLE buy (
	num	int auto_increment not null primary key,
    mem_id char(8) not null,
    prod_name char(6) not null,
    foreign key(mem_id) references member(mem_id)   
);
-- 오류: reference 삼는 테이블에 primary key가 지정이 되어 있어야 foreign key로 가져올 수 있음

-- 다시만들기
drop table if exists member;
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL primary key,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED
);

CREATE TABLE buy (
	num	int auto_increment not null primary key,
    user_id char(8) not null,
    prod_name char(6) not null,
    foreign key(user_id) references member(mem_id)   
    -- 기준 테이블과 참조 테이블 외래키의 컬럼명이 같을 필요는 없음
    -- 가급적 맞춰주는 게 좋음
);


-- alter기능 사용, foreign key 지정
drop table if exists buy;
CREATE TABLE buy (
	num	int auto_increment not null primary key,
    mem_id char(8) not null,
    prod_name char(6) not null
);
alter table buy 
	add constraint 
		foreign key(mem_id) references member(mem_id);
describe buy;
describe member;
-- 'MUL': 한 곳에서는 primary key, 다른 곳에서는 foreign key로 사용되는 칼럼

insert into member values('BLK', '블랙핑크', 163);
insert into buy values(null, 'BLK', '지갑');
insert into buy values(null, 'BLK', '맥북');

select * from naver_db.buy;
select * from member;

update member set mem_id = 'PINK' where mem_id = 'BLK';
-- 오류: mem_id는 다른 테이블과 연결되어 있으므로 바꿀 수 없음  ex.회원ID 변경 어려움

update member set mem_name = '블핑' where mem_name = '블랙핑크';
update member set mem_name = '블랙핑크' where mem_name = '블핑';

delete from member where mem_id = 'BLK';
-- 오류: mem_id는 다른 테이블과 연결되어 있으므로 지울 수 없음  ex.회원ID 삭제 안 됨

-- 삭제/수정하고 싶을 경우? cascade 활용
drop table if exists buy;
CREATE TABLE buy (
	num	int auto_increment not null primary key,
    mem_id char(8) not null,
    prod_name char(6) not null
);
alter table buy 
	add constraint 
		foreign key(mem_id) references member(mem_id)
    on update cascade
    on delete cascade;
insert into buy values(null, 'BLK', '지갑');
insert into buy values(null, 'BLK', '맥북');

update member set mem_id = 'PINK' where mem_id = 'BLK';
select * from member;
select * from buy;
-- buy테이블의 mem_id도 같이 변경이 됨 

delete from member where mem_id = 'PINK';
select * from member;
select * from buy;
-- buy테이블에서도 같이 지워짐


-- p247 기타제약조건 ------------------------------
-- unique 중복되지 않음


