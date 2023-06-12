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
        su int default 0,
        dan int default 0
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

class ManageTable:
    def __init__(self, lookupgood):    # ----------------------------------- 질문사항
        self.lookupgood = lookupgood
        if lookupgood == '코드':
            self.lookup_sql = 'select * from goods where code ='
        else:
            self.lookup_sql = 'select * from goods where name ='
        # else: 
        #     self.lookup_sql = 'select * from goods'

    def inputValues(self):         # 메서드로 삽입했습니다 ------------------------------------ 요구사항2
        in_name = input("상품명을 입력하세요: ")
        in_su = int(input("수량을 입력하세요: "))
        in_dan = int(input("단가를 입력하세요: "))
        return in_name, in_su, in_dan
    
    def inputEach(self):           # 메서드로 삽입했습니다 ------------------------------------ 요구사항3
        if self.lookupgood == '코드':
            in_put = int(input('상품의 ' + self.lookupgood + '를 입력하세요: '))
        else:
            in_put = input('상품의 ' + self.lookupgood + '을 입력하세요: ')
        return in_put

    def registerGood(self):   # 메서드로 삽입했습니다 ------------------------------------ 요구사항4-1)
        try:
            conn = pymysql.connect(**config)
            curs = conn.cursor()
            print("\n------------ 상품등록 ------------")
            in_put = self.inputEach()       # ------------------------------------ 요구사항3
            while in_put:
                sql = self.lookup_sql + f"'{in_put}'"
                curs.execute(sql)
                row = curs.fetchone()
                if row:
                    print("이미 존재하는 코드입니다. 다른 코드를 입력하세요")
                    in_put = self.inputEach()    # ------------------------------------ 요구사항3
                else:
                    in_name, in_su, in_dan = self.inputValues()   # ------------------------------------ 요구사항2
                    sql = f'insert into goods values({in_put}, "{in_name}", {in_su}, {in_dan})'
                    curs.execute(sql)
                    conn.commit()
                    print("\n>>>>>> 실행결과: 상품 등록을 성공했습니다")
                    self.lookupGood()
                    break
        except Exception as e:
            print("DB연동 실패", e)
            conn.rollback()
        finally:
            curs.close()
            conn.close()

    def lookupGood(self):   # 메서드로 삽입했습니다 ------------------------------------ 요구사항4-2)
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

    def lookupEach(self):
        try:
            conn = pymysql.connect(**config)
            curs = conn.cursor()
            print('\n------------ 상품조회 ------------')
            if self.lookupgood == '코드':       
                in_put = self.inputEach()   # ------------------------------------ 요구사항3
                sql = self.lookup_sql + f"'{in_put}'"
            else:
                in_put = self.inputEach()   # ------------------------------------ 요구사항3
                sql = self.lookup_sql + f"'{in_put}'"
            curs.execute(sql)
            rows = curs.fetchall()

            if rows:
                print('\n------------ 상품조회 ({}) ------------'.format(self.lookupgood))
                for row in rows:
                    print('조회된 상품정보>>> 코드: {}, 이름: {}, 수량: {}, 단가: {} 입니다'.format(int(row[0]), row[1], int(row[2]), int(row[3])), '\n')
            else:
                print('해당하는 상품이 없습니다')
            self.lookupGood()   # ------------------------------------ 요구사항4-2
        except Exception as e:
            print("DB연동 실패", e)
            conn.rollback()
        finally:
            curs.close()
            conn.close()

    def updateGood(self):
        try:
            conn = pymysql.connect(**config)
            curs = conn.cursor()
            self.lookupGood()   # ------------------------------------ 요구사항4-2
            print('\n------------ 상품수정 ------------')
            in_put = self.inputEach()   # ------------------------------------ 요구사항3
            while in_put:
                sql = self.lookup_sql + f"'{in_put}'"
                curs.execute(sql)
                rows = curs.fetchall()
                if len(rows) < 1:
                    print('상품코드가 올바르게 입력되지 않았습니다. 다시 입력하세요')
                    self.lookupGood()
                    in_put = self.inputEach()   # ------------------------------------ 요구사항3
                else:
                    print("------------ 수정할 상품 조회 --------------")
                    for row in rows:
                        print(row)  
                    yesno = input("위의 상품을 수정하시겠습니까? (Y/N) ").upper()
                    if yesno == 'Y':
                        in_name, in_su, in_dan = self.inputValues()   # ------------------------------------ 요구사항2
                        sql = f'update goods set name = "{in_name}", su = {in_su}, dan = {in_dan} where code = {in_put}'
                        curs.execute(sql)
                        conn.commit()
                        print('\n>>>>>> 실행결과: 상품 수정을 성공했습니다')
                    else:
                        print('\n상품 수정을 취소하였습니다')
                    self.lookupGood()   # ------------------------------------ 요구사항4-2
                    break                   

        except Exception as e:
            print("DB연동 실패", e)
            conn.rollback()
        finally:
            curs.close()
            conn.close()

    def deleteGood(self):
        try:
            conn = pymysql.connect(**config)
            curs = conn.cursor()
            self.lookupGood()   # ------------------------------------ 요구사항4-2
            print('\n------------ 상품삭제 ------------')
            in_put = self.inputEach()   # ------------------------------------ 요구사항3
            while in_put:
                sql = self.lookup_sql + f'{in_put}'
                curs.execute(sql)
                rows = curs.fetchall()
                if len(rows) < 1:
                    print('상품코드가 올바르게 입력되지 않았습니다. 다시 입력하세요')
                    self.lookupGood()   # ------------------------------------ 요구사항4-2
                    in_put = self.inputEach()   # ------------------------------------ 요구사항3
                else:
                    print("------------ 삭제할 상품 조회 --------------")
                    for row in rows:
                        print(row)  
                    yesno = input("위의 상품을 삭제하시겠습니까? (Y/N) ").upper()
                    if yesno == 'Y':
                        sql = f'delete from goods where code = {in_put}'
                        curs.execute(sql)
                        conn.commit()
                        print('\n>>>>>> 실행결과: 상품삭제를 성공했습니다')
                    else:
                        print('\n상품 삭제를 취소하였습니다')
                    self.lookupGood()   # ------------------------------------ 요구사항4-2
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
            r = ManageTable('코드')       
            r.registerGood()
            os.system('pause')
        elif sel == 2:
            r = ManageTable('코드')        
            r.lookupGood()
            os.system('pause')
        elif sel == 3:
            r = ManageTable('코드')
            r.lookupEach()         
            os.system('pause')
        elif sel == 4:
            r = ManageTable('상품명')
            r.lookupEach()  
            os.system('pause')
        elif sel == 5:
            r = ManageTable('코드')        # 상품조회 기능을 해당메서드 내에 삽입했습니다 ------------------------------------
            r.updateGood()
            os.system('pause')
        elif sel == 6:
            r = ManageTable('코드')        # 상품조회 기능을 해당메서드 내에 삽입했습니다 ------------------------------------
            r.deleteGood()
            os.system('pause')
        elif sel == 9:
            print("상품관리를 종료합니다")
            os.system('pause')
            os.system('cls')
            sys.exit(0)
        else:
            print("잘못 누르셨습니다. 다시 선택해주세요")
            os.system('pause')




### 요구사항2: inputValues 메서드를 삽입했습니다
    
### 요구사항3: inputEach 메서드를 삽입했습니다

### 요구사항4-1: 상품등록기능을 메서드로 삽입했습니다
### 요구사항4-2: 상품조회기능을 메서드로 삽입했습니다 (객체 생성시 일일이 불러오지 않도록 함)

### 번외: 상품수정 및 삭제 시, 잘못된 코드를 입력하면 다시 입력하도록 while구문 입력했습니다

### 질문사항: 클래스 정의시, 매개변수의 인수로 '코드'와 '상품명'만 들어가도록 설계해보았는데, 
# 왜냐하면 그밖의 인수가 있을 경우, 매 메서드마다 sql구문을 다시 고려해줘야하는 등 복잡해지는 것 같아서 그랬습니다
# 뭐가 더 효율적인건지는 아직 감이 안오는데, 이같이 '코드'와 '상품명'만 인수로 허용할 경우 예상되는 문제가 있을까요?
# 그리고 다른 인수까지 허용하는 것이 더 효율적인 방법일까요?

