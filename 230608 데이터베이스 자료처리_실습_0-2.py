class Clac_class13:
    # num1 = num2 = 0
    # def __init__(self):
    #     pass
        
    def member_clear(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def div(self):        
        if self.num2 != 0:
            result = self.num1 / self.num2
        else:
            result = print("Value Error")
        return result 
    def squ(self):
        result = self.num1 ** self.num2
        return result
        

obj3 = Clac_class13()
obj3.member_clear(int(input("정수를 입력하세요: ")), int(input("정수를 입력하세요: ")))
print("나눗셈: ", obj3.div())
print("제곱: ", obj3.squ())


# ------------------------------------------------------------------------------------------------

class Clac_class14:
    # num1 = num2 = 0
    # def __init__(self):
    #     pass
        
    def member_clear(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def div(self):        
        if self.num2 != 0:
            result = self.num1 / self.num2
        else:
            result = print("Value Error")
        self.display(result)

    def squ(self):
        result = self.num1 ** self.num2
        self.display(result)
        
    def display(self, result):
        print("연산 결과는 %d" %(result))


obj4 = Clac_class14()
obj4.member_clear(int(input("정수를 입력하세요: ")), int(input("정수를 입력하세요: ")))
obj4.div(), obj4.squ()