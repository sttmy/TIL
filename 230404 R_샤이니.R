##### 9.샤이니
# 웹에서 배포, 웹 서비스 만들어보기
# 데이터분석 결과를 앱으로 만드는 개발 도구

#---------------------
library(shiny)
ui <- fluidPage("사용자 인터페이스")   # 사용자 인터페이스
server <- function(input, output, session){}   # 서버
shinyApp(ui, server) # 실행

# 127.0.0: 집 / :6467 문
# open in browser 확인해볼 수 있음

# 샤이니 샘플 확인
runExample()
runExample("01_hello")
runExample("02_text")
runExample("03_reactivity")
runExample("04_mpg")       # global
runExample("05_sliders")   # slider bars
runExample("06_tabsets")   # tabbed panels
runExample("07_widgets")   # help text and submit buttons
runExample("08_html")      # shiny app built from html
runExample("09_upload")   # file download wizard
runExample("10_download") # file download wizard
runExample("11_timer")    # an automated timer


faithful <- faithful  # Yellow stone park, geyser data
head(faithful)

# hello 샘플, UI
ui <- fluidPage(
  titlePanel("샤이니 1번 샘플"),
  sidebarLayout(
    sidebarPanel(
      sliderInput(inputId = "bins",
                  label = "막대(bin) 개수: ",
                  min = 1, max = 50,
                  value = 30)),
    mainPanel(      # 메인패널
      plotOutput(outputId = "distPlot")   # 차트출력
      )
  )
)

# hello 샘플, server
server <- function(input, output, session){
  output$distPlot <- renderPlot({
    # 분출대기시간 정보, x변수로 저장
    x <- faithful$waiting   
    #히스토그램 구간설정
    bins <- seq(min(x), max(x), length.out = input$bins + 1) 
    # 히스토그램 그리기
    hist(x, breaks = bins, col = "#75AADB", border = "white", 
         xlab = "다음 분출때까지 대기시간(분)",
         main = "대기시간 히스토그램")
  })
}

# hello 샘플, 실행
shinyApp(ui, server)

#--------------------------------------------------------
##### 9-2) 입력과 출력하기
ui <- fluidPage(
  sliderInput("range","연비", min=0, max=35, value=c(0,10))) # 입력받기
server <- function(input, output, session) {}  
shinyApp(ui, server)
# server, {} output을 정의하지 않아서 반응이 없음

# output정의하기
ui <- fluidPage(
  sliderInput("range","연비", min=0, max=35, value=c(0,10)),
  textOutput("value"))   # 결과값 출력
server <- function(input, output, session) {
  output$value <- renderText(input$range[1] + input$range[2])  # 입력값 계산
} 
shinyApp(ui, server)

# 랜더링이 안된다면? ('render'삭제) > 오류발생
ui <- fluidPage(
  sliderInput("range","연비", min=0, max=35, value=c(0,10)),
  textOutput("value"))   # 결과값 출력
server <- function(input, output, session) {
  output$value <- Text(input$range[1] + input$range[2])  # 입력값 계산
} 
shinyApp(ui, server)

#--------------------------------------------------------
##### 9-3) 반응형 웹 앱
install.packages("DT")
library(DT)
datatable(iris)
library(ggplot2)
mpg <- mpg
head(mpg,3)

# table이 검색될 수 있도록 웹 앱을 만들어보기
library(shiny)
ui <- fluidPage(
  sliderInput("range","연비",min=0, max=35, value=c(0,10)), # 데이터입력
  DT::dataTableOutput("table")  # 출력
)
server <- function(input, output, session) {
  # 반응식
  cty_sel <- reactive({
    cty_sel = subset(mpg, cty >= input$range[1] & cty <= input$range[2])
    return(cty_sel)})
  # 반응 결과 랜더링
  output$table <- DT::renderDataTable(cty_sel())
  }

shinyApp(ui, server)  

##-------------------------------------------
ui라고 말하는 화면은 실제로 사용자가 보는 화면을 뜻합니다. shiny에서는 크게 titlePanel과 sidebarPanel, mainPanal의 세 가지

shiny의 입출력: shiny는 다른 R 패키지와는 다르게 강제하는 변수가 3개, input, output, session 가 있습니다. 각각 객체로써 존재하고 이번에는 input과 output으로 데이터를 ui와 server가 교환하는 방법을 소개하겠습니다. 각각의 객체는 *Input 함수와 *Output 함수로 데이터를 입력 받아 저장합니다. *Output 함수는 render* 함수로 선언됩니다.

shiny는 웹 기술을 R로 사용할 수 있게 만드는 덕분에 render라는 과정이 필요합니다. 그래서 render 환경에서 변수들이 관리되어야 합니다. 입출력은 input 변수와 output 변수로 관리합니다. 이 두 가지는 render 밖에서 관리되는 변수로 다르게 취급해야 합니다.

- output 변수는 list라고 이해하시면 좋을 것 같습니다. list인 output 변수는 output$뒤에 변수명을 작성함으로써 output 객체에 필요한 결과물을 전달합니다. 만약에 화면에 보여줘야할 것의 이름을 sample이라고 하면 output$sample에 필요한 내용을 선언하는 것으로 진행합니다.
# (server쪽 코드) output$sample <- randerPlot({ ...plot()... })
- plot함수로 만들어지는 이미지를 output$sample에 저장하는 것을 뜻합니다. 

- ui쪽에서 이걸 어디에다 위치하게 하는지를 결정하는 함수에서 사용할 수 있습니다. 이때는 plotOutput 함수를 사용합니다.
# (ui쪽 코드) plotOutput("sample")
- 함수명이 Output 이고, "로 변수명을 감싸며, output$ 문법을 사용하지 않고 컬럼명인 sample만 사용한다는 점을 주목해 주세요. server쪽 코드에서 output$에 컬럼명의 형태로 저장한 R의 결과물을 ui쪽 코드에서 *Output 함수에서 "로 감싼 글자의 형태로 컬럼명만 작성해서 사용

- render*({ }) 함수 안에는 plot 함수가 R 문법으로 작성되어 있습니다. 그리고 render*({ })의 특이한 점은 () 안에 {}가 또 있다는 점입니다. 여기서는 ({ }) 안쪽은 R의 세계이고, 그 바깥은 웹의 세계라고 이해
# (server쪽 코드) output$sample <- randerPlot({
# data <- faithful[faithful$eruptions >3, ]
# plot(data)
# })

intput$은 output$과 같이 웹의 세계에 있는 변수입니다. 그래서 *Input() 함수들을 통해서 input$의 컬럼 이름으로 웹 페이지 내에서 얻을 수 있는 데이터를 R의 세계에서 사용할 수 있게 해줍니다. 우선 input$에 웹의 세계의 데이터를 R의 세계로 가져와 보겠습니다.

# (ui쪽 코드) sliderInput("sdata1", "슬라이더 입력:", min=50, max=150, value=100)
위의 코드는 sliderInput()이라는 *Input() 패밀리 함수를 통해서 input$sdata1이라는 곳에 웹 데이터를 저장하는 것을 뜻합니다. *Input() 패밀리 함수는 같은 규칙을 가지는데 
입력형태명Input()의 함수명을 가지고, 첫번째 인자는 input$ 뒤로 붙을 컬럼명, 두번째 인자는 화면에 보여줄 글자를 의미합니다. 나머지 인자는 입력형태에 따라 다양하게 달라집니다. 

이제 input하나를 받고 output 하나를 출력하는 shiny 앱을 작성할 준비가 되었습니다



#------------------------------------------------------------
##### 9-4) 레이아웃
ui <- fluidPage(
  fluidRow(
    # 첫번째 열: 빨강 박스로 높이 450, 픽셀, 폭 9
    column(9, div(style = "height:450px;border: 4px solid red;", "폭 9")),
    # 두번째 열: 보라 박스로 높이 450, 픽셀, 폭 3
    column(3, div(style = "height:450px;border: 4px solid purple;", "폭 3")),
    # 세번째 열: 빨강 박스로 높이 450, 픽셀, 폭 9
    column(12, div(style = "height:400px;border: 4px solid blue;", "폭 12"))
  )
)

server <- function(input, output, session) {}

shinyApp(ui, server)

# 탭 페이지 추가하기

ui <- fluidPage(
  fluidRow(
    # 첫번째 열: 빨강 박스로 높이 450, 픽셀, 폭 9
    column(9, div(style = "height:450px;border: 4px solid green;", "폭 9")),
    # 두번째 열: 보라 박스로 높이 450, 픽셀, 폭 3
    column(3, div(style = "height:450px;border: 4px solid purple;", "폭 3")),
    # 탭 패널 1~2번 추가
    tabsetPanel(
      tabPanel("탭1",
               column(4, div(style = "height:300px;border: 4px solid red;", "폭 4")),
               column(4, div(style = "height:300px;border: 4px solid yellow;", "폭 4")),
               column(4, div(style = "height:300px;border: 4px solid red;", "폭 4"))),
      tabPanel("탭2", div(style = "height:300px;border: 4px solid blue;", "폭 12")))
  )
)

server <- function(input, output, session) {}

shinyApp(ui, server)

