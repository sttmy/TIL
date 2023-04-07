##### 13. 통계분석, 가설검정

# 유의확률(Significance probability, p-value)
# 실제로는 집단 간 차이가 없는데 우연히 차이가 있는 데이터가 추출될 확률분석 결과 유의확률이 크게 나타났다면 '집단 간 차이가 통계적으로 유의하지 않다'고 해석. 실제로 차이가 없더라도 우연에 의해 이 정도의 차이가 관찰될 가능성이 크다는 의미
# 분석 결과 유의확률이 작게 나타났다면, '집단 간 차이가 통계적으로 유의하다'고 해석. 실제로 차이가 없는데 우연히 차이가 발생, 이 정도의 차이가 관찰될 가능성이 작다, 우연이라고 보기 힘들다는 의미

library(ggplot2)
library(dplyr)
# t-test 

mpg1 <- as.data.frame(mpg)
View(mpg1)
mpg <- as.data.frame(ggplot2::mpg)
View(mpg)
str(mpg)
summary(mpg)
head(mpg)

## compact, suv 도시연비(cty)가 차이가 있는지 검증: t-test
table(mpg$class)
mpg_diff <- mpg %>% 
  select(class, cty) %>% 
  filter(class %in% c("compact","suv"))

table(mpg_diff)
table(mpg_diff$class)

# t-test
t.test(data = mpg_diff, cty~class, 
       var.equal = T)   # var.equal: 집단 간 분산 같음을 가정
# p-value < 0.05, reject H0, 차종간 연비차이가 있다


## 일반휘발유, 고급휘발유, 도시연비(cty) t검정
table(mpg$fl)
mpg_diff2 <- mpg %>% 
  select(fl, cty) %>% 
  filter(fl %in% c('r','p'))   #Regular, Premium
table(mpg_diff2$fl)
t.test(data = mpg_diff2, cty~fl, 
       var.equal = T)   # var.equal: 집단 간 분산 같음을 가정
# p-value > 0.05, do not reject H0, 휘발유 간 연비 차이가 없다


##### 상관관계 분석
eco <- as.data.frame(economics)
eco1 <- as.data.frame(ggplot2::economics)
head(eco)
str(eco)

## 실업률, 개인소득 간 상관관계
cor.test(eco$unemploy, eco$pce)   # p-value < 0.05, reject H0, 통계적으로 유의하다.significant

#히트맵만들기
mtcars   #내장데이터
head(mtcars)
car_cor <- cor(mtcars)

# 히트맵 패키지 
install.packages("corrplot")
library(corrplot)
corrplot(car_cor)
corrplot(car_cor, method = "number")

col <- colorRampPalette(c("#BB4444", "#EE9988",
                          "#FFFFFF","#77AADD", "#4477AA"))
corrplot(car_cor, method = 'color',
         col = col(200), # 색상 200개 선정
         type = "lower", # 대각선 기준으로 반쪽만 보면 됨
         order = 'hclust', # 유사한 상관관계끼리 군집화
         addCoef.col = "black",  # 상관계수 표시 색
         tl.col = "black",   # 변수명 색
         tl.srt = 45,   # 수직 글씨 각도 변경
         diag = F,    # 대각행렬 없애기
         )

corrplot(car_cor, method = 'color',
         col = col(200), # 색상 200개 선정
         type = "lower", # 대각선 기준으로 반쪽만 보면 됨
         addCoef.col = "black"  # 상관계수 표시 색
         )



##### Markdown

# 보고서 형태로 저장
# New file > R Mark down > HTML > 저장
# 튜토리얼: rmarkdown.rstudio.com