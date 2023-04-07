##### 12-2) 여러지역 상관관계 비교하기


##### 데이터 준비하기

getwd()
setwd("C:/R_workspace/Data_s")
load("./06_geodataframe/06_apt_price.rdata")
library(sf)
library(shiny)

# 글꼴
require(showtext) 
font_add_google(name = "Nanum Gothic", regular.wt = 400, bold.wt = 700)
showtext_auto()
showtext_opts(dpi=112)

# 데이터준비
apt_price <- st_drop_geometry(apt_price)
apt_price$py_area <- round(apt_price$area / 3.3, 0)  # 크기변환 m^2 > 평
head(apt_price$py_area)

##### 사용자화면 구현하기
library(ggpmisc)

ui <- fluidPage(
  #---# 타이틀입력
  titlePanel("Correlation comparison of several regions"),
  fluidRow(
    #---# 선택메뉴1: 지역선택
    column(6,
           selectInput(
             inputId = "region",
             label = "Select region",
             unique(apt_price$addr_1),
             multiple = TRUE)),
    #---# 선택메뉴2: 크기선택
    column(6,
           sliderInput(
             inputId = "range_py",
             label = "Select area",
             min = 0,
             max = max(apt_price$py_area),
             value = c(0,30))),
    #---# 출력
    column(12,
           plotOutput(outputId = "gu_Plot", height = "600"))
  )
)

server <- function(input, output, session){
  #---# 반응식 
  apt_sel = reactive({
    apt_sel = subset(apt_price,
                     addr_1 == unlist(strsplit(paste(input$region, collapse = ','),
                                               ",")) &
                       py_area >= input$range_py[1] &
                       py_area <= input$range_py[2])
    return(apt_sel)
  })
  #---# 지역별 회귀선 그리기
  output$gu_Plot <- renderPlot({
    if (nrow(apt_sel()) == 0)  # 선택 전 오류메시지 없애기
      return(NULL)
    ggplot(apt_sel(), aes(x = py_area, y = py, col = "red")) + # 축설정
      geom_point() +
      geom_smooth(method = "lm", col = "blue") + # 회귀선
      facet_wrap(~addr_1, scale = "free_y", ncol = 3) +   # 카테고리별 그리기
      theme(legend.position = "none") +
      xlab("크기(평)") +
      ylab("평당가격(만원)") +
      stat_poly_eq(aes(label = paste(..eq.label..)),
                   label.x = "right",
                   label.y = "top",
                   formula = y ~ x, parse = TRUE, 
                   size = 5, col = "black")
  })
}

shinyApp(ui, server)
