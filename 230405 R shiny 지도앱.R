setwd("C:/R_workspace")

##### 10.데이터분석 앱 개발하기
##### 10-1) 반응형 지도 만들기
load("Data_s/06_geodataframe/06_apt_price.rdata")
load("Data_s/07_map/07_kde_high.rdata")   # 높은지역
load("Data_s/07_map/07_kde_hot.rdata")    # 급등지역
library(sf)
bnd <- st_read("Data_s/sigun_bnd/seoul.shp")  # 서울시경계선
grid <- st_read("Data_s/seoul/seoul.shp")  # 서울시 격자
load("Data_s/circle_marker.rdata")



### 하위 10%, 90%, 마커 클러스터링 설정
quantile(apt_price$py, probs = seq(.1,.9, by=.1))
pcnt_10 <- as.numeric(quantile(apt_price$py, probs = seq(.1,.9, by=.1))[1])
pcnt_90 <- as.numeric(quantile(apt_price$py, probs = seq(.1,.9, by=.1))[9])  
circle.colors <-sample(x = c("red","green",'blue'), size = 1000, replace = TRUE)


### 반응형지도 만들기
library(leaflet)
library(purrr)
library(raster)
leaflet() %>% 
  #---# 배경: 기본맵 설정: 오픈스트리트맵
  addTiles(options = providerTileOptions(minZoom = 9, maxZoom = 18)) %>% 
  #---# 최고가지역 KDE, 커널추정
  addRasterImage(raster_high,
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_high), na.color = "transparent"), opacity = 0.4, group = "2021최고가") %>% 
  
  #---# 급등지역 
  addRasterImage(raster_hot, 
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_hot), na.color = "transparent"), opacity = 0.4, group = "2021급등지") %>% 
  
  #---# 레이어 스위치, 선택 레이어
  addLayersControl(baseGroups = c("2021최고가", "2021급등지"), 
                   options = layersControlOptions(collapsed = FALSE)) %>% 
  
  #---# 서울시 외곽선
  addPolygons(data=bnd, weight=3, stroke = T, color = "red", fillOpacity = 0) %>% 
  
  #---# 마커 클러스터링
  addCircleMarkers(data = apt_price,
                   lng = unlist(map(apt_price$geometry,1)),
                   lat = unlist(map(apt_price$geometry,2)),
                   radius = 10,
                   stroke = FALSE,
                   fillOpacity = 0.5,
                   fillColor = circle.colors,
                   weight = apt_price$py,
                   clusterOptions = markerClusterOptions(iconCreateFunction =
                                                           JS(avg.formula))
                   )

#--------------------------------------------------
##### 10-2) 지도 어플리케이션 만들기
grid <- as(grid, "Spatial") # 그리드 불러오기
grid <- as(grid, "sfc")     # 변환
grid <- grid[which(sapply(st_contains(st_sf(grid),apt_price),length)>0)]  # 필터링
plot(grid)   # 그리드확인


### 반응형지도 모듈화하기
m <- leaflet() %>% 
  #---# 배경: 기본맵 설정: 오픈스트리트맵
  addTiles(options = providerTileOptions(minZoom = 9, maxZoom = 18)) %>% 
  #---# 최고가지역 KDE, 커널추정
  addRasterImage(raster_high,
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_high), na.color = "transparent"), opacity = 0.4, group = "2021최고가") %>% 
  
  #---# 급등지역 
  addRasterImage(raster_hot, 
                 colors = colorNumeric(c("blue","green","yellow","red"),
                                       values(raster_hot), na.color = "transparent"), opacity = 0.4, group = "2021급등지") %>% 
  
  #---# 레이어 스위치, 선택 레이어
  addLayersControl(baseGroups = c("2021최고가", "2021급등지"), 
                   options = layersControlOptions(collapsed = FALSE)) %>% 
  
  #---# 서울시 외곽선
  addPolygons(data=bnd, weight=3, stroke = T, color = "red", fillOpacity = 0) %>% 
  
  #---# 마커 클러스터링
  addCircleMarkers(data = apt_price,
                   lng = unlist(map(apt_price$geometry,1)),
                   lat = unlist(map(apt_price$geometry,2)),
                   radius = 10,
                   stroke = FALSE,
                   fillOpacity = 0.5,
                   fillColor = circle.colors,
                   weight = apt_price$py,
                   clusterOptions = markerClusterOptions(iconCreateFunction =
                                                           JS(avg.formula))) %>% 
  #---# 그리드
  leafem::addFeatures(st_sf(grid), layerId = ~seq_len(length(grid)), color = 'grey')
  
