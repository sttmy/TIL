# 데이터 불러오기
load("Data_s/04_preprocess/04_preprocess.rdata")  # 실거래 자료
load("Data_s/05_geocoding/05_juso_geocoding.rdata")  # 지오코딩 좌표 

# 데이터 합치기
library(dplyr)
head(apt_price$juso_jibun,3)
head(juso_geocoding$apt_juso, 3)

apt_price <- left_join(apt_price, juso_geocoding, 
                       by = c('juso_jibun' = "apt_juso"))
head(apt_price,3)

# 결측치 제거
table(is.na(apt_price))
apt_price <- na.omit(apt_price)
table(is.na(apt_price))


##### 지오 데이터프레임 만들기

install.packages('sp')
install.packages('sf')
library(sp)
library(sf)

coordinates(apt_price) <- ~coord_x + coord_y # 좌표값 할당
proj4string(apt_price) <- "+proj=longlat + datum=WGS84 +no_defs"   # 좌표계(CRS) 정의

apt_price <- st_as_sf(apt_price)   # sp형을 sf형으로 변환


##### 지오데이터프레임 시각화
plot(apt_price$geometry, axes = T, pch = 1)  # 플롯 그리기
install.packages('leaflet')    #지도그리는 라이브러리
library(leaflet)

leaflet() %>% 
  addTiles() %>% 
  addCircleMarkers(data=apt_price[1:1000,], label = ~apt_nm)  # 1000개만 그리기

### 저장하기

dir.create("Data_s/06_geodataframe")
save(apt_price, file="Data_s/06_geodataframe/06_apt_price.rdata")
write.csv(apt_price, file="Data_s/06_geodataframe/06_apt_price.csv")
  

