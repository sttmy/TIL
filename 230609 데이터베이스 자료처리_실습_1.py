'''
예제-1 코드를 코딩조건에 맞게 수정하세요.

------------------------------------------------------------------

<코딩조건>
Ufo라는 이름의 클래스를 한 개 더 만드세요.
Ufo클래스는 개념적으로 fly클래스, Airplane클래스, Bird 클래스의 형제 클래스입니다.
Ufo클래스는 부모와 동일한 이름의 메소드를 오버라이드 합니다.
메소드이 내용은 'UFO가 날아다닙니다.' 를 프린트 합니다. 
Ufo클래스로부터 객체를 한 개 만들고 이를 참조변수에 할당하세요.
이 때 참조변수의 이름은 u 로 합니다.
참조변수 u를 프린트 해보세요.
flight = Flight()
위와 같이 만들어진 참조변수 flight도 프린트 해보세요.

u 참조변수를 부모이름 참조변수에 할당하고,
부모이름참조변수.fly()라고 호출해 보세요. 
-----------------------------------------------------------------

<실행결과>

날다, fly 원형 메서드
비행기가 날다.
새가 날다.
종이 비행기가 날다.
==== filght에 u 를 할당하기 이전 ====
<__main__.Ufo object at 0x000002193697A910>
<__main__.PaperAirplane object at 0x000002193697AD60>
UFO가 날아다닙니다.
==== filght에 u 를 할당한 이후 ====
<__main__.Ufo object at 0x000002193697A910>
<__main__.Ufo object at 0x000002193697A910>

'''

# 예제-01 : 다형성(polymorphism)
class Flight: # (1) 부모 클래스
    def fly(self): # 부모 원형 메소드 
        print('날다, fly 원형 메서드')
class Airplane(Flight) : # (2) 자식 클래스 : 비행기
    def fly(self): #  메소드 재정의
        print('비행기가 날다.')
class Bird(Flight) : # (2) 자식 클래스 : 새
    def fly(self): #  메소드 재정의
        print('새가 날다.')
class PaperAirplane(Flight) : # (2) 자식 클래스 : 종이비행기
    def fly(self): #  메소드 재정의
        print('종이 비행기가 날다.')
class Ufo(Flight) : 
    def fly(self): # 메서드 재정의
        print('UFO가 날아다닙니다')

# (3) 객체 생성
# 부모 객체 = 자식 객체(자식1, 자식2)
flight = Flight()   # 부모 클래스로부터 객체를 생성하고 그 주소를 flight참조변수에 할당함
air = Airplane()    # 자식1 클래스 객체
bird = Bird()       # 자식2 클래스 객체
paper = PaperAirplane() # 자식3 클래스 객체
u = Ufo() # 자식4 클랙스 객체

# (4) 다형성
flight.fly() # '날다, fly 원형 메서드' 라고 출력됨 

flight = air # 23라인에서 Airplane클래스로부터 만들어진 
             # 객체의 주소를 저장한 것이 air 참조변수이다. 
             # air참조변수에 저장된 객체의 주소값을 flight참조변수에
             # 할당한다는 개념이다.
flight.fly() # '비행기가 날다.' 라고 출력됨 

flight = bird
flight.fly() # '새가 날다.' 라고 출력됨 

flight = paper
flight.fly() # '종이 비행기가 날다.' 라고 출력됨 


# 추가 출력결과
print('\n==== filght에 u 를 할당하기 이전 ====')
print(u)
print(flight)

flight = u
print('\n==== filght에 u 를 할당한 이후 ====')
flight.fly()
print(u)
print(flight)