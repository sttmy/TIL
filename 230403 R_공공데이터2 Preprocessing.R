##### 4.전처리

load("Data_s/03_integrated/apt_price.rdata")  #rdata사용하면 용량이 줄어듦
head(apt_price)
str(apt_price)

### 1) 결측값
# 결측값확인
table(is.na(apt_price))

# 결측값 제거 후 확인
apt_price <- na.omit(apt_price)
table(is.na(apt_price))


### 2) 문자열 전처리 (공백 제거)
library(stringr)   # 문자열 처리하는 패키지
apt_price <- as.data.frame(apply(apt_price, 2, str_trim))  #str_trim: 공백제거 함수. 
# apply함수, 1은 행, 2는 열
head(apt_price, 2)


### 3) 항목별 데이터 다듬기   # 문자형/숫자형 데이터 속성 일관되도록 변경
## 3-1) 매매 연월일, 데이터 만들기
install.packages("lubridate")   # make_date() 함수 필요
library(lubridate)
library(dplyr) 
head(apt_price)
apt_price <- apt_price %>% 
  mutate(ymd = make_date(year, month, day))         #연월일
apt_price$ym <- floor_date(apt_price$ymd, "month")  #연월, 1일로 일괄 통일
head(apt_price,2)

## 3-2) 매매가 변환하기
str(apt_price)
head(apt_price$price, 3)
apt_price$price <- apt_price$price %>% 
  sub(",","",.) %>%   # 쉼표 제거, .은 전체
  as.numeric()        # 숫자로 변경

## 3-3) 주소 조합하기
head(apt_price$apt_nm, 30)

# 괄호 이후 삭제
apt_price$apt_nm <- gsub("\\(.*","",apt_price$apt_nm)   # sub는 첫번째 일치 항목에 적용, gsub은 모든 일치 항목에 적용

# 아파트 이름, 지역코드, 주소 조합
loc <- read.csv('Data_s/sigun_code.csv', fileEncoding = 'UTF-8')
apt_price <- merge(apt_price, loc, by = 'code')
head(apt_price)

apt_price$juso_jibun <- paste0(apt_price$addr_2, " ",
                               apt_price$dong_nm, " ",
                               apt_price$jibun, " ",
                               apt_price$ apt_nm)
head(apt_price,2)


### 4) 건축연도 숫자 변환
str(apt_price)
apt_price$con_year <- apt_price$con_year %>% 
  as.numeric()


### 5) 평당매매가
## round를 0으로, 평으로 바꾸려면 면적에 3.3을 곱하면 됨
apt_price$area <- apt_price$area %>% 
  as.numeric()
str(apt_price)
apt_price$area <- round(apt_price$area*3.3,0)

#tch
head(apt_price$area,3)
apt_price$area <- apt_price$area %>% 
  as.numeric() %>% 
  round(0)
head(apt_price$area,3)
apt_price$py <- round(((apt_price$price/apt_price$area)*3.3),0)
head(apt_price$py,3)

### 6) 층수변환: 지하1층을 1층으로 처리, 숫자로 변환 후 절대값 사용
table(apt_price$floor)
as.numeric(apt_price$floor)
apt_price$floor <- ifelse(apt_price$floor == -1, 1, apt_price$floor)
as.character(apt_price$floor)

#tch
table(apt_price$floor)
apt_price$floor <- apt_price$floor %>% 
  as.numeric() %>% 
  abs()
table(apt_price$floor)
min(apt_price$floor)

apt_price$cnt <- 1 # 모든 행에 숫자1을 할당, count를 sum활용해 도출
head(apt_price,3)

### 7) 저장하기, 필요한 컬럼만 추출
apt_price <- apt_price %>% 
  select(ymd, ym, year, code, addr_1, apt_nm, juso_jibun, price, area, con_year, area, floor, py, cnt)
str(apt_price)


dir.create("Data_s/04_preprocess")
save(apt_price, file = "Data_s/04_preprocess/04_preprocess.rdata")
write.csv(apt_price, file = "Data_s/04_preprocess/04_preprocess.csv")
