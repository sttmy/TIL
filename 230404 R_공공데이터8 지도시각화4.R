##### 8.통계분석과 시각화

#####  서울에서 가장 비싼 지역만 찾기

rm(list = ls())
# 데이터 불러오기
load("Data_s/06_geodataframe/06_apt_price.rdata")  # 2021년 서울 아파트 실거래가
load("Data_s/07_map/07_kde_high.rdata")  # 최고가 래스터이미지
library(sf)
grid <- st_read("Data_s/seoul/seoul.shp")   # 서울시그리
드

# 그리드 그리기
install.packages("tmap")
library(tmap)
tmap_mode('view')
tm_shape(grid) + tm_borders() + 
  tm_text("ID",col = "red") +  #ID기준으로 표시
  # 래스터 이미지 그리기
  tm_shape(raster_high) + 
  # 래스터 이미지 색상 패턴 설정
  tm_raster(palette = c('blue','green','yellow','red'), alpha = .4) + # alpha는 투명도
  # 기본지도설정
  tm_basemap(server = c("OpenStreetMap"))
  

##### 전체지역 / 관심지역 저장하기

library(dplyr)
apt_price <- st_join(apt_price, grid, join = st_intersects)  # 실거래가, 그리드
head(apt_price,2)
apt_price <- apt_price %>% 
  st_drop_geometry()   # 실거래에서 공간 속성 지우기
all <- apt_price
sel <- apt_price %>% filter(ID==81016)   # 관심지역(81016, 제일 증가율 높은 곳) 추출

dir.create("Data_s/08_chart")
save(all, file = "Data_s/08_chart/all.rdata")
save(sel, file = "Data_s/08_chart/sel.rdata")

rm(list = ls())



















