class Clac_class11:
    num1 = num2 = 0
    
    def __init__(self, num1, num2):
        self.x = num1
        self.y = num2
        num1 = int(input("정수를 입력하세요: "))
        num2 = int(input("정수를 입력하세요: "))
        
    def div(self):        
        if self.num2 != 0:
            result = self.num1 / self.num2
        else:
            result = print("Value Error")
        return result 
    def squ(self):
        result = self.num1 ** self.num2
        return result


# num1 = int(input("정수를 입력하세요: "))
# num2 = int(input("정수를 입력하세요: "))

obj = Clac_class11()
obj