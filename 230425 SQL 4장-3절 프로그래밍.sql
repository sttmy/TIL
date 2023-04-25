/* p196 delimiter -----------------------------------------
Delimiter 구문문자 ;. 문법의 끝을 나타내는 역할
명령어 없이 프로시저를 작성하면 세미콜론으로 끝나는 SQL 부분이 나눠져 서버로 보내짐
Delimiter 없이 이렇게 프로시저를 짠다면 IF ~ THEN; 따로, ~; 따로, END IF; 따로 서버로 보내져서
어디부터 어디까지가 프로시저인지 구분하지 못하게 됨

DELIMITER $$ 
create procedure 함수이름()
begin

end $$
DELIMITER ;
call 함수이름;

*/

use bookstore;
DELIMITER $$
create procedure ifProc1()
begin
	if 100 = 100 then
		select '100은 100과 같다';
	end if;  -- if문 종료
end $$
DELIMITER ;
call ifProc1();

drop procedure if exists ifProc2;
DELIMITER $$
create procedure ifProc2()
begin
	declare myNum int;  -- 변수선언. 함수 밖에서는 @ (ex. set @myNum), 함수 안에서는 declare
    set myNum = 200;
    if myNum = 100 then
		select '100입니다';
	else 
		select '100이 아닙니다';
	end if; 
end $$
DELIMITER ;
call ifProc2();

-- 날짜계산 procedure 만들기

use market_db;
DELIMITER $$
create procedure ifProc3()
begin
	declare debutDate date;  -- 데뷔일자
    declare curDate date;   -- 오늘날짜
    declare days int;  -- 활동일수 (오늘날짜 - 데뷔일자)
    select debut_date into debutDate   -- market_db의 debut_date 컬럼을 debutDate 변수에 넣기
		from market_db.member 
        where mem_id = 'APN'; 
	set curDate = current_date();   -- 현재 날짜 입력
    set days = Datediff(curDate, debutDate);    -- 일 단위
    
    if (days/365) >= 5 then
		select concat('데뷔한 지 ', days, '일이 지났습니다. 축하합니다.');  -- concat 문자 함께 입력
	else 
		select concat('데뷔한 지 ', days, '일이 지났습니다. 화이팅');
	end if;
end $$
DELIMITER ;
call ifProc3();

-- 참고. 간단히 if문 작성 가능
select if(100 > 300, '크다', '작다');


-- ----------------- 다중 분기 ---------------------

/*   먼저 조건이 만족되는 when이 처리되고 종료됨.
case 
	when 조건 then 값
    when 조건 then 값
    else 값
end
*/

select
case 100
	when 10 then '십'
    when 50 then '오십'
    when 100 then '일백'
    else '기타'
end 
as '결과';


drop procedure if exists caseProc;
DELIMITER $$
create procedure caseProc()
begin
	declare point int;
    declare credit char(1);
    set point = 88;
    case 
		when point >= 90 then set credit = 'A';
        when point >= 80 then set credit = 'B';
        when point >= 70 then set credit = 'C';
        when point >= 60 then set credit = 'D';
		else set credit = 'F';
	end case;
    select concat('취득 점수는 ', point,'점입니다'), concat('취득 학점은 ', credit, '입니다');
end $$
DELIMITER ;
call caseProc();


-- p203
-- case문 활용, 구매액 기준 회원 등급 만들기
select mem_id, sum(price*amount) "총구매액" from buy
	group by mem_id
    order by sum(price*amount) desc;
    
-- 구매테이블 회원테이블 join
select B.mem_id, M.mem_name, sum(price*amount) '총구매액'
	from buy B
		inner join member M
        on B.mem_id = M.mem_id
	group by B.mem_id
    order by sum(price*amount) desc;

--  한 번도 안 산 사람도 나와야 하기 때문에 outer join 필요
select B.mem_id, M.mem_name, sum(price*amount) '총구매액'
	from buy B
		right outer join member M
        on B.mem_id = M.mem_id
	group by B.mem_id
    order by sum(price*amount) desc;
    
select B.mem_id, M.mem_name, sum(price*amount) '총구매액',
	case
		when sum(price*amount) >= 1500 then '최우수고객'
        when sum(price*amount) >= 1000 then '우수고객'
        when sum(price*amount) >= 1 then '일반고객'
        else '유령고객'
	end '회원등급'
 	from buy B
		right outer join member M
        on B.mem_id = M.mem_id
	group by B.mem_id
    order by sum(price*amount) desc;

-- p206 while ----------------------------------------------

DELIMITER $$
create procedure whileProc()
begin
	declare i int; -- 1~100까지 증가할 변수
    declare hap int; -- 합계를 넣어주는 변수
    set i = 1;
    set hap = 0;
    while (i <= 100) do 
		set hap = hap + i;
        set i = i + 1;
    end while;
    select '1부터 100까지 합은', hap; 
end $$
DELIMITER ;
call whileProc();

-- p208 while문 응용

drop procedure if exists whileProc2;
DELIMITER $$
create procedure whileProc2()
begin
	declare i int;
    declare hap int;
    set i = 1;
    set hap = 0;
    
	myWhile:  				   -- label문
    while (i <= 100) do
		if (i % 4 = 0) then    -- 4의 배수이면, i에 1씩 더해줌
			set i = i + 1;
            iterate myWhile;   -- iterate: continue. label문을 계속 진행해라
		end if;
		set hap = hap + i;     -- 4의 배수가 아닌 i끼리 합
        if (hap > 1000) then 
			leave myWhile;     -- leave: break. 지정한 label을 떠남. 종료
		end if;
        set i = i + 1;
	end while;
    select '1부터 100까지 합(4배수 제외)은? (합이 1000 이상이면 종료)', hap;           
end $$
DELIMITER ;
call whileProc2();


-- 동적SQL ------------------------------------------------
-- MySQL: Michael Widenius의 딸 My, Structured Query Language
-- 동적쿼리: input parameter값에 따라 실행할 쿼리의 내용이 달라질 때 사용

prepare myQuery 
	from 'select * from member where mem_id = "BLK" ';
execute myQuery;
deallocate prepare myQuery;    -- 동적SQL 해제

-- --------------- 출입문 내역 만들기, prepare / execute 활용
create table gate_table (
	id int auto_increment primary key,
    entry_time datetime);

-- 3번 반복 : set, excute 3번 반복 실행
set @curDate = current_timestamp();   -- 현재 날짜 시간 출력
prepare myQuery   
	from 'insert into gate_table values(null, ?)';  
				-- insert auto_increment니까 null, ?은 변수가 들어감
execute myQuery using @curDate;     -- input param가 아닌 @을 활용한 지역변수 대입해야 함

-- table조회
select * from gate_table;
    
    
    
    
    
    
    
    
    
    
    
    

