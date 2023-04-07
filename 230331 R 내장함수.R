##### 15. Dataframe

exam <- read.csv("Data/csv_exam.csv")
exam[]   #[] 데이터프레임 전부
exam[1,]   #1행 
exam[,1]   #1열 

head(exam)
# class가 1반인 행 추출
exam[exam$class == 1, ]

# math 80점 이상인 학생 추출
exam[exam$math >=80, ]

# 1반이면서 수학점수 50점 이상
exam[exam$class ==1 & exam$math >=50, ]

# 영어점수 90점 미만이거나 과학점수 50점 미만
exam[exam$english < 90 | exam$science < 50, ]

# exam 열 추출
exam[,1]
exam[,"class"]  # class변수
exam[,c("math","english")]

# 행 변수 모두 가져오기
exam[1,3]
exam[5, 'english']
exam[exam$math >= 50, 'english']
exam[exam$math >= 50, c('english','science')]

# 계산해서 col 추가하기
exam$tot <- (exam$math + exam$english + exam$science)
head(exam)
exam$mean <- (exam$math + exam$english + exam$science)/3

#수학 50점이상이고, 영어 80점이상 되는 학생, class별 평균
aggregate(data = exam[exam$math>=50 & exam$english>=80, ], mean~class, mean)

library(dplyr)

exam %>% 
  filter(math>=50 & english>=80) %>% 
  mutate(tot = (math + english + science) / 3) %>% 
  group_by(class) %>% 
  summarise(mean = mean(tot))
exam

rm(exam1)
exam1 <- exam
exam1 %>% 
  filter(math>=50 & english>=80) %>% 
  mutate(tot = (math + english + science) / 3) %>% 
  group_by(class) %>% 
  summarise(total = sum(tot))



##### 변수타입
var1 <- c(1,2,3,1,2)   # numeric 연속변수
var2 <- factor(c(1,2,3,1,2))   # factor 범주형 변수

var1 + 2
var2 + 2    # 범주형변수는 연산이 안 됨

class(var1)   # type을 확인
class(var2)
levels(var1)
levels(var2)   # level 범주형 변수에는 있음

var3 <- c('a','b','b','c')    # 문자형
var4 <- factor(c('a','b','b','c'))   #범주형
class(var3)
class(var4)
mean(var3)
mean(var4)

# 타입변경
var2 <- as.numeric(var2)
class(var2)
mean(var2)
levels(var2)

#### 혼자서해보기 p14
mpg <- as.data.frame(ggplot2::mpg) # mpg 데이터 불러오기
mpg %>%
  mutate(tot = (cty + hwy)/2) %>% # 통합 연비 변수 생성
  filter(class == "compact" | class == "suv") %>% # compact, suv 추출
  group_by(class) %>% # class 별 분리
  summarise(mean_tot = mean(tot)) # tot 평균 산출

# dplyr 대신 R 내장 함수를 이용해 "suv"와 "compact"의 '도시 및 고속도로 통합 연비' 평균 구해보기

head(mpg)
table(mpg$class)

mean(mpg[mpg$class=="suv","cty"])
mean(mpg[mpg$class=="compact","cty"])

aggregate(data = mpg[mpg$class == c("suv","compact"),], cty~class, mean)


#### 혼자서해보기 p28
# mpg 데이터의 drv 변수는 자동차의 구동 방식
# Q1. drv 변수의 타입을 확인해 보세요.
# Q2. drv 변수를 as.factor()를 이용해 factor 타입으로 변환한 후 다시 타입을 확인해 보세요.
# Q3. drv가 어떤 범주로 구성되는지 확인해 보세요

###tch
class(mpg$drv)
mpg$drv <- as.factor(mpg$drv)
levels(mpg$drv)


##### 15-3. 데이터 구조

# Vector: 하나 또는 여러 개의 값으로 구성된 데이터 구조, 여러 타입을 섞을 수 없고, 한 가지 타입으로만 구성 가능
a <- 1
b <- 'hello'
class(a)
class(b)

# Dataframe: 행과 열로 구성된 2차원 데이터 구조, 다양한 변수 타입으로 구성 가능
x1 <- data.frame(var1 = c(1,2,3),
                 var2 = c('a','b','c'))
class(x1)

# Matrix: 행과 열로 구성된 2차원 데이터 구조, 한 가지 타입으로만 구성 가능
x2 <- matrix(c(1:12), ncol = 2)
class(x2)

# Array: 2차원 이상으로 구성된 매트릭스, 한 가지 타입으로만 구성 가능
x3 <- array(1:20, dim = c(2,5,2))
x3
class(x3)

# List: 모든 데이터 구조를 포함하는 데이터 구조, 여러 데이터 구조를 합해 하나의 리스트로 구성 가능
x4 <- list(f1 = a, f2 = x1, f3 = x2, f4 = x3)
class(x4)
View(x4)

#boxplot
x <- boxplot(mpg$cty)
x$stats
x$stats[,1]   #요약통계량 추출
x$stats[,1][3]   # 중앙값median
x$stats[,1][2]   # 1분위수