# install.packages("mapedit")
library(mapedit)
library(dplyr)
library(shiny)

# 샤이니로 구현
ui <- fluidPage(
  selectModUI("selectmap"), # 지도의 특정 지역을 선택할 수 있는 메소드. 그리드선택 모듈
  "선택은 할 수 있지만 아무런 반응이 없습니다")

server <- function(input, output){
  callModule(selectMod, "selectmap", m)}   # 모듈 서버 함수
  
shinyApp(ui, server)


### 반응식 추가
ui <- fluidPage(
  selectModUI("selectmap"), 
  textOutput('sel')
)

server <- function(input, output, session){
  df <- callModule(selectMod, "selectmap", m)   # 모듈 서버 함수
  output$sel <- renderPrint({df()[1]})
  }

shinyApp(ui, server)


#--------------------------------------------------
##### 10-3) 완성하기

library(DT)

ui <- fluidPage(
  #---# 상단화면: 지도+입력 슬라이더
  fluidRow(
    column(9, selectModUI("selectmap"), div(style = "height:45px")),
    column(3, 
           sliderInput("range_area","전용면적", sep = "", min=0, max=350, value=c(0,200)),
           sliderInput("range_time","건축연도", sep = "", min=1960, max=2020, value=c(1980,2020)), ),
    #---# 하단화면: 테이블 출력
    column(12, dataTableOutput(outputId="table"), div(style = "height:200px")))
  )


server <- function(input, output, session){
  #---# 반응식
  apt_sel = reactive({
    apt_sel = subset(apt_price, con_year >= input$range_time[1] & con_year <= input$range_time[2] & 
                       area >= input$range_area[1] & area <= input$range_area[2])
    return(apt_sel)
  })
  #---# 지도 입출력 모듈 설정
  g_sel <- callModule(selectMod, "selectmap", 
                      leaflet() %>% 
                        #---# 배경: 기본맵 설정: 오픈스트리트맵
                        addTiles(options = providerTileOptions(minZoom = 9, maxZoom = 18)) %>% 
                        #---# 최고가지역 KDE, 커널추정
                        addRasterImage(raster_high,
                                       colors = colorNumeric(c("blue","green","yellow","red"),
                                                             values(raster_high), na.color = "transparent"), opacity = 0.4, group = "2021최고가") %>% 
                        #---# 급등지역 
                        addRasterImage(raster_hot, 
                                       colors = colorNumeric(c("blue","green","yellow","red"),
                                                             values(raster_hot), na.color = "transparent"), opacity = 0.4, group = "2021급등지") %>% 
                        #---# 레이어 스위치, 선택 레이어
                        addLayersControl(baseGroups = c("2021최고가", "2021급등지"), 
                                         options = layersControlOptions(collapsed = FALSE)) %>% 
                        #---# 서울시 외곽선
                        addPolygons(data=bnd, weight=3, stroke = T, color = "red", fillOpacity = 0) %>% 
                        #---# 마커 클러스터링
                        addCircleMarkers(data = apt_price,
                                         lng = unlist(map(apt_price$geometry,1)),
                                         lat = unlist(map(apt_price$geometry,2)),
                                         radius = 10,
                                         stroke = FALSE,
                                         fillOpacity = 0.5,
                                         fillColor = circle.colors,
                                         weight = apt_price$py,
                                         clusterOptions = markerClusterOptions(iconCreateFunction=JS(avg.formula))) %>% 
                        #---# 그리드
                        leafem::addFeatures(st_sf(grid), layerId = ~seq_len(length(grid)), color = 'grey'))
  
  # 선택에 따른 반응결과 저장
  ## 반응초기값 설정
  rv <- reactiveValues(intersect= NULL, selectgrid = NULL)
  ## 반응결과 저장
  observe({
    gs <- g_sel()
    rv$selectgrid <- st_sf(grid[as.numeric(gs[which(gs$selected==TRUE), "id"])])
    if(length(rv$selectgrid)>0){
      rv$intersect <- st_intersects(rv$selectgrid, apt_sel())
      rv$sel <- st_drop_geometry(apt_price[apt_price[unlist(rv$intersect[1:10]),],])
    }else{
      rv$intersect <- NULL
      }
    })
  output$table <- DT::renderDataTable({
    dplyr::select(rv$sel, ymd, addr_1, apt_nm, price, area, floor, py) %>% 
      arrange(desc(py))},
    extensions ="Buttons", 
    options = list(dom = 'Bfrtip', scrollY = 300, scrollCollapse=T, paging= TRUE, buttons = c('excel'))
    )
}


#강사님
server <- function(input, output, session){
  #반응식
  apt_sel = reactive({
    apt_sel = subset(apt_price, con_year >= input$range_time[1]& con_year <= input$range_time[2] & area >= input$range_area[1] & area <=input$range_area[2])
    return(apt_sel)})
  
  # 지도 입출력 모듈 설정
  g_sel <- callModule(selectMod, 'selectmap',
                      leaflet() %>% 
                        addTiles(options = providerTileOptions(minZoom =9, maxZoom=18)) %>% 
                        # 최고가지역 KDE
                        addRasterImage(raster_high, 
                                       colors = colorNumeric(c("blue", "green", "yellow", "red"),
                                                             values(raster_high), na.color = "transparent"), opacity = 0.4,
                                       group = "2021 최고가") %>% 
                        addRasterImage(raster_hot, 
                                       colors = colorNumeric(c("blue", "green", "yellow", "red"),
                                                             values(raster_hot), na.color = "transparent"), opacity = 0.4,
                                       group = "2021 급등지") %>% 
                        addLayersControl(baseGroups = c("2021 최고가", "2021 급등지"),
                                         options = layersControlOptions(collapsed =FALSE)) %>% 
                        addPolygons(data=bnd, weight = 3, stroke = T, color = "red", fillOpacity = 0) %>% 
                        addCircleMarkers(data = apt_price, lng = unlist(map(apt_price$geometry, 1)),
                                         lat = unlist(map(apt_price$geometry, 2)), radius = 10, stroke = FALSE, fillOpacity = 0.6, fillColor = circle.colors, weight = apt_price$py,
                                         clusterOptions = markerClusterOptions(iconCreateFunction=JS(avg.formula))) %>% 
                        leafem::addFeatures(st_sf(grid), layerId= ~seq_len(length(grid)), color = 'grey'))
  # 선택에 따른 반응 결과 저장
  # 반응 초기값 설정
  rv <- reactiveValues(intersect=NULL, selectgrid= NULL)
  # 반응결과 저장
  observe({
    gs <- g_sel()
    rv$selectgrid <- st_sf(grid[as.numeric(gs[which(gs$selected==TRUE), "id"])])
    if(length(rv$selectgrid) > 0){
      rv$intersect <- st_intersects(rv$selectgrid, apt_sel())
      rv$sel      <- st_drop_geometry(apt_price[apt_price[unlist(rv$intersect[1:10]),],])
    }else{
      rv$intersect <- NULL
    }
  })
  output$table <- DT::renderDataTable({
    dplyr::select(rv$sel, ymd, addr_1, apt_nm, price, area, floor, py) %>% 
      arrange(desc(py))}, extensions = "Buttons", options = list(dom= 'Bfrtip', scrollY=300, scrollCollapse =T, paging=TRUE, buttons = c('excel')))
}

 

shinyApp(ui, server)







