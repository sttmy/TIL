class Account:
    # 은닉 멤버변수
    __balance = 0  # 잔액
    __accName = None  # 예금주
    __accNo = None  # 계좌번호
    
    # 생성자: 멤버변수 초기화
    def __init__(self, bal, name, no):
        self.__balance = bal
        self.__accName = name
        self.__accNo = no
    
    # 계좌정보 확인: getter
    def getBalance(self):
        return self.__balance, self.__accName, self.__accNo
    
    # 입금하기: setter
    def deposit(self, money):    # 지정자메서드
        if money < 0:
            print('금액 확인')
            return #  종료
        self.__balance += money
    
    # 출금하기: setter            # 지정자메서드
    def withdraw(self, money):
        if self.balance < money:
            print("잔액 부족")
            return
        self.__balance -= money