##### 7. 지도로 시각화하기

getwd()
setwd("C:/R_workspace")

load("Data_s/06_geodataframe/06_apt_price.rdata")
library(sf)
grid <- st_read("Data_s/seoul/seoul.shp")  # seoul.zip 압축풀고 모든 파일 유지한 상태에서 .shp파일만 불러옴

# 데이터 결합
head(apt_price,3)
head(grid,3)

apt_price <- st_join(apt_price, grid, join=st_intersects) # 실거래+그리드 결합
head(apt_price,3)


#---------------------------------------------------------
##### 1.어느 지역이 제일 비쌀까?
### 1) 지역별 평균 가격 구하기

# 그리드별 평당 평균가격 계산
kde_high <- aggregate(apt_price$py, by=list(apt_price$ID), mean) 
head(kde_high,3)
colnames(kde_high) <- c("ID","avg_price")
head(kde_high,3)

#---------------------------------------------------------
### 2) 그리드와 평균가격 결합
head(grid,3)
kde_high <- merge(grid, kde_high, by = "ID")  # ID 기준으로 결합
head(kde_high,3)

#---------------------------------------------------------
### 3) 동별? 평균가격 정보 표시하기
library(ggplot2)
library(dplyr)
kde_high %>% 
  ggplot(aes(fill = avg_price)) + 
  geom_sf() + 
  scale_fill_gradient(low = "white", high = "red")

#---------------------------------------------------------
### 4) 지도의 경계 그리기
library(sp)
kde_high_sp <- as(st_geometry(kde_high), 'Spatial')   # sf형→sp형 데이터로 변환, 지도작업 수월한 진행을 위해
## sp형은 위도, 경도 값 / sf형은 point( , )
head(kde_high_sp,2)
x <- coordinates(kde_high_sp)[,1]   # 그리드중심 x,y좌표 추출
y <- coordinates(kde_high_sp)[,2]

## bbox로 l1~l4까지 외곽끝점을 나타내는 좌표 4개 추출, 약간의 여유를 주고자 0.1% 추가함
l1 <- bbox(kde_high_sp)[1,1] - (bbox(kde_high_sp)[1,1] * 0.0001)
l2 <- bbox(kde_high_sp)[1,2] + (bbox(kde_high_sp)[1,2] * 0.0001)
l3 <- bbox(kde_high_sp)[2,1] - (bbox(kde_high_sp)[2,1] * 0.0001)
l4 <- bbox(kde_high_sp)[2,2] + (bbox(kde_high_sp)[2,2] * 0.0001)

install.packages('spatstat')
library(spatstat)
win <- owin(xrange = c(l1, l2), yrange = c(l3, l4))
plot(win)

#---------------------------------------------------------
### 5) 밀도그래프 표시 데이터가 집중된 곳 찾기. 커널 밀도 추정
p <- ppp(x,y, window = win)   #경계창 위에 좌표값 포인트 생성
p
d <- density.ppp(p, weights = kde_high$avg_price,  # 커널 밀도함수로 변환
                 sigma = bw.diggle(p),
                 kernel = 'gaussian')
plot(d)

rm(list = c("kde_high_sp","apt_price", "l1","l2","l3","l4","x","y","win","p"))  # 변수정리

#---------------------------------------------------------
### 6) 픽셀 이미지를 래스터 이미지로 변환
View(d)
quantile(d) 
d[d<quantile(d)[4] + (quantile(d)[4]*0.1)] <- NA  #하위 75%를 NA처리

install.packages("raster")
library(raster)
raster_high <- raster(d)   #래스터 변환
plot(raster_high)

#---------------------------------------------------------
### 7) 클리핑, 불필요한 부분 자르기
bnd <- st_read("Data_s/sigun_bnd/seoul.shp")  # 서울시 경계선만 그리는 데이터 불러오기
raster_high <- crop(raster_high, extent(bnd))   # 외곽선 자르기
crs(raster_high) <- sp::CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")   # 좌표계 정의, 띄어쓰기 중요
plot(raster_high)   #지도 확인
plot(bnd, col=NA, border = "red", add=TRUE)


#---------------------------------------------------------
### 8) 지도 그리기
install.packages("rgdal")
library(rgdal)  
library(leaflet)
leaflet() %>% 
  addProviderTiles(providers$CartoDB.Positron) %>% 
  addPolygons(data = bnd, weight = 3, color = "red", fill = NA) %>% 
  addRasterImage(raster_high, 
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_high), 
                                       na.color = "transparent"),
                 opacity = 0.4)
#---------------------------------------------------------

dir.create("Data_s/07_map")
save(raster_high, file = "Data_s/07_map/07_kde_high.rdata")
rm(list=ls())
  