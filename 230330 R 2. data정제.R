##### 7장 데이터 정제
##### 7-1. 결측치

# %>%: dplyr 패키지 제공, 함수를 여러개 한꺼번에 적용시 사용, 연산자 오른쪽 함수를 왼쪽에 적용

# mutate: apply함수. DF에 파생변수 col붙여줌

df <- data.frame(sex = c("M",'F', NA, "M",'F'), score = c(5,4,3,4,NA))
View(df)
table(is.na(df))    #결측치 확인하기
table(is.na(df$sex))
table(is.na(df$score))

library(dplyr)

df %>% filter(is.na(score))   #score가 NA인 값
df %>% filter(!is.na(score))  #score가 NA가 아닌 값
df_nomiss <- df %>% filter(!is.na(score) & !is.na(sex))
df_nomiss2 <- na.omit(df)

mean(df$score)      #평균값
sum(df$score)
mean(df$score, na.rm = T)

exam <- read.csv("Data/csv_exam.csv")
View(exam)
# 행 3, 8, 15의 math컬럼에 NA값을 할당
exam[c(3,8,15), "math"] <- NA
exam %>% summarise(mean_math = mean(math))

# 결측치 제외한 평균, 합계, 중앙값 산출
exam %>% summarise(mean_math = mean(math, na.rm = T))
exam %>% summarise(sum_math = sum(math, na.rm = T))
exam %>% summarise(median_math = median(math, na.rm = T))
exam %>% summarise(mean_math = mean(math, na.rm = T),
                   sum_math = sum(math, na.rm = T),
                   median_math = median(math, na.rm = T))

##### 결측치 대체법 p14
# 평균값으로 대체
mean(exam$math, na.rm = T)
table(is.na(exam$math))
exam$math <- ifelse(is.na(exam$math), mean(exam$math, na.rm = T), exam$math)
table(is.na(exam$math))
View(exam)

###p18 혼자서해보기
# mpg 데이터 불러오기
mpg <- as.data.frame(ggplot2::mpg)
mpg[c(65,124,131,153,212), "hwy"]  <-  NA    #NA 할당

# Q1. drv(구동방식)별로 hwy(고속도로 연비) 평균이 어떻게 다른지 알아보려고 합니다. 분석을 하기 전에 우선 두 변수에 결측치가 있는지 확인해야 합니다. drv 변수와 hwy 변수에 결측치가 몇 개 있는지 알아보세요.
table(is.na(mpg$drv), is.na(mpg$hwy))

# Q2. filter()를 이용해 hwy 변수의 결측치를 제외하고, 어떤 구동방식의 hwy 평균이 높은지 알아보세요. 하나의 dplyr 구문으로 만들어야 합니다.
View(mpg)
(mean(mpg$hwy, na.rm = T))
### tch
mpg %>% filter (!is.na(hwy)) %>% 
  group_by(drv) %>% 
  summarise(mean_hwy = mean(hwy))
mpg %>%
  group_by(drv) %>% 
  summarise(mean_hwy = mean(hwy, na.rm = T))
table(mpg$drv)

##### 7-2. 이상치 p23
##### 존재할 수 없는 값 처리
outlier <- data.frame(sex = c(1,2,1,3,2,1), score = c(5,4,3,4,2,6))
table(outlier$sex)
table(outlier$score)

# sex3이면 NA할당
outlier$sex <- ifelse(outlier$sex == 3, NA, outlier$sex)
table(outlier$sex)
outlier

# score>5이면 NA할당
outlier$score <- ifelse(outlier$score > 5, NA, outlier$score)
table(outlier$score)
outlier

# 결측치 제외하고 평균값 구하기
outlier %>% 
  filter(!is.na(sex) & !is.na(score)) %>% 
  group_by(sex) %>% 
  summarise(mean_score = mean(score))

outlier

##### 극단값 제거 
####### 상하위 0.3% 또는 상자그림 1.5IQR 벗어나면 극단치
mpg <- as.data.frame(ggplot2::mpg)
View(mpg)
boxplot(mpg$hwy)
boxplot(mpg$hwy)$stats

#12~37 벗어나면 NA를 할당
mpg$hwy <- ifelse(mpg$hwy < 12 | mpg$hwy >37, NA, mpg$hwy)
#결측치 확인
table(is.na(mpg$hwy))
#결측치 제외하고 구동방식별 평균도출
mpg %>% 
  group_by(drv) %>% 
  summarise(mean_hwy = mean(hwy, na.rm = T))

###혼자서해보기 p37
mpg <- as.data.frame(ggplot2::mpg) # mpg 데이터 불러오기
mpg[c(10, 14, 58, 93), "drv"] <- "k" # drv 이상치 할당
mpg[c(29, 43, 129, 203), "cty"] <- c(3, 4, 39, 42) # cty 이상치 할당

# Q1. drv 에 이상치가 있는지 확인하세요. 이상치를 결측 처리한 다음 이상치가 사라졌는지 확인하세요. 결측처리 할 때는 %in% 기호를 활용하세요.
table(mpg$drv)
mpg$drv <- ifelse(mpg$drv =="k", NA, mpg$drv)
table(mpg$drv)
###tch
mpg$drv <- ifelse(mpg$drv %in% c("4","f","r"), mpg$drv, NA)   ## %in% 여러개 표시

# Q2. 상자 그림을 이용해서 cty 에 이상치가 있는지 확인하세요. 상자 그림의 통계치를 이용해 정상 범위를 벗어난 값을 결측 처리한 후 다시 상자 그림을 만들어 이상치가 사라졌는지 확인하세요.
table(mpg$cty)
boxplot(mpg$cty)
boxplot(mpg$cty)$stat
mpg$cty <- ifelse(mpg$cty<9 | mpg$cty>26, NA, mpg$cty)
boxplot(mpg$cty)

# Q3. 두 변수의 이상치를 결측처리 했으니 이제 분석할 차례입니다. 이상치를 제외한 다음 drv 별로 cty평균이 어떻게 다른지 알아보세요. 하나의 dplyr 구문으로 만들어야 합니다
mpg %>% 
  filter(!is.na(drv) & !is.na(cty)) %>% 
  group_by(drv) %>% 
  summarise(mean_cty = mean(cty))

mpg %>% 
  group_by(drv, na.rm = T) %>% 
  summarise(mean_cty = mean(cty, na.rm = T))
