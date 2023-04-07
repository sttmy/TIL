##### data.go.kr 가입, API인증키
## 아파트매매 실거래자료 

##### XML: 마크업 언어(태그 사용해 문서 내 요소 정의), 다양한 플랫폼 간 데이터 교환(확장버전, vs html은 웹페이지 구조 개발)

##### 3-1.Crawling

#### 지역  & 인증키 & 날짜 보내기
install.packages("rstudioapi")
getwd()
setwd("C:/R_workspace")

## 1) 수집대상 지역 설정
loc <- read.csv("Data_s/sigun_code.csv", fileEncoding = "UTF-8")
str(loc$code)
loc$code <- as.character(loc$code)  #code를 문자로 변경
head(loc)

## 2) 수집기간 설정하기
datelist <- seq(from = as.Date('2021-01-01'),  # 시작
                to = as.Date('2021-12-31'), # 종료
                by = '1 month') # 단위
datelist <- format(datelist, format = '%Y%m') # 형식변환 YYYY-MM-DD 를 YYYYMM으로
datelist[1:3]

## 3)인증키
service_key <- 

##### 3-2.요청목록 생성

# for문으로 요청목록 채우기
url_list <- list() # 빈리스트 설정
cnt <- 0 # 반복문 제어별수 초기값 설정
for (i in 1:nrow(loc)){           # 외부 반복: 25개 자치구
  for (j in 1:length(datelist)){  # 내부 반복: 12개월
    # URL 목록 채우기
    cnt <- cnt + 1
    url_list[cnt] <- paste0("http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?",
                            
                           "LAWD_CD=", loc[i,1],  # 지역코드
                           "&DEAL_YMD=", datelist[j],   # 수집월
                           "&numOfRows=", 100,  # 가져올 최대자료 수
                           "&serviceKey=", service_key)
  Sys.sleep(0.1)  # 0.1초간 멈춤
  msg <- paste0("[",i,"/",nrow(loc),"]", loc[i,3], "의 크롤링 목록이 생성됨 => 총 [", cnt, "] 건")
  cat(msg, "\n\n")
  }
}

View(url_list)

length(url_list)
#browseURL(paste0(url_list[1]))

##### 3-3 크롤러 제작: 자동으로 자료 수집

# 라이브러리 설치 및 불러오기
install.packages("XML")
install.packages("data.table")
install.packages("stringr")
library(XML)
library(data.table)
library(stringr)

raw_data <- list()  # XML 임시저장소
root_Node <- list()  # 거래내역 추출 임시저장소
total <-list()  # 거래내역 정리 임시저장소
dir.create("Data_s/02_raw_data")  # 디렉토리(폴더) 생성
dir.create("Data_s/raw_data")  # 디렉토리(폴더) 생성

url_list[1]
# URL 요청- XML응답
for (i in 1:length(url_list)) {      # 요청목록 url_list 반복
  raw_data[[i]] <- xmlTreeParse(url_list[i], useInternalNodes = TRUE, encoding = "UTF-8")  # 결과저장
  root_Node[[i]] <- xmlRoot(raw_data[[i]])   # xmlRoot로 루트 노드 이하 추출
  items <- root_Node[[i]][[2]][['itmes']]   # 전체 거래내역(items) 추출
  size <- xmlSize(items)   # 전체 거래건수 확인
  
  # 거래내역 추출
  item <- list()
  item_temp_dt <- data.table()  # 세부거래내역(item) 저장 임시테이블 생성
  Sys.sleep(.1)
  for (m in 1:size){   # 전체 거래건수(size)만큼 반복
    item_temp <- xmlSApply(items[[m]], xmlValue)
    item_temp_dt <- data.table(year = item_temp[4],    # 거래연도
                               month = item_temp[7],   # 거래월
                               day = item_temp[8],     # 거래일
                               price = item_temp[1],   # 거래금액
                               code = item_temp[12],   # 지역코드
                               dong_nm = item_temp[5], # 법정동
                               jibun = item_temp[11],  # 지번
                               con_year = item_temp[3],  # 건축연도
                               apt_nm = item_temp[6],  # 아파트이름
                               area = item_temp[9],    # 전용면적
                               floor = item_temp[13])  # 층수
    item[[m]] <- item_temp_dt
    }
  apt_bind <- rbindlist(item)  # 통합저장
  
  # 응답내역 저장
  region_nm <- subset(loc, code = str_sub(url_list[i], 115, 119))$addr_1 # 지역명 추출
  month <- str.sub(url_list[i], 130, 135)    #연월(YYYYMM)
  path <- as.character(paste0("Data_s/raw_data/", region_nm, "_", month, ".csv"))
  write..csv(apt_bind, path)    # csv저장
  msg <- paste0("[",i,"/",length(url_list), "] 수집한 데이터를 [", path,"] 에 저장합니다")
  cat(msg, "\n\n")
} 



files <- dir('Data_s/02_raw_data')
library(plyr)


apt_price <- ldply(as.list(paste0("Data_s/02_raw_data/", files)), read.csv)  # 결합. files에 있는 파일을 불러와서 list를 합쳐줌

# 저장해주기
dir.create("Data_s/03_integrated")
save(apt_price, file = "Data_s/03_integrated/apt_price.rdata")
write.csv(apt_price, file = "Data_s/03_integrated/apt_price.csv")

