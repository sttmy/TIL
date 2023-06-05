import os 
import sys
import pymysql

config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'passwd' : '0000',
    'database' : 'test_db',
    'port' : 3306,
    'charset' : 'utf8',
    'use_unicode' : True
}

def createTable():
    try: 
        conn = pymysql.connect(**config)
        curs = conn.cursor()
        sql = '''create table if not exists goods (
        code int primary key,
        name varchar(30) not null,
        su int default 0,
        dan int default 0
        )'''
        os.system('cls')
        curs.execute(sql)
        conn.commit()
    except Exception as e: 
        print("DB연동 실패", e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()

def register():
    try: 
        conn = pymysql.connect(**config)
        curs = conn.cursor()
        print('\n======= 상품등록 ======')
        in_code = int(input('상품코드를 입력하세요: '))
        while in_code:
            sql = f'select * from goods where code = {in_code}'
            curs.execute(sql)
            row = curs.fetchone()
            if row:
                print("이미 존재하는 코드입니다. 다른 코드를 입력하세요")
                in_code = int(input('상품코드를 입력하세요: '))
            else: 
                in_name = input('상품명 입력: ')
                in_su = int(input('수량 입력: '))
                in_dan = int(input('단가 입력: '))
                sql = f'insert into goods values ({in_code}, "{in_name}", {in_su}, {in_dan})'
                curs.execute(sql)
                conn.commit()
                print("상품 등록을 성공했습니다")
                break
    except Exception as e: 
        print("DB연동 실패", e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()

def lookupAll():
    try: 
        conn = pymysql.connect(**config)
        curs = conn.cursor()
        sql = 'select * from goods'
        curs.execute(sql)
        rows = curs.fetchall()
        print('\n======= 전체 상품 목록 조회 ======')
        print('CODE | NAME | SU | DAN')
        for row in rows:
            print('%d  |  %s  |  %d  |  %d'%row)
        print('검색 레코드 수: ', len(rows))
    except Exception as e: 
        print("DB연동 실패", e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()

class GoodsRead:
    def lookupCode(self, cd):
        try:
            conn = pymysql.connect(**config)
            curs = conn.cursor()
            in_code = int(input('\n조회할 상품코드 입력: '))
            sql = f'select * from goods where code = {in_code}'
            curs.execute(sql)
            rows = curs.fetchall()
            print(f'======= 상품 조회 ({cd}) ======')
            if rows:
                for row in rows:
                    print('코드: {}, 이름: {}, 수량: {}, 단가: {} 입니다'.format(int(row[0]), row[1], int(row[2]), int(row[3])))
            else:
                print('해당 코드에 해당하는 상품은 없습니다')
        except Exception as e: 
            print("DB연동 실패", e)
            conn.rollback()
        finally:
            curs.close()
            conn.close()

    def lookupGood(self, nm):
        try: 
            conn = pymysql.connect(**config)
            curs = conn.cursor()
            in_name = input('\n조회할 상품명 입력: ')
            sql = f'select * from goods where name like "%{in_name}%"'
            curs.execute(sql)
            rows = curs.fetchall()
            print(f'\n======= 상품 조회 ({nm}) ======')
            if rows:
                for row in rows:
                    print('코드: {}, 이름: {}, 수량: {}, 단가: {} 입니다'.format(int(row[0]), row[1], int(row[2]), int(row[3])))
            else:
                print('해당 상품은 없습니다')
        except Exception as e: 
            print("DB연동 실패", e)
            conn.rollback()
        finally:
            curs.close()
            conn.close()

def deleteGood():
    try: 
        conn = pymysql.connect(**config)
        curs = conn.cursor()
        sql = 'select * from goods'
        curs.execute(sql)
        rows = curs.fetchall()
        print('======= 전체 상품목록 ======')
        for row in rows:
            print('%d   %s  %d  %d'%row)
        print('검색 레코드 수: ', len(rows))
        in_name = input('\n삭제할 상품명 입력: ')
        sql = f'select * from goods where name = "{in_name}"'
        curs.execute(sql)
        rows = curs.fetchall()
        print('\n======= 삭제된 상품 ======')
        if len(rows)>=1:
            for row in rows:
                print('코드: {}, 이름: {}, 수량: {}, 단가: {}'.format(int(row[0]), row[1], int(row[2]), int(row[3])))
            sql = f'delete from goods where name like "%{in_name}%"'
            curs.execute(sql) 
            conn.commit()
        else:
            print('상품명이 올바르게 입력되지 않았습니다')
    except Exception as e: 
        print("DB연동 실패", e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()


if __name__ == '__main__':
    createTable()
    while True:
        os.system('cls')
        print("\n======= 상품 관리 =======")
        print("<1> 상품등록")
        print("<2> 상품목록조회")
        print("<3> 상품개별조회(코드)")
        print("<4> 상품개별조회(상품명)")
        print("<5> 상품수정")
        print("<6> 상품삭제")
        print("<9> 종료")
        sel = int(input("\n작업을 선택하세요 : "))
        if sel == 1:
            register()
            os.system('pause')
        elif sel == 2:
            lookupAll()
            os.system('pause')
        elif sel == 3:
            r1 = GoodsRead()
            r1.lookupCode('코드')
            os.system('pause')
        elif sel == 4:
            r1 = GoodsRead()
            r1.lookupGood('상품명')
            os.system('pause')
        elif sel == 5:
            print("해당 기능은 준비중입니다")
            os.system('pause')
        elif sel == 6:
            deleteGood()
            os.system('pause')
        elif sel == 9:
            print("상품관리를 종료합니다")
            os.system('pause')
            os.system('cls')
            sys.exit(0)
        else:
            print("잘못 누르셨습니다. 다시 선택해주세요")
            os.system('pause')


