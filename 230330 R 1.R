## PPT 6장 7. 데이터합치기  p74
install.packages("dplyr")
library(dplyr)

##### 가로로 합치기: left_join p75
# left_join(exam, name, by = "class")
# by 변수명 앞에 쌍따옴표 입력
test1 <- data.frame(id = c(1,2,3,4,5), midterm = c(60,70,80,90,85))
test2 <- data.frame(id = c(1,2,3,4,5), finterm = c(70,83,65,95,80))
total <- left_join(test1, test2, by="id")

# 담임선생님 명단
name <- data.frame(class = c(1,2,3,4,5), teacher = c('Kim','Lee','Park','Choi','Jung'))

exam <- read.csv("Data/csv_exam.csv")
head(exam)
exam_new <- left_join(exam, name, by = "class")


##### 세로로 합치기: bind_rows p80
group_a <- data.frame(id = c(1,2,3,4,5), test = c(60,70,80,90,85))
group_b <- data.frame(id = c(6,7,8,9,10), test = c(63,73,83,93,89))
View(group_a)
group_all <- bind_rows(group_a, group_b)
View(group_all)

group_c <- data.frame(id = c(6,7,8,9,10), test1 = c(63,73,83,93,89))
group_acall <- bind_rows(group_a, group_c)
View(group_acall)
# colname이 다르면 NA값, 제대로 합쳐지지 않음


##### p83 Quiz
fuel <- data.frame(fl = c("c", "d", "e", "p", "r"),
                    price_fl = c(2.35, 2.38, 2.11, 2.76, 2.22), stringsAsFactors = F)
fuel

mpg <- as.data.frame(ggplot2::mpg)
View(mpg)


#Q1. mpg 데이터에는 연료 종류를 나타낸 fl 변수는 있지만 연료 가격을 나타낸 변수는 없습니다. 위에서 만든 fuel 데이터를 이용해서 mpg 데이터에 price_fl(연료 가격) 변수를 추가

mpg_update <- left_join(mpg, fuel, by ="fl")
View(mpg_update)

# Q2. 연료 가격 변수가 잘 추가됐는지 확인하기 위해서 model, fl, price_fl 변수를 추출해 앞부분 5행을 출력해 보세요

mpg_update %>%  
  select(model, fl, price_fl) %>% 
  head(5)

##### 정리하기
# 조건에 맞는 데이터만 추출
exam %>% filter(eng >=80)

# 여러조건 동시 충족
exam %>% filter(eng >=80 & class == 1)

# 필요 변수만 추출
exam %>% select(class, math, eng)

# 일부만 출력
exam %>% 
  select(id, math) %>% 
  head(5)

# 순서대로 정렬
exam %>% arrange(math)          #오름차순
exam %>% arrange(desc(math))    #내림차순
exam %>% arrange(class, math)   #여러변수 기준 오름차순

# 파생변수 추가
exam %>% mutate(total = math + eng + science)

# 여러 파생변수 추가
exam %>% 
  mutate(total = math + eng + science, 
         mean = (math + eng + science)/3 )

# mutate()에 ifelse() 적용
exam %>% mutate(test = ifelse(science >=60, "P","F"))

# 추가한 변수를 dplyr 코드에 바로 활용  ########
exam %>%
  mutate(total = math + english + science) %>%
  arrange(total)
# 집단별로 요약하기
exam %>%
  group_by(class) %>%
  summarise(mean_math = mean(math))
# 각 집단별로 다시 집단 나누기
mpg %>%
  group_by(manufacturer, drv) %>%
  summarise(mean_cty = mean(cty))


##### 분석도전 p91
# 참고: https://ggplot2.tidyverse.org/reference/midwest.html#details

midwest <- as.data.frame(ggplot2::midwest)
View(midwest)
dim(midwest)

#Q1. popadults 는 해당 지역의 성인 인구, poptotal 은 전체 인구를 나타냅니다. midwest 데이터에 '전체 인구 대비 미성년 인구 백분율' 변수를 추가하세요

per <- data.frame((midwest$poptotal - midwest$popadults) / midwest$poptotal * 100)
View(per)

###tch
midwest <- midwest %>% 
  mutate(ratio_child = (poptotal-popadults)/poptotal*100)
View(midwest)

#Q2. 미성년 인구 백분율이 가장 높은 상위 5개 county(지역)의 미성년 인구 백분율

###tch
midwest %>% arrange(desc(ratio_child)) %>% 
  select(county, ratio_child) %>% 
  head(5)

#Q3. 분류표에 따라 미성년 비율 등급 추가, 각 등급에 몇 개의 지역이 있는지
# large 40%이상, middle 30~40%, small 30%미만
###tch
midwest <- midwest %>% 
  mutate(grade = ifelse (ratio_child >=40, "Large", ifelse(ratio_child >= 30, "Middle", "Small")))
View(midwest)
table(midwest$grade)

#Q4.  popasian은 해당 지역의 아시아인 인구를 나타냅니다. '전체 인구 대비 아시아인 인구 백분율'  변수를 추가하고, 하위 10개 지역의 state(주), county(지역명), 아시아인 인구 백분율을 출력

midwest %>% 
  mutate(ratio_asian = (popasian / poptotal)*100) %>% 
  arrange(ratio_asian) %>% 
  select(state, county, ratio_asian) %>% 
  head(10)

