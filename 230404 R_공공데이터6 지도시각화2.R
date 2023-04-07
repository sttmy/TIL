##### 7-2) 요즘 뜨는 지역은?
# 일정기간동안 가장 많이 오른 지역

# 데이터 불러오기
load("Data_s/06_geodataframe/06_apt_price.rdata")  #실거래데이터
grid <- st_read("Data_s/seoul/seoul.shp")  # 서울시 1km 격자데이터
apt_price <- st_join(apt_price, grid, join = st_intersects)
  
head(apt_price,2)
tail(apt_price,2)
str(apt_price)

# 이전/이후 데이터세트 만들기
kde_before <- subset(apt_price, ymd < "2021-07-01") # 이전데이터
kde_after <- subset(apt_price, ymd >= "2021-07-01") # 이후데이터

# 전반기/후반기 ID별 가격 형균집계
kde_before <-aggregate(kde_before$py, by = list(kde_before$ID), mean)
kde_after <-aggregate(kde_after$py, by = list(kde_after$ID), mean)

colnames(kde_before) <- c("ID","before")
colnames(kde_after) <- c("ID","after")

# 데이터 결합 (이전/이후 차이 비교)
kde_diff <- merge(kde_before, kde_after, by = "ID")
kde_diff$diff <- round(( ( kde_diff$after - kde_diff$before ) / kde_diff$before * 100 ), 0)   # 변화율
head(kde_diff, 2)

# 가격이 오른 지역
library(sf)
kde_diff <- kde_diff[kde_diff$diff >0, ]  # 상승 지역만 추출
kde_hot <- merge(grid, kde_diff, by = "ID")  # 그리드에 상승지역 결합
library(ggplot2)
library(dplyr)
kde_hot %>% 
  ggplot(aes(fill = diff)) +
  geom_sf() +
  scale_fill_gradient(low = "white", high = "red")

#--------------------------------------------------------------------------
# 지도 경계선 그리기
library(sp)
kde_hot_sp <- as(st_geometry(kde_hot), 'Spatial')
head(kde_hot_sp,2)
x <- coordinates(kde_hot_sp)[,1]   # 그리드중심 x,y좌표 추출
y <- coordinates(kde_hot_sp)[,2]

## bbox로 l1~l4까지 외곽끝점을 나타내는 좌표 4개 추출, 약간의 여유를 주고자 0.1% 추가함
l1 <- bbox(kde_hot_sp)[1,1] - (bbox(kde_hot_sp)[1,1] * 0.0001)
l2 <- bbox(kde_hot_sp)[1,2] + (bbox(kde_hot_sp)[1,2] * 0.0001)
l3 <- bbox(kde_hot_sp)[2,1] - (bbox(kde_hot_sp)[2,1] * 0.0001)
l4 <- bbox(kde_hot_sp)[2,2] + (bbox(kde_hot_sp)[2,2] * 0.0001)

library(spatstat)
win <- owin(xrange = c(l1, l2), yrange = c(l3, l4))
plot(win)

rm(list = c("kde_hot_sp","apt_price","l1","l2","l3","l4"))
## 밀도그래프 표시 데이터가 집중된 곳 찾기. 커널 밀도 추정
p <- ppp(x,y, window = win)   #경계창 위에 좌표값 포인트 생성
head(kde_hot,2)
str(p,2)
d <- density.ppp(p, weights = kde_hot$diff,  # 커널 밀도함수로 변환
                 sigma = bw.diggle(p),
                 kernel = 'gaussian')
plot(d)
head(kde_hot,2)

## 픽셀 이미지를 래스터 이미지로 변환
quantile(d) 
d[d<quantile(d)[4] + (quantile(d)[4]*0.1)] <- NA  #하위 75%를 NA처리

library(raster)
raster_hot <- raster(d)   #래스터 변환
plot(raster_hot)

## 클리핑, 불필요한 부분 자르기
bnd <- st_read("Data_s/sigun_bnd/seoul.shp")  # 서울시 경계선만 그리는 데이터 불러오기
raster_hot <- crop(raster_hot, extent(bnd))   # 외곽선 자르기
crs(raster_hot) <- sp::CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")   # 좌표계 정의, 띄어쓰기 중요
plot(raster_hot)   #지도 확인
plot(bnd, col=NA, border = "red", add=TRUE)

## 지도 그리기
library(rgdal)  
library(leaflet)
leaflet() %>% 
  addProviderTiles(providers$CartoDB.Positron) %>% 
  addPolygons(data = bnd, weight = 3, color = "red", fill = NA) %>% 
  addRasterImage(raster_hot, 
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_high), 
                                       na.color = "transparent"),
                 opacity = 0.4)
save(raster_hot, file = "Data_s/07_map/07_kde_hot.rdata")

