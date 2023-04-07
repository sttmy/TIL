a <- 1
b <- 2
c <- 3
d <- 3.5
a + b + c
4/b
5*d

var1 <- c(1,2,5,7,8)
var1
var2 <- c(1:5)
var3 <- seq(1,5)
var4 <- seq(1, 10, 2)
var5 <- seq(1, 10, by=3)
var1 + 2    # 벡터지만, array처럼 2씩 더해줌
var1 + var2

str1 <- "a"
str2 <- "hello world"
str3 <- c('a','b','c')
str4 <- c("Hello", "World")

x <- c(1,2,3)
mean(x)
max(x)
min(x)
str4 <- c("Hello", "World")
paste(str4, collapse = ',') # ,형태로 합치기
paste(str4, collapse = ' ') # 공백, 하나의 형태로 합치기

x_mean = mean(x)

############################################
install.packages("ggplot2")  # 그림그리기
library(ggplot2)

x <- c("a","a","b","c")

# 빈도그래프
qplot(x)

# mpg data  (내장되어 있음)
# x축에 hwy변수 지정해서 그래프 생성  hwy 고속도로 연비 cty 도심연비

qplot(data = mpg, x = hwy)
qplot(data = mpg, x = cty)

# x축 drv, y축 hwy
qplot(data = mpg, x = drv, y = hwy)
qplot(data = mpg, x = drv, y = hwy, geom = "line")
qplot(data = mpg, x = drv, y = hwy, geom = "boxplot")

qplot(data = mpg, x = drv, y = hwy, geom = "boxplot", color = drv)

?qplot

########################################################

#연습1
25+99
456-123
2*(3+4)
(3+5*6)/7
(7-4)*3
2^10 + 3^5
1256%%7
184%%5
1976/24
16*25 + 186* 5 - 67*22

#연습2-1  반지름 10, 15, 20 원의 면적
x <- 10
area <- x^2*3.14
area
x <- 15
area <- x^2*3.14
area
x <- 20
area <- x^2*3.14
area

#연습2-2. y=2x^2+5x+10 , x가 6,8,10일때 값

x <- 6
y <- 2*x^2 + 5*x + 10
y
x <- 8
y <- 2*x^2 + 5*x + 10
y
x <- 10
y <- 2*x^2 + 5*x + 10
y

x <- c(6,8,10)
y <- 2*x^2 + 5*x + 10
y

#연습3. 101~200의 값으로 구성된 벡터 d생성
d <- c(101:200)
#10번째값
d[10]
#뒤에서 10개 잘라내기
length(d)
d[91:100]
tail(d, 10)
#짝수출력
d[seq(2,100,2)]   
d[d%%2 == 0]
#앞에서 20개 값 잘라서 d.20에저장
d.20 <- d[c(1:10)]
d.20[-5]
d.20[-c(5,7,9)]

#연습4. d1, d2
d1 <- 1:50
d2 <- 51:100
d1+d2; d2-d1; d1*d2; d2/d1
sum(d1); sum(d2)
max(d2); min(d2)
mean(d1); mean(d2); mean(d1) - mean(d2)
#큰수에서 작은수 순으로 정렬
sort(d1, T)
#d1 과 d2 에서 큰수 순으로 각각 10개씩을 추출하여 d3 에 저장하시오 
d3 <- c(sort(d1, T)[1:10], sort(d2, T)[1:10])

#연습5 
v1 <- 51:90
v1[v1 < 60]
length(v1[v1 < 70])
sum(v1[v1>65])
v1[60<v1 & v1<73]
v1[65>=v1 | v1>80]
v1[v1 %% 7 == 3]
sum(v1[v1 %% 2 == 0])
v1[(v1 %% 2 == 1) | v1 >80]
v1[(v1 %% 3 == 0) & (v1 %% 5 == 0)]


####################################혼자서해보기(p77)
#1 시험점수
score <- c(80, 60, 70, 50, 90)
m <- mean(score)
m