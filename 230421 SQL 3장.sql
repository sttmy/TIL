use market_db;  -- market_db를 쓰겠다

SELECT * FROM member;  -- member테이블의 전체 컬럼을 가져옴 / market_db에서 실행해야 함
SELECT * FROM market_db.member;  -- 다른db에 있는 테이블 실행할 때 (예를들어 sakila DB에서 market_db의 member를 불러옴)

SELECT addr, debut_date, mem_name FROM member;

-- 컬럼이름 별칭 부여
SELECT addr, debut_date "데뷔 일자", mem_name FROM member;

-- where 조건 사용: 블랙핑크만 불러오기
SELECT * FROM member WHERE mem_name = '블랙핑크';   

-- where 조건 사용: 멤버수 4명인 그룹의 모든 컬럼 불러오기
SELECT * FROM member WHERE mem_number = 4;

-- 키평균이 162 이상인 그룹의 멤버id와 그룹이름 불러오기
SELECT mem_id, mem_name FROM member WHERE height > 162;

-- 키평균 165이상 또는 멤버수가 6명 이상인 그룹의 name, height, 멤버수 불러오기
SELECT mem_name, height, mem_number FROM member WHERE height >= 165 or mem_number >= 6;
SELECT mem_name, height, mem_number FROM member WHERE height >= 165 and mem_number >= 6;

SELECT mem_name, height, mem_number
	FROM member 
    WHERE height >= 165 and mem_number >= 6;

-- 키가 163이상 165이하의 멤버이름, 키 불러오기
SELECT mem_name, height 
	FROM member
    -- WHERE height >= 163 and height <= 165;
    WHERE height between 163 and 165;
    
-- 주소가 경기 전남 경남 중 하나인 그룹의 이름, 주소 조회
SELECT mem_name, addr 
	FROM member
    -- WHERE addr = '경기' or addr = '전남' or addr = '경남';
    WHERE addr in('경기','전남','경남');
    
-- 이름이 우* 인 정보를 모두 불러올 때  : %를 붙임
SELECT * FROM member 
	WHERE mem_name like '우%';

-- 이름이 **핑크 인 정보를 모두 불러옴 : __ 언더바 2개, '%핑크'도 사용 가능
SELECT * FROM member
	WHERE mem_name like '__핑크';
    
SELECT * FROM member
	WHERE mem_name like '__핑크'
			and addr in ('경기', '전남');

SELECT height FROM member
	WHERE mem_name = '에이핑크';

-- 에이핑크의 키보다 키가 큰 그룹을 찾는 쿼리 (서브쿼리)
SELECT mem_name, height
	FROM member
	WHERE height > (SELECT height FROM member
						WHERE mem_name = '에이핑크');


-- ---해보기
-- bookstore 스키마 만들고
-- table 3개 만들기 (book, customer, order)
-- foreign key (custid) references Customer(custid)

