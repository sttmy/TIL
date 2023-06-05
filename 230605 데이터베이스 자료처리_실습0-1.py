import pymysql
import os
print(pymysql.version_info)

config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'passwd' : '0000',
    'database' : 'work',
    'port' : 3306,
    'charset' : 'utf8',
    'use_unicode' : True
}

try:
    conn = pymysql.connect(**config)
    curs = conn.cursor()

    # (1) table 생성
    sql = '''create table if not exists goods(
    code int primary key,
    name varchar(30) not null,
    su int default 0,
    dan int default 0
    )'''
    curs.execute(sql)
    conn.commit()

    # # (2) 레코드 추가
    code = int(input('코드 입력: '))
    name = input('상품명 입력: ')
    su = int(input('수량 입력: '))
    dan = int(input('단가 입력: '))

    sql = f'insert into goods values ({code}, "{name}", {su}, {dan})'
    curs.execute(sql)
    conn.commit()

    # (3) 전체목록 보기
    sql = 'select * from goods'
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows: 
        print('%d   %s  %d  %d'%row)
    print('검색 레코드 수: ', len(rows))

    # (4) 상품명 조회
    in_name = input('\n조회할 상품명 입력: ')
    sql = f'select * from goods where name like "%{in_name}%"'
    curs.execute(sql)
    rows = curs.fetchall()
    if rows:
        for row in rows:
            print(row[0], row[1], row[2], row[3])
    else:
        print('해당상품 없음')

    # # (5) 상품 삭제
    # in_code = int(input('\n삭제할 상품코드 입력: '))
    # sql = f'delete from tgoods where code = {in_code}'
    # curs.execute(sql)
    # conn.commit()
        
except Exception as e:
    print("DB연동 오류 : ", e)
    conn.rollback()

finally:
    curs.close()
    conn.close()
