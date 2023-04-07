##### 8. 그래프 만들기

library(ggplot2)
mpg <- as.data.frame(ggplot2::mpg)
table(mpg$displ)
summary(mpg)
View(mpg)
boxplot(mpg$displ)$stat

##### 산점도 : geom_point()
# x축 displ, y축 hwy
ggplot(data = mpg, aes(x = displ, y = hwy)) +
  geom_point() + xlim(3,6) + ylim(10,30)


##### 혼자서해보기 p13  (책 p188)
# Q1. mpg 데이터의 cty(도시 연비)와 hwy(고속도로 연비) 간에 어떤 관계가 있는지 알아보려고 함. x 축은 cty, y 축은 hwy 로 된 산점도를 만들어 보기
ggplot(data = mpg, aes(x = cty, y = hwy)) +
  geom_point()

# Q2. 미국 지역별 인구통계 정보를 담은 ggplot2 패키지의 midwest 데이터를 이용해서 전체 인구와 아시아인 인구 간에 어떤 관계가 있는지 알아보려고 합니다. x 축은 poptotal(전체 인구), y 축은 popasian(아시아인 인구)으로 된 산점도를 만들어 보세요. 전체 인구는 50 만 명 이하, 아시아인 인구는 1 만 명 이하인 지역만 산점도에 표시되게 설정하세요
midwest <- as.data.frame(ggplot2::midwest)
boxplot(midwest$poptotal)$stat
boxplot(midwest$popasian)$stat
ggplot(data = midwest, aes(x = poptotal, y = popasian)) +
  geom_point() +
  xlim(0, 500000) +
  ylim(0, 10000)

table(is.na(midwest$poptotal))
table(is.na(midwest$popasian))


##### 막대그래프: geom_col() / geom_bar()
# 평균표를 이용해 그래프 생성 - geom_col()
# 별도로 표를 만들지 않고 원 자료를 이용해 바로 그래프 생성 - geom_bar()


library(dplyr)
df_mpg <- mpg %>%
  group_by(drv) %>%
  summarise(mean_hwy = mean(hwy))
ggplot(data = df_mpg, aes(x = drv, y = mean_hwy)) +
  geom_col()
ggplot(data = df_mpg, aes(x = reorder(drv, -mean_hwy), y = mean_hwy)) +
  geom_col()

ggplot(data = mpg, aes(x = drv)) + geom_bar()
ggplot(data = mpg, aes(x = hwy)) + geom_bar()


##### 혼자서해보기 p25
# Q1. 어떤 회사에서 생산한 "suv" 차종의 도시 연비가 높은지 알아보려고 합니다. "suv" 차종을 대상으로 평균 cty(도시 연비)가 가장 높은 회사 다섯 곳을 막대 그래프로 표현해 보세요. 막대는 연비 가 높은 순으로 정렬하세요.
View(mpg)
mpg_df <- mpg %>%
  group_by(manufacturer) %>%
  summarise(mean_cty = mean(cty))
mpg %>% 
  filter(class == "suv")
  
ggplot(data = mpg, aes(x = reorder(manufacturer, -mean_cty), y = mean_cty ))

###tch
df <- mpg %>% 
  filter(class == "suv") %>% 
  group_by(manufacturer) %>% 
  summarise(mean_cty = mean(cty)) %>% 
  arrange(desc(mean_cty)) %>% 
  head(5)
df

ggplot(data = df, aes(x = reorder(manufacturer, -mean_cty), y = mean_cty )) + 
  geom_col()

# Q2. 자동차 중에서 어떤 class(자동차 종류)가 가장 많은지 알아보려고 합니다. 자동차 종류별 빈도를 표현한 막대 그래프를 만들어 보기
### tch
ggplot(data = mpg, aes(x = class)) +
  geom_bar()


##### 선 그래프: geom_line()

eco <- as.data.frame(ggplot2::economics)
View(eco)

ggplot(data = eco, aes(x = date, y = unemploy)) +
  geom_line()

#Q. psavert(개인 저축률)가 시간에 따라서 어떻게 변해왔는지 알아보려고 합니다. 시간에 따른 개인저축률의 변화를 나타낸 시계열 그래프를 만들어 보세요
ggplot(data = eco, aes(x = date, y = psavert)) +
  geom_line()


##### 박스플롯: geom_boxplot() 
ggplot(data = mpg, aes(x = drv, y = hwy)) +
  geom_boxplot()

###혼자서해보기
#Q1. class(자동차 종류)가 "compact", "subcompact", "suv"인 자동차의 cty(도시 연비)가 어떻게 다른지 비교해보려고 합니다. 세 차종의 cty를 나타낸 상자 그림을 만들어보세요

table(mpg$class)
comp <- mpg %>% 
  filter(class == c("compact",'subcompact','suv'))
ggplot(data = comp, aes(x = class, y = cty)) + 
  geom_boxplot()

###tch
comp <- mpg %>% 
  filter(class %n% c("compact",'subcompact','suv'))

