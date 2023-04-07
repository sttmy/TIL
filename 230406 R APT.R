##### 12. 아파트가격 상관관계 분석

##### 12-1) 평수 및 아파트가격 상관관계 분석하기
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
head(apt_price)


f <- lm(apt_price$py~ apt_price$py_area)
summary(f)
summary(f)$coefficients
c <- cor(apt_price$py, apt_price$py_area)
c
plot(apt_price$py_area,apt_price$py)
abline(f, col = "red")


# UI 만들기
ui <- fluidPage(
  #---# 제목
  titlePanel("Correlation of apartment prices"),
  #---# 사이드패널
  sidebarPanel(
    #---# 선택메뉴1:지역
    selectInput(
      inputId = "sel_gu",   #입력아이디
      label = "Select area",
      choices = unique(apt_price$addr_1),
      selected = unique(apt_price$addr_1)[1]),  #기본지역선택
    #---# 선택메뉴2: 크기(평)
    sliderInput(
      inputId = "range_py", #입력아이디
      label = "area",
      min = 0,
      max = max(apt_price$py_area),
      value = c(0,30)),
    #---# 선택메뉴3: x축
    selectInput(
      inputId = "var_x",
      label = "Select variable of X-axis",
      choices = list(
        "매매가(평당)" = "py",
        "크기(평)" = "py_area",
        "건축연도" = "con_year",
        "층수" = "floor"),
      selected = "py_area"),   # 기본선택
    #---# 선택메뉴4: y축
    selectInput(
      inputId = "var_y",
      label = "Select variable of Y-axis",
      choices = list(
        "매매가(평당)" = "py",
        "크기(평)" = "py_area",
        "건축연도" = "con_year",
        "층수" = "floor"),
      selected = "py"),    # 기본선택
    #---# 체크박스1: 상관계수
    checkboxInput(
      inputId = "corr_checked",
      label = strong("Correlation coefficient"),
      value = TRUE),
    #---# 체크박스2: 회귀계수
    checkboxInput(
      inputId = "reg_checked",
      label = strong("Regression coefficient"),
      value = TRUE)
    ),
  #---# 메인 패널
  mainPanel(
    #---#
    h4("Plotting"),
    plotOutput("scatterPlot"),
    #---#
    h4("Correlation coefficient"),
    verbatimTextOutput("corr_coef"),
    #---#
    h4("Regression coefficient"),
    verbatimTextOutput("reg_fit")
  )
)

# server 만들기
server <- function(input, output, session) {
  #---# 반응식
  apt_sel = reactive({
    apt_sel = subset(apt_price,
                     addr_1 == input$sel_gu &
                       py_area >= input$range_py[1] & 
                       py_area <= input$range_py[2])
    return(apt_sel)
  })
  #---# 플롯
  output$scatterPlot <- renderPlot({
    var_name_x <- as.character(input$var_x)
    var_name_y <- as.character(input$var_y)
    #---# 회귀선 그리기
    plot(
      apt_sel()[,input$var_x],
      apt_sel()[,input$var_y],
      xlab = var_name_x,
      ylab = var_name_y,
      main = "Plotting")
    fit <- lm(apt_sel()[, input$var_y] ~ apt_sel()[, input$var_x])
    abline(fit, col = "red")
  })
  #---# 상관계수
  output$corr_coef <- renderText({
    if(input$corr_checked){   # 체크박스1 확인
      cor(apt_sel()[,input$var_x],
          apt_sel()[,input$var_y])
    }
  })
  #---# 회귀계수
  output$reg_fit <- renderPrint({
    if(input$reg_checked){
      fit <- lm(apt_sel()[, input$var_y] ~ apt_sel()[, input$var_x])
      names(fit$coefficients) <- c("Intercept", input$var_x)  # 회귀계수 추출
      summary(fit)$coefficients # 회귀계수 요약
    }
  })
}

shinyApp(ui, server)


