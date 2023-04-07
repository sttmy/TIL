#점심먹고 
# PPT 4장 p19~
# RDS 파일로 저장 용량이 더 크지만 R에서 전용으로 쓸 수 있는 파일임

# saveRDS(df_midterm, file='R/data/df_midterm2.rds')

# 옆에 만들어둔 테이블 지우기 (rermove) - save for memory
# rm(df_midterm)
# rm(df_midterm2)

# RDS 파일 불러오기 
# df_midterm <- readRDS('R/data/df_midterm2.rds') 내가 폴더 채로 옯겨서 경로 data/가 더 있음 

# 100 page 쪽 한대요 - 여기서 환경창 빗자루로 지웠음
# exam <- read.csv('R/data/csv_exam.csv')
# head(exam) #6행 - 저작권 문제로 6행 
# head(exam, 10) #10행
# tail(exam) # 뒤에서 6행
#
# View(exam) - view 창에서 데이터 확인 = 그 차트 나오는거  
#
# dim(exam) #행, 열 출력
# str(exam) #데이터 속성 확인
#
# summary(exam) # describe 같은거 
# 
# ggplot mpg 데이터 프레임 형태로 불러오기
# mpg <- as.data.frame(ggplot2::) 데이터 불러오는 형식
#
# head(mpg)
# tail(mpg, 2)
# View(mpg)
# dim(mpg)
# summary(mpg)
# 
# 이제 5-2 장이라함...
# 변수명 바꾸기
# 위해서
# dplyr설치

# install.packages("dplyr")
# library(dplyr)
# 
# df_raw <- data.frame(var1 = c(1,2,3), var2 = c(2,3,4))
# df_raw
# df_new <- df_raw
# df_new <- rename(df_new, v2 = var2)
# df_new
#
# 차트위에 cty, hwy rename 하기
# mpg_new <- mpg
# mpg_new <-  rename(mpg_new, city = cty, highway = hwy)
#
# 5-3 파생변수 만들기
# df <- data.frame(var1 =c(4,3,8), var2=c(2,6,1))
#
# var1이나 2만 가져오고 싶을때 
# $ 달러사인을 붙인다 
# ex) df$var1 + df$var2
# df$var_sum = df$var1 + df$var2 없는 컬럼 만들때 앞에 sum 컬럼 생성
# df$var_mean = (df$var1 + df$var2)/2 이러면 var_mean 컬럼이 제일 오른족에 새로 생성
# 
# mpg에서 total column 만들고 통합연비 평균을 구해라 
# mpg$total <- (mpg$cty + mpg$hwy)/2
# mean(mpg$total)
# summary(mpg$total)
# hist(mpg$total)  - 히스토그램
#
# # total 기준으로 A,B,C 등급부여 
# mpg$grade <- ifelse(mpg$total >=30, 'A', ifelse(mpg$total >=20,'B', 'C'))
# head(mpg,20) - 오른쪽 끝에 grade add 됨 
# table(mpg$grade)
# qplot(mpg$grade) bar chart
# 
# grade2로 나눠서 다시 만들었을 때
# mpg$grade2 <- ifelse(mpg$total >=30, 'A', ifelse(mpg$total >=25, 'B', ifelse(mpg$total >=20, 'C', 'D')))
# head(mpg, 10)
# table(mpg$grade2)
# qplot(mpg$grade2)
#
# test로 20 이상 일때 pass else fail 일때
# mpg$test <- ifelse(mpg$total >=20, 'Pass','Fail')
# head(mpg)
# table(mpg$test)
# qplot(mpg$test)
# -------- 여기까지 chapter 4~5 까지 -----------
# 저장 하고 new script , ctrl + L 


########################################

## R 6장 p68 퀴즈

#Q1. class별 cty평균

#Q2.  앞 문제의 출력 결과는 class 값 알파벳 순으로 정렬되어 있습니다. 어떤 차종의 도시 연비가 높은지 쉽게 알아볼 수 있도록 cty 평균이 높은 순으로 정렬해 출력

#Q3. 어떤 회사 자동차의 hwy(고속도로 연비)가 가장 높은지 알아보려고 합니다. hwy 평균이 가장 높은 회사 세 곳을 출력
mpg %>% 
  group_by(manufacturer) %>% 
  summarise(mean_hwy = mean(hwy)) %>% 
  arrange(desc(mean_hwy)) %>% 
  head(3)

# Q4. 어떤 회사에서 "compact"(경차) 차종을 가장 많이 생산하는지 알아보려고 합니다. 각 회사별 "compact" 차종 수를 내림차순으로 정렬

