import os
import sys
import pymysql

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd' : '0000',
    'database' : 'test_db',
    'port': 3306,
    'charset': 'utf8',
    'use_unicode': True
}

def createTable():
    try:
        conn = pymysql.connect(**config)
        curs = conn.cursor()
        sql = """
        create table if not exists goods(
        code int primary key,
        name varchar(30) not null,
        num int default 0,
        unit_price int default 0
        )
        """
        os.system('cls')
        curs.execute(sql)
        conn.commit()
    except Exception as e:
        print("DB연동 실패", e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()

def registerGood():
    try:
        conn = pymysql.connect(**config)
        curs = conn.cursor()
        print("\n------------ 상품등록 ------------")
        in_code = int(input("상품코드를 입력하세요: "))
        while in_code:
            sql = f'select * from goods where code = {in_code}'
            curs.execute(sql)
            row = curs.fetchone()
            if row:
                print("이미 존재하는 코드입니다. 다른 코드를 입력하세요")
                in_code = int(input("상품코드를 입력하세요: "))
            else:
                in_name = input("상품명을 입력하세요: ")
                in_num = int(input("수량을 입력하세요: "))
                in_unit_price = int(input("단가를 입력하세요: "))
                sql = f'insert into goods values({in_code}, "{in_name}", {in_num}, {in_unit_price})'
                curs.execute(sql)
                conn.commit()
                print("상품 등록을 성공했습니다")
                sql = f'select * from goods'
                curs.execute(sql)
                rows = curs.fetchall()
                print("\n============ 상품목록조회 ============")
                print("code | name | number | unit_price")
                for row in rows:
                    print('%d | %s | %d | %d'%row)
                print('\n검색된 레코드 수: ', len(rows), '\n')
                break
    except Exception as e:
        print("DB연동 실패", e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()

def lookupGood():
    try:
        conn = pymysql.connect(**config)
        curs = conn.cursor()
        sql = f'select * from goods'
        curs.execute(sql)
        rows = curs.fetchall()
        print("\n============ 상품목록조회 ============")
        print("code  | name  | number    | unit_price")
        for row in rows:
            print('%d    | %s    | %d    | %d'%row)
        print('\n검색된 레코드 수: ', len(rows),'\n')
    except Exception as e:
        print("DB연동 실패", e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()

class LookupEach:
    def __init__(self, lookupgood):
        self.lookupgood = lookupgood
        if lookupgood == '코드':
            self.lookup_sql = 'select * from goods where code ='
        else:
            self.lookup_sql = 'select * from goods where name ='
    def each(self):
        try:
            conn = pymysql.connect(**config)
            curs = conn.cursor()
            print('\n------------ 상품개별조회 ------------')
            if self.lookupgood == '코드':
                in_put = int(input('\n조회할 ' + self.lookupgood + '를 입력하세요: '))
            else:
                in_put = input('\n조회할 ' + self.lookupgood + '을 입력하세요: ')
            sql = self.lookup_sql + f"'{in_put}'"
            curs.execute(sql)
            rows = curs.fetchall()
            if rows:
                print('\n------------ 상품조회 ({}) ------------'.format(self.lookupgood))
                for row in rows:
                    print('조회된 상품정보>>> 코드: {}, 이름: {}, 수량: {}, 단가: {} 입니다'.format(int(row[0]), row[1], int(row[2]), int(row[3])), '\n')
            else:
                print('해당하는 상품이 없습니다')
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
        lookupGood()
        in_code = int(input('삭제할 상품코드 입력: '))
        while in_code:
            sql = f'select * from goods where code = {in_code}'
            curs.execute(sql)
            rows = curs.fetchall()
            if len(rows) < 1:
                print('상품코드가 올바르게 입력되지 않았습니다. 다시 입력하세요')
                in_code = input('\n삭제할 상품코드 입력: ')
            else:
                sql = f'delete from goods where code = {in_code}'
                curs.execute(sql)
                conn.commit()
                print('\n------------ 삭제된 상품 ------------')
                for row in rows:
                    print('삭제된 상품정보>>> 코드: {}, 이름: {}, 수량: {}, 단가: {} 입니다'.format(int(row[0]), row[1], int(row[2]), int(row[3])))
                print('상품삭제를 성공했습니다')
                lookupGood()
                break                
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
        print("\n==============[ 상품관리 ]==============")
        print("<1> 상품등록")
        print("<2> 상품목록조회")
        print("<3> 상품개별조회(코드)")
        print("<4> 상품개별조회(상품명)")
        print("<5> 상품수정")
        print("<6> 상품삭제")
        print("<9> 종료")
        sel = int(input("\n원하시는 작업을 선택하세요: "))
        if sel == 1:
            registerGood()
            os.system('pause')
        elif sel == 2:
            lookupGood()
            os.system('pause')
        elif sel == 3:
            r1 = LookupEach('코드')
            r1.each()         
            os.system('pause')
        elif sel == 4:
            r1 = LookupEach('상품명')
            r1.each()
            os.system('pause')
        elif sel == 5:
            print("\n해당 기능은 준비중입니다")
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





