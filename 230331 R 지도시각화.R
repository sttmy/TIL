##### 지도시각화
##### 단계구분도

install.packages("mapproj")
install.packages("ggiraphExtra")
library(ggiraphExtra)

# 내장데이터 불러와서 사용 USArrests
str(USArrests)
head(USArrests)

library(tibble)   # dplyr과 함께 설치됨
# 행 이름을 state 변수로 바꿔 데이터프레임 생성
crime <- rownames_to_column(USArrests, var = "state")
# state 이름 소문자로 바꾸기
crime$state <- tolower(crime$state)
head(crime, 3)
dim(crime)

# 미국 지도데이터 준비
install.packages("maps")  # 미국, 위도, 경도정보 패키지
library(ggplot2)
states_map <- map_data("state")  #map_data 매소드 사용
str(states_map)
dim(states_map)

ggChoropleth(data = crime,
             aes(fill = Murder,   # 색깔 기준 변수
                 map_id = state),  # 지역 기준 변수
             map = states_map,   # 지도 데이터
             interactive = T) # 맵에 가져다 대면 자료 기반 상호작용


##### 대한민국 시도별 인구, 결핵환자 수 단계구분도
install.packages('stringi')
install.packages('devtools')
devtools::install_github("cardiomoon/kormaps2014") 

library(kormaps2014)
head(korpop1,3)
str(changeCode(korpop1))
library(dplyr)
korpop1 <- rename(korpop1,
                  pop = 총인구_명,
                  name = 행정구역별_읍면동
                  )
korpop1$name <- iconv(korpop1$name, "UTF-8","CP949")   #한글 인코딩 변경
str(kormap1)
str(kormap2)
str(changeCode(kormap1))
ggChoropleth(data = korpop1,
             aes(fill = pop, 
                 map_id = code,
                 tooltip = name),
             map = kormap1,
             interactive = T)


### 결핵환자 수 데이터
rm(tbc)
str(tbc)     
str(changeCode(tbc))   # 한글 깨져서 나올 때, changeCode

tbc$name <- iconv(tbc$name, "UTF-8","CP949")
View(tbc)

ggChoropleth(data = tbc,
             aes(fill = NewPts, 
                 map_id = code,
                 tooltip = name),
             map = kormap1,
             interactive = T)

