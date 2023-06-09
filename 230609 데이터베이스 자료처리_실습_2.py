'''
<문제>

다음과 같은 <요구사항>에 맞게 Rectangle 클래스를 작성하세요.

------------------------------------------------------------------

<요구사항>
1. 멤버변수 : 가로(width) ， 세로(height)
2. 생성자 : 가로(width) ， 세로(height) 멤버 변수 초기화
3. 멤버메서드(area_calc) : 사각형의 넓이를 구하는 메소드
    사각형넓이=가로*세로
4. 멤버메소드(circum_calc) : 사각형의 둘레를 구하는 메소드
    사각형 둘레 = (가로 + 세로) * 2
5. 기타 내용은 〈실행결과〉 참조

------------------------------------------------------------------

〈실행결과〉
사각형의 넓이와 둘레를 계산합니다.
사각형의 가로 입력 : 10
사각형의 세로 입력 :5
----------------------------------------
사각형의 넓이 : 50
사각형의 둘레 : 30
----------------------------------------
'''

class Rectangle:
    width = height = 0
    print('사각형의 넓이와 둘레를 계산합니다')
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def areaCalc(self):
        print('사각형의 넓이: ', self.width * self.height)
    def circumCalc(self):
        print('사각형의 둘레: ', (self.width + self.height) * 2)

rt = Rectangle(int(input('사각형의 가로: ')), int(input('사각형의 세로: ')))
print('-'*30)
rt.areaCalc()
rt.circumCalc()

