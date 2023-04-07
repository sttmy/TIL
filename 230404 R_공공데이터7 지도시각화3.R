##### 7-3)우리 동네가 옆 동네보다 비쌀까?

rm(list= ls())
load("Data_s/06_geodataframe/06_apt_price.rdata")
load("Data_s/07_map/07_kde_high.rdata")
load("Data_s/07_map/07_kde_hot.rdata")

library(sf)
grid <- st_read("Data_s/seoul/seoul.shp")  # 서울시 1km 격자데이터
bnd <- st_read("Data_s/sigun_bnd/seoul.shp")  # 서울시 경계선만 

# 이상치설정 (평당 가격의 10%, 90% 지점)
quantile(apt_price$py, probs = seq(.1,.9, by = .1))         
quantile(apt_price$py)
pcnt_10 <- as.numeric(quantile(apt_price$py, probs = seq(.1,.9, by = .1))[1])
pcnt_90 <- as.numeric(quantile(apt_price$py, probs = seq(.1,.9, by = .1))[9])

load("Data_s/circle_marker.rdata")

# 마커 클러스터링 색상 설정 : 상, 중, 하
circle.colors <- sample(x = c("red","green","blue"), size = 1000, replace = TRUE)

# 마커 클러스터링 시각화
library(leaflet)
install.packages("purrr")
library(purrr)

leaflet() %>% 
  # 오픈스트리트맵 불러오기
  addTiles() %>%
  # 서울시 경계선 불러오기
  addPolygons(data = bnd, weight = 3, color = "red", fill = NA) %>% 
  # 최고가 래스터이미지 불러오기
  addRasterImage(raster_high, 
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_high), 
                                       na.color = "transparent"),
                 opacity = 0.4, group = "2021 최고가") %>% 
  # 급등지 래스터이미지 불러오기
  addRasterImage(raster_hot, 
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_hot), 
                                       na.color = "transparent"),
                 opacity = 0.4, group = "2021 급등지") %>% 
  # 최고가/급등지 선택 옵션 추가
  addLayersControl(baseGroups = c("2021 최고가","2021 급등지"),
                   options = layersControlOptions(collapsed = FALSE)) %>% 
  # 마커 클러스터링 불러오기
  addCircleMarkers(data = apt_price, 
                   lng = unlist(map(apt_price$geometry,1)), 
                   lat = unlist(map(apt_price$geometry,2)), 
                   radius = 10, 
                   stroke = FALSE,  # 경계 그릴건지 말건지
                   fillOpacity = 0.6, 
                   fillColor = circle.colors, weight = apt_price$py,
                   clusterOptions = markerClusterOptions(iconCreateFunction =
                                                           JS(avg.formula)))
  
#정리-----------------------------
# 포인트데이터 불러오기
library(spatstat) 
data(cells)
density(cells, 0.00001, at="points")
plot(cells)
rm(cells)

# 밀도데이터로 변환
d <- density.ppp(cells, 0.05) 
plot(d)
# 래스터로 변환
raster <- raster(d)
plot(raster)


