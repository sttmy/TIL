#!/usr/bin/env python
# coding: utf-8

# ### 6.3.2 상속 INHERITANCE ★중요
# 
# - 클래스 간 계층적 관계 구성하여, 높은 수준의 코드 재사용성과 다형성의 문법적 토대 마련
# - 부모클래스는 자식클래스에서 공통으로 사용할 수 있는 멤버를 선언하여 클래스를 정의함
# - 예) 부모클래스: 사원( 사원명, 부서명, 급여 있음 ) / 자식클래스: 정규직 / 임시직
# 
# #### 클래스의 상속
# - 자식클래스는 부모의 멤버(멤버변수, 메서드)를 상속받음
# - 자식클래스가 부모클래스를 지정하면 상속관계가 맺어짐
# - 생성자는 상속 대상이 아님
# 
# #### 클래스 다이어그램

# In[1]:


from IPython.display import Image

Image('Data/230609/classDiagram.png')


# In[37]:


# 부모클래스
class Super:
    # 생성자: 동적 멤버 생성
    def __init__(self, name, age):
        self.name = name     # 동적 멤버
        self.age = age
        
    # 메서드
    def display(self):
        print('name: %s, age: %d'%(self.name, self.age))


# In[39]:


sup = Super('부모',55)
sup.display()     # 부모 메서드 호출(부모멤버 출력)


# In[40]:


# 자식클래스  
class Sub(Super):   # 클래스 상속  Sub(부모클래스명)
    gender = None    # 자식 멤버
    
    # 생성자
    def __init__(self, name, age, gender):
        self.name = name     # 부모클래스의 동적 멤버를 그대로 갖다 씀
        self.age = age
        self.gender = gender    # 새로운 동적 멤버변수 지정
        
    # 메서드 확장 (매서드 재정의, Method Override)
    ##### 부모클래스의 메서드를 가져와서 재정의함
    def display(self):
        print('name: %s, age: %d, gender: %s'%(self.name, self.age, self.gender))


# In[41]:


sub = Sub('자식', 25, '여자')
sub


# In[42]:


sub.display()   # 자식 메서드 호출(자식멤버 출력)


# #### SUPER 클래스
# - 상속할 때, 부모클래스의 생성자는 상속대상에서 제외됨
# - 필요한경우, 부모클래스 생성자를 강제로 호출
#     - super().__ init __ ()
#         - 부모클래스의 멤버변수를 별도로 지정해주지 않아도 사용 가능

# In[2]:


# 부모클래스 
class Parent: 
    # 생성자: 객체+ 초기화
    def __init__(self, name, job):
        self.name = name
        self.job = job
    # 멤버함수
    def display(self):
        print('name: {}, job: {}'.format(self.name, self.job))


# In[3]:


# 부모클래스 객체 생성
p = Parent('홍길동','회사원')
p.display()


# In[10]:


# 자식클래스
class Childeren(Parent):
    gender = None   # 자식클래스 멤버변수 추가
    
    # 생성자
    def __init__(self, name, job, gender):
        # 부모클래스 생성자호출
        super().__init__(name, job)   # name, job 초기화
#         self.name = name            # 이 두 라인을 대신 실행해도 됨
#         self.job = job
        self.gender = gender          # 자식클래스 멤버변수 gender 초기화
    
    # 멤버함수
    def display(self):   # 함수 재정의
        print('name: {}, job: {}, gender: {}'.format(self.name, self.job, self.gender))


# In[11]:


chil = Childeren('홍홍동','장군','남자')
chil


# In[12]:


chil.display()


# In[13]:


chil.name, chil.job, chil.gender


# ### 6.3.3 메서드 재정의
# - 예) 부모클래스: 사원(급여계산), 자식클래스: 정규직(급여=기본급+상여금), 임시직(급여=시급*근무시간)

# #### Method override 메서드 재정의
# - 부모에게 상속받은 메서드를 자식클래스에서 수정하거나 확장해서 사용
# - 메서드 이름은 부모클래스에서와 같으나 내용이 다름
# - 부모클래스의 메서드의 동일 내용을 가져오려면, super().매서드명()
# 
# vs Overload : 상속과 무관: 기존에 있던 메서드와 이름은 같지만, 부가적인 내용을 추가시킴. 하나의 클래스 내에서 사용 (파이썬에서는 사용하지 않음)
# 
#             Overriding         vs       Overloading
#         Parent - Children class        In the Same class
#         Same method name               Same method name                 
#         Same parameters                Different parameters
#         Compile-time polymorphism      Runtime polymorphism

# In[62]:


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


# In[57]:


Image('Data/230609/pay.png')


# In[58]:


# 객체 생성
p = Permanent('이순신')
p


# In[59]:


p.pay(3000000, 200000)


# In[60]:


t = Temporary('홍길동')
t


# In[61]:


t.pay(15000, 80)


# ### [실습0-5]
# 
# - 특정메서드의 오버라이딩을 위해 부모클래스는 pass로 설정

# ### 6.3.4 다형성: 여러가지 형태를 가질 수 있는 능력
# 
# - 다형성: 하나의 참조변수로 여러 타입의 객체를 참조할 수 있는 것
# <br> 예) 파이썬에서 + 기호: 산술연산 덧셈, 문자열연산 결합기능 2가지 다 갖고 있음
# <br> 클래스 예) 
#     - 부모클래스: 비행(날다)를, 
#     - 자식클래스: 비행기(날다), 새(날다), 종이비행기(날다) 로 재정의
# <br>
# 
# - 참조변수끼리 할당이 이루어져야 다형성이 구현됨
# <br> 부모객체 참조변수 = 자식객체 참조변수

# In[99]:


# 부모클래스
class Flight:
    # 부모 원형함수
    def fly(self):
        print("날다, fly 원형 메서드")


# In[100]:


# 자식클래스(비행기)
class Airplane(Flight):
    
    # 함수재정의
    def fly(self):
        print("비행기가 날다")

# 자식클래스(새)
class Bird(Flight):
    
    # 함수재정의
    def fly(self):
        print("새가 날다")

# 자식클래스(종이비행기)
class PaperAirplane(Flight):
    
    # 함수재정의
    def fly(self):
        print("종이비행기가 날다")


# In[101]:


## 객체 생성
# 부모객체 = 자식객체(자식1, 자식2)

flight = Flight()
air = Airplane()
bird = Bird()
paper = PaperAirplane()
print(flight)               # 메모리주소 출력
print(air)
print(bird)
print(paper)


# In[102]:


id(air), id(flight)


# In[103]:


flight.fly(), air.fly()


# In[104]:


# 부모클래스
class Flight:
    # 부모 원형함수
    def fly(self):
        print("날다, fly 원형 메서드")
    def landing(self):
        print("착륙")      


# In[105]:


flight = Flight()
air = Airplane()


# In[106]:


# 다형성
flight.fly(), flight.landing()


# In[107]:


air.fly(), air.landing()


# In[108]:


air = flight            # air를 flight에 할당. 
air.fly(), air.landing()


# In[69]:


flight = bird
flight.fly()


# In[70]:


flight = paper
flight.fly()


# 쉬운파이썬
# https://wikidocs.net/192021
# 
# #### 다형성
# - 같은 형태의 코드가 서로 다른 동작을 함
# - 코드의 양을 줄이고, 여러 객체 타입을 하나의 타입으로 관리가 가능하게 만들어, 코드의 유지보수에 좋음
# - 상속관계 내의 다른 클래스들의 인스턴스들이 같은 멤버 함수 호출에 대해 각각 다르게 반응 하도록 하는 기능
