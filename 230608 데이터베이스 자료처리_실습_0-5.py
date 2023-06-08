class Calc_class14:
    num1 = num2 = 0
    # str = ''
    def __init__(self, x, y, str):
        self.num1 = x
        self.num2 = y
        self.str = str
    def div(self):
        try:
            return self.num1 / self.num2
        except:
            print("0으로 나눌 수 없습니다")
    def squ(self):
        return self.num1 ** self.num2
    @classmethod
    def filter(cls, str):      
        year = str[:2]
        month = str[2:4]
        day = str[4:6]
        sex = '남성' if int(str[7:8]) in (1,3) else '여성'
        print('19{}년 {}월 {}일에 출생한 {}입니다.'.format(year, month, day, sex))


obj14 = Calc_class14(int(input("첫번째 숫자 입력: ")), int(input("두번째 숫자 입력: ")), input("주민등록번호 입력: "))
print('나눗셈: ', obj14.div())
print('제곱: ', obj14.squ())
obj14.filter(obj14.str)


# ------------------------------------------------------- year 수정 ------------
class Calc_class14_1:
    num1 = num2 = 0
    def __init__(self, x, y, str):
        self.num1 = x
        self.num2 = y
        self.str = str
    def div(self):
        try:
            return self.num1 / self.num2
        except:
            print("0으로 나눌 수 없습니다")
    def squ(self):
        return self.num1 ** self.num2
    @classmethod
    def filter(cls, str):      
        year = ('19'+str[:2]) if int(str[0]) != 0 else ('20'+str[:2])
        month = str[2:4]
        day = str[4:6]
        sex = '남성' if int(str[7]) in (1,3) else '여성'
        print('{}년 {}월 {}일에 출생한 {}입니다.'.format(year, month, day, sex))


obj14_1 = Calc_class14_1(int(input("첫번째 숫자 입력: ")), int(input("두번째 숫자 입력: ")), input("주민등록번호 입력: "))
print('나눗셈: ', obj14_1.div())
print('제곱: ', obj14_1.squ())
obj14_1.filter(obj14_1.str)
