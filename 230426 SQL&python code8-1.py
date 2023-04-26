## 파이썬에서 데이터 입력 : 6단계
# 1) mysql 연결하기: pymysql.connect(연결옵션)
# 2) 커서생성: 커서이름 = 연결자.cursor()
# 3) 테이블 만들기: 커서이름.execute("create table 문장")
# 4) 데이터 입력하기: 커서이름.execute("insert 문장"  --- 반복
# 5) 입력한 데이터 저장: 연결자.commit()
# 6) mysql 연결 종료: 연결자.close()


import pymysql
conn, cur = None, None
data1, data2, data3, data4 = "", "", "", ""
sql = ''
# 연결자: host = 서버IP주소, user= 사용자, password=, db=, charset=
conn = pymysql.connect(host='127.0.0.1', user='root', password='0000',
                db='solodb', charset='utf8')
# 커서: DB에 SQL문을 실행하거나 실행된 결과를 돌려받는 통로로 생각
cur = conn.cursor()

# cur.execute(sql문 사용)
while True:
    data1 = input("사용자 ID == > ")
    if data1 =="":
        break
    data2 = input("사용자 이름 == > ")
    data3 = input("이메일 == > ")
    data4 = input("출생연도 == > ")
    sql = "insert into userTable values('"+ data1 + "', '"+ data2 +"','"+ data3 +"',"+ data4 +")"
    cur.execute(sql)

# commit: 임시로 저장된 상태를 확실하게 저장
conn.commit()

# 데이터베이스를 닫아줌
conn.close



