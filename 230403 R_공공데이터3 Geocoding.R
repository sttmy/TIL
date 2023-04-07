##### 5.지오코딩

### 1) 준비
## 1-1) 카카오API발급

## 2-2) 중복주소 제거  
load("Data_s/04_preprocess/04_preprocess.rdata")  # 실거래 자료 불러오기
apt_juso <- data.frame(apt_price$juso_jibun)  # 주소가 있는 컬럼 추출
apt_juso <- data.frame(apt_juso[!duplicated(apt_juso), ])  # 고유한 주소만 추출, 겹치지 않는 주소만
head(apt_juso)

### 2) 지오코딩하기 (주소를 좌표로 변경)

install.packages('httr')
install.packages("RJSONIO")
library(httr)
library(RJSONIO)
library(data.table)
library(dplyr)

add_list <- list()
cnt <- 0
kakao_key = 

for (i in 1:nrow(apt_juso)){
  tryCatch(                # try ~ except와 유사한 기능, 예외처리
    { 
      # 주소로 좌표값 요청
      lon_lat <- GET(url = "https://dapi.kakao.com/v2/local/search/address.json", 
                 query = list(query = apt_juso[i,]),
                 add_headers(Authorization = paste0("KakaoAK ", kakao_key)))
      # 위도,경도만 추출해서 저장
      coordxy <- lon_lat %>% 
        content(as = 'text') %>% 
        RJSONIO::fromJSON()
      cnt = cnt + 1
      # 주소의 경도, 위도 정보를 리스트로 저장
      add_list[[cnt]] <- data.table(apt_juso = apt_juso[i,],
                              coord_x = coordxy$documents[[1]]$x,
                              coord_y = coordxy$documents[[1]]$y)
      msg <- paste0("[",i,"/",nrow(apt_juso),"]번째 (", 
                    round(i/nrow(apt_juso)*100,2)," %) [",
                    apt_juso[i,],"] 지오 코딩 중입니다: X= ",
                    add_list[[cnt]]$coord_x, " /Y= ",
                    add_list[[cnt]]$coord_y)
      cat(msg, "\n\n")
      # 예외처리
    }, error = function(e){cat("ERROR :", conditionMessage(e), "\n")}
  )
}

### 3) 지오코딩 결과 저장
juso_geocoding <- rbindlist(add_list)   # 리스트를 데이터프레임으로 변환
juso_geocoding$coord_x <- as.numeric(juso_geocoding$coord_x)
juso_geocoding$coord_y <- as.numeric(juso_geocoding$coord_y)
table(is.na(juso_geocoding))
juso_geocoding <- na.omit(juso_geocoding)  # 결측치 제거

dir.create("Data_s/05_geocoding")
save(juso_geocoding, file="Data_s/05_geocoding/05_juso_geocoding.rdata")
write.csv(juso_geocoding, file="Data_s/05_geocoding/05_juso_geocoding.csv")


### 참고: 저자 깃허브 : https://github.com/cmman75/Open_data_R_with_Shiny/blob/main/05_%EC%A7%80%EC%98%A4%20%EC%BD%94%EB%94%A9.R


##### tryCatch문 연습
inputs <- list(1,2,3, 'four', 5, 6)
for (input in inputs){
  print(paste(input, "의 로그값은: ", log(input)))}

for (input in inputs){
  tryCatch({
    print(paste(input, "의 로그값은: ", log(input)))
    }, error = function(e){cat("Error: ", conditionMessage(e),"\n")}
    )}
    
    
    
    