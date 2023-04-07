#####  12.Interactive Graph

##### Plotly 패키지 사용
install.packages("plotly")
library(plotly)
library(ggplot2)
mpg
str(mpg)
p <- ggplot(data = mpg, aes(x = displ, y = hwy, col=drv)) + 
  geom_point()
ggplotly(p)

head(diamonds,5)
ggplotly(ggplot(data = diamonds, aes(x = cut, fill = clarity)) +
  geom_bar(position = 'dodge'))

### 이미지 Export > Save as Web Page > (name).html 웹페이지에 띄우기

##### 시계열그래프
install.packages("dygraphs")
library(dygraphs)
eco <- ggplot2::economics
head(eco)
summary(eco)
str(eco)

# 시간 순서 속성을 가지는 xts. 시계열 데이터 다루려면 필요
library(xts)
eco1 <- xts(eco$unemploy, order.by = eco$date)
head(eco1)
dygraph(eco1)

dygraph(eco1) %>% dyRangeSelector()

# 저축률 / 실업률
eco_a <- xts(eco$psavert, order.by = eco$date)
head(eco_a)
eco_b <- xts(eco$unemploy/1000, order.by = eco$date)
head(eco_b)

eco2 <- cbind(eco_a, eco_b)   # 컬럼기준으로 붙이기
head(eco2)

# xts는 컬럼명 바꿀 때 rename 말고 colnames()사용
colnames(eco2) <- c("psavert","unemploy")
head(eco2)

dygraph(eco2) %>% dyRangeSelector()
