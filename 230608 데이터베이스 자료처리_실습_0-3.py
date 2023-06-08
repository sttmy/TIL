class Clac_class13:
    num1 = num2 = 0

    def member_clear(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def div(self):        
        if self.num2 != 0:
            result = self.num1 / self.num2
        else:
            result = print("나눗셈 연산은 0으로 나누기가 불가능합니다. 다시 입력하세요")
        return result 
    def squ(self):
        result = self.num1 ** self.num2
        return result

obj3 = Clac_class13()
obj3.member_clear(int(input("정수를 입력하세요: ")), int(input("정수를 입력하세요: ")))
print("나눗셈: ", obj3.div())
print("제곱: ", obj3.squ())



# ----------------------------------
class Clac_class13_1:
    num1 = num2 = 0

    def member_clear(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    def div(self):        
        try: 
            return self.num1 / self.num2
        except:
            print("나눗셈 연산은 0으로 나누기가 불가능합니다. 다시 입력하세요")
    def squ(self):
        result = self.num1 ** self.num2
        return result

obj31 = Clac_class13_1()
obj31.member_clear(int(input("1번째 정수를 입력하세요: ")), int(input("2번째 정수를 입력하세요: ")))
print("나눗셈: ", obj31.div())
print("제곱: ", obj31.squ())