'''
클래스를 4개 만들고 메소드 오버라이드를 구현하세요.

------------------------------------------------------------------

<코딩조건>
- 168~ 169 페이지 소스를 기본으로하여 아래의 내용을 추가하세요.
- 해당 소스코드에 Alba 라는 클래스를 추가 하세요.
- Alba 클래스의 모든 내용은 Temporary클래스와 비슷한데 추가내용이 있습니다.
- Alba 클래스의 선언부에 부모클래스의 pay_calc메소드를  오버라이드 하세요.
- Alba 클래스의 객체를 만들 때, 급여계산에 사용하는
   시간당 급여는 20,000원으로 정하고 근무시간은 160시간으로 정하세요.
- Alba 클래스의 pay_calc메소드에 
  20일 만근(160시간 이상근무) 했을 때는 8시간 근무한 금액을 수당으로 계산하여 더하는
  로직을 추가하세요.

------------------------------------------------------------------
<실행결과>
총 수령액 :  3,200,000 원
총 수령액 :  1,200,000 원
총 수령액 :  3,360,000 원 
'''

# 부모클래스
class Employee:
    name = None
    pay = 0
    
    def __init__(self, name):
        self.name = name
    def pay(self):
        pass

# 자식클래스: 정규직
class Permanent(Employee):
    def __init__(self, name):
        super().__init__(name)
    def pay(self, base, bonus):
        self.pay = base + bonus
        print(self.name, "님의 총 수령액: ", format(self.pay, ',d'),'원')
        # format(self.pay, '4,d')  : 최소한 4칸의 자리공간을 생성

# 자식클래스: 임시직
class Temporary(Employee):
    def __init__(self, name):
        super().__init__(name)
    def pay(self, tpay, time):
        self.pay = tpay * time
        print(self.name, "님의 총 수령액: ", format(self.pay, ',d'),'원')

# Alba 클래스 추가
class Alba(Temporary):
    def __init__(self, name):
        super().__init__(name)
    def pay(self, tpay, time):
        self.pay = tpay * time if time < 160 else tpay * (time + 8) 
        print(self.name, "님의 총 수령액: ", format(self.pay, ',d'),'원')


# 객체 생성
p = Permanent('이순신')
t = Temporary('홍길동')
a = Alba('김영희')

# 결과 도출
p.pay(3000000, 200000)
t.pay(15000, 80)
a.pay(20000, 160)