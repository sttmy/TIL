##### 9장 데이터분석 실습
##### 한국복지패널데이터

install.packages('foreign') # SPSS에서 사용하는 파일(예 .sav 등) 로드하기 위한 패키지

library(foreign)
library(dplyr)
library(ggplot2)
library(readxl)

# 데이터불러오기
raw_welfare <- read.spss(file = "Data/Koweps_hpc10_2015_beta1.sav", to.data.frame = T)
welfare <- raw_welfare # 복사본만들기

head(welfare)
tail(welfare)
View(welfare)
str(welfare)   #col변수, 데이터타입 확인
summary(welfare)

# 변수명 바꾸기, 데이터명세서 보고 결정
welfare <- rename(welfare, 
                  sex = h10_g3,
                  birth = h10_g4,
                  marriage = h10_g10,
                  religion = h10_g11,
                  income = p1002_8aq1,
                  code_job = h10_eco9,
                  code_region = h10_reg7)

##### 전처리
table(welfare$sex)
class(welfare$sex)

# 이상치 및 결측치 처리
welfare$sex <- ifelse(welfare$sex == 9, NA, welfare$sex)
table(is.na(welfare$sex))

# 성별 항목 이름 부여
welfare$sex <- ifelse(welfare$sex ==1, 'male','female')
table(welfare$sex)
qplot(welfare$sex)

# 월급정보
class(welfare$income)
summary(welfare$income)
qplot(welfare$income)
qplot(welfare$income) + xlim(0,1000)   #bin의 갯수가 자동으로 달라짐
qplot(welfare$income) + xlim(0,1000) + ylim(0,1000)

# 이상치 결측처리
summary(welfare$income)
welfare$income <- ifelse(welfare$income %in% c(0,9999), NA, welfare$income)   # 0과 9를 결측치처리
welfare$income
table(welfare$income)
table(is.na(welfare$income))   # 결측치가 많지만, 유소득자 대상 데이터 분석을 위해 처리

# 성별 월급 평균표 만들기
sex_income <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(sex) %>% 
  summarise(mean_income = mean(income))
sex_income
ggplot(data = sex_income, aes(x = sex, y = mean_income))+
  geom_col()


# 나이와 성별 관계
class(welfare$birth)
summary(welfare$birth)
qplot(welfare$birth)

# 나이 이상치 결측 처리
welfare$birth <- ifelse(welfare$birth == 9999, NA, welfare$birth)
table(is.na(welfare$birth))

# 출생연도에서 나이 추출하기
welfare$age <- 2015 - welfare$birth + 1
summary(welfare$age)
qplot(welfare$age)

# 나이별로 연봉 차이가 있나
diff <- welfare %>% 
  filter(!is.na(age) & !is.na(income)) %>% 
  group_by(age) %>% 
  summarise(mean_inc = mean(income))

ggplot(data = diff, aes(x = age, y = mean_inc)) +
  geom_line()

# 나이별 3개 그룹으로 나누어서 qplot 만들어보기
welfare <- welfare %>% 
  mutate(ageg = ifelse(age < 30 , "young", ifelse(age <= 59, "middle","old")))

table(welfare$ageg)
qplot(welfare$ageg)

welfare <- welfare %>% 
  mutate(agegr = ifelse(age >= 60 , "old", ifelse(age < 30, "young", "middle")))
qplot(welfare$agegr)

# 연령대에 따른 월급 차이
ageg_income <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg) %>% 
  summarise(mean_income = mean(income))

ggplot(data = ageg_income, aes(x = ageg, y = mean_income)) +
  geom_col() + scale_x_discrete(limits = c('young','middle','old'))   # 바 순서 지정가능

# 연령대별 성별 월급 차이
sex_income <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg, sex) %>% 
  summarise(mean_income = mean(income))
sex_income

ggplot(data = sex_income, aes(x = ageg, y = mean_income, fill = sex)) +   #fill: 성별로 나눠줌
  geom_col() + scale_x_discrete(limits = c('young','middle','old'))   

ggplot(data = sex_income, aes(x = ageg, y = mean_income, fill = sex)) +
  geom_col(position = 'dodge') + # position = 'dodge' 누적그래프말고, 옆에 쌓아줌 
  scale_x_discrete(limits = c('young','middle','old'))   

### 나이대별 성별 월급 차이 p231
dif <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(sex, age) %>% 
  summarise(mean_dif = mean(income))
dif
ggplot(data = dif, aes(x = age, y = mean_dif, col = sex)) +   #col: 성별로 색상 구분
  geom_line()

### 직업별 월급 차이 p35
# 데이터 불러오기
list_job <- read_excel('Data/Koweps_Codebook.xlsx', col_names = T, sheet = 2)
head(list_job)
dim(list_job)
class(list_job)
table(welfare$code_job)

# welfare에 코드 직업 합치기
welfare <- left_join(welfare, list_job, by = "code_job")
welfare %>% 
  filter(!is.na(code_job)) %>% 
  select(code_job, job) %>% 
  head(10)

# 직업별 월급 평균
job_ic <- welfare %>% 
  filter(!is.na(job) & !is.na(income)) %>% 
  group_by(job) %>% 
  summarise(mean_ic = mean(income))
head(job_ic)

# 상위 top10 직업
top10 <- job_ic %>% 
  arrange(desc(mean_ic)) %>% 
  head(10)
top10

# 하위 bottom10 직업
bottom10 <- job_ic %>% 
  arrange(mean_ic) %>% 
  head(10)
bottom10

bottom10_b <- job_ic %>% 
  arrange(desc(mean_ic)) %>% 
  tail(10)
bottom10_b

job_ic
ggplot(data = top10, aes(x = reorder(job, mean_ic), y =mean_ic))+
  geom_col() + 
  coord_flip()   # coord_flip 가로로 표시

ggplot(data = bottom10, aes(x = reorder(job, -mean_ic), y =mean_ic)) + # -mean_ic작은 수부터 그리기    
  geom_col() + 
  coord_flip() + 
  ylim(0, 600)

## 성별 직업 빈도
# 남성 직업빈도 상위 10개
job_male <- welfare %>% 
  filter(!is.na(job) & sex == 'male') %>% 
  group_by(job) %>% 
  summarise(n = n()) %>%  
  arrange(desc(n)) %>% 
  head(10)

# 여성 직업빈도 상위 10개
job_female <- welfare %>% 
  filter(!is.na(job) & sex == 'female') %>% 
  group_by(job) %>% 
  summarise(n = n()) %>%  
  arrange(desc(n)) %>% 
  head(10)

ggplot(data = job_male, aes(x = reorder(job,n), y = n)) + 
  geom_col() + 
  coord_flip() 


ggplot(data = job_female, aes(x = reorder(job, n), y = n)) + 
  geom_col() + 
  coord_flip()


### 종교 유무에 따른 이혼율 p249
class(welfare$religion)  # 1.Y, 2.N
table(welfare$religion) 
class(welfare$marriage)  # 0.18세미만 1.유배우 2.사별 3.이혼 4.별거 5.미혼(18세이상, 미혼모 포함) 6.기타(사망 등)
table(welfare$marriage)

# 종교 유무에 이름부여
welfare$religion <- ifelse(welfare$religion == 1, "Y","N")
table(welfare$religion)
qplot(welfare$religion)

# 이혼변수 만들기
welfare$group_marriage <- ifelse(welfare$marriage == 1, 'marriage', ifelse(welfare$marriage == 3, 'divorced', NA))
table(welfare$group_marriage)
table(is.na(welfare$group_marriage))
qplot(welfare$group_marriage)

# 종교 유무에 따른 이혼율 
religion_marriage <- welfare %>% 
  filter(!is.na(group_marriage)) %>% 
  group_by(religion, group_marriage) %>% 
  summarise(n=n()) %>%  
  mutate(tot_group = sum(n), 
         pct = round((n/tot_group*100), 1))

# 종교 유무에 따른 이혼율 추출
divorced <- religion_marriage %>% 
  filter(group_marriage == "divorced") %>% 
  select(religion, pct)
ggplot(data = divorced, aes(x = religion, y = pct)) +
  geom_col()

# 연령대별 이혼율
ageg_marriage2 <- welfare %>% 
  filter(!is.na(group_marriage)) %>% 
  group_by(ageg, group_marriage) %>% 
  summarise(n=n()) %>% 
  mutate(tot_group = sum(n),
         pct = round((n/tot_group*100),1))
### tch  
ageg_marriage <- welfare %>% 
  filter(!is.na(group_marriage)) %>% 
  count(ageg, group_marriage) %>% 
  group_by(ageg) %>% 
  mutate(pct = round((n/sum(n)*100),1))
ageg_marriage

# 초년 제외하고 이혼율 추출
ageg_divorced <- ageg_marriage %>% 
  filter(ageg !='young' & group_marriage == 'divorced') %>% 
  select(ageg, pct)

ggplot(data = ageg_divorced, aes(x = ageg, y = pct)) +
  geom_col()

# 연령대, 종교유무, 결혼상태별 비율표 만들기
ageg_religion_marriage <- welfare %>% 
  filter(!is.na(group_marriage) & (ageg != 'young')) %>% 
  group_by(ageg, religion, group_marriage) %>% 
  summarise(n = n()) %>% 
  mutate(tot_group = sum(n),
         pct = round(n/tot_group*100, 1))

# 연령대, 종교유무, 이혼율 표 만들기
df_divorce <- ageg_religion_marriage %>% 
  filter(group_marriage == 'divorced') %>% 
  select(ageg, religion, pct)

ggplot(data = df_divorce, aes(x = ageg, y = pct, fill = religion)) +  #python 에서는 hue
  geom_col(position = 'dodge')   # position 누적인지 분리인지, dodge는 분리


### 지역별 연령대 비율 p69
View(welfare)
table(welfare$code_region)

# 지역코드 목록 만들기
list_region <- data.frame(code_region = c(1:7),
                          region = c('서울','수도권(인천/경기)','부산/경남/울산','대구/경북','대전/충남','강원/충북','광주/전남/전북/제주도'))
welfare <- left_join(welfare, list_region, by = "code_region")
table(welfare) 
welfare %>% 
  select(code_region, region) %>% 
  head()

region_ageg <- welfare %>% 
  group_by(region, ageg) %>% 
  summarise(n=n()) %>% 
  mutate(tot_group = sum(n), 
         pct = round(n/tot_group*100, 1))

ggplot(data = region_ageg, aes(x = region, y = pct, fill=ageg)) +
  geom_col() +
  coord_flip()   # 세로막대그래프


# 노년층 비율을 내림차순으로
list_order_old <- region_ageg %>% 
  filter(ageg=='old') %>% 
  arrange(desc(pct))

# 지역명 노년층비율 높은 순서 변수 만들기
order <- list_order_old$region

ggplot(data = region_ageg, aes(x = region, y = pct, fill = ageg)) +
  geom_col() +
  coord_flip() +
  scale_x_discrete(limits = rev(order))   #reverse 반대로 만들기, 오름차순으로 해서 정렬하거나, 만들 때 반대로 정렬하기.
