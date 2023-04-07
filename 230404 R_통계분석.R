##### 8.

setwd("C:/R_workspace")
##### 2) 확률 밀도 함수 표현하기

load("Data_s/08_chart/all.rdata")
load("Data_s/08_chart/sel.rdata")
head(all,2)
head(sel,2)

density(all$py) # density: 확률밀도함수로 만들어줌. y축은 상대도수, 전체면적 1로 두고 해당구간 발생할 확률(확률밀도값)
hist(all$py)    # histogram: y축은 빈도수
max_all <- density(all$py)  
max_sel <- density(sel$py) 

max_all
head(max_all,2)
max_all <- max(max_all$y)
max_all    #max_all의 y값 중 최대값
max_sel <- max(max_sel$y)
max_sel    #max_sel의 y값 중 최대값

plot_high <- max(max_all, max_sel)   #y축의 최대값, 둘중 더 큰 값

avg_all <- mean(all$py)    # 전체 지역 평당 평균가
avg_sel <- mean(sel$py)    # 관심 지역 평당 평균가
avg_all; avg_sel; plot_high

# 확률밀도함수그리기
plot(stats::density(all$py), ylim=c(0, plot_high), col = "blue", 
     lwd = 3, # 선의 굵기
     main = NA)
abline(v = mean(all$py), lwd = 2, col= "blue", lty = 2)   # 전체지역 평균, 수직선 그리기, lty =2 파선

text(avg_all + (avg_all) *0.15, plot_high * 0.1,
     sprintf("%.0f",avg_all), srt = 0.2, col = "blue")   # 전체지역 평균 텍스트 입력
lines(stats:: density(sel$py), col = "red", lwd = 3)    #  관심지역 확률밀도함수
abline(v = avg_sel, lwd = 2, col = "red", lty = 2)      #  관심지역 평균 수직선
text(avg_sel + (avg_sel) *0.15, plot_high * 0.1,
     sprintf("%.0f",avg_sel), srt = 0.2, col = "red")   # 관심지역 평균 텍스트 입력


# ------------------------------------------
##### 8-3) 회귀분석
library(dplyr)
library(lubridate)

# 월별 거래가 요약
all <- all %>% 
  group_by(month = floor_date(ymd, "month")) %>% 
  summarize(all_py = mean(py))   # 전체지역 카운팅
sel <- sel %>% 
  group_by(month = floor_date(ymd, "month")) %>% 
  summarize(sel_py = mean(py))   # 관심지역 카운팅
head(all,2)
head(sel,2)

plot(all)
plot(sel)

# 회귀식 모델링
## 독립변수: 월, 종속변수: 평당 평균가격
all$month; all$all_py

fit_all <- lm(all$all_py ~ all$month)  # 전체지역 회귀식
fit_sel <- lm(sel$sel_py ~ sel$month)  # 전체지역 회귀식
 
fit_all$coefficients[2]

summary(fit_all)
summary(fit_sel)

summary(fit_all)$coefficients
summary(fit_all)$coefficients[1]
summary(fit_all)$coefficients[2]

coef_all <- round(summary(fit_all)$coefficients[2],1) * 365   
coef_sel <- round(summary(fit_sel)$coefficients[2],1) * 365
coef_all  ## 365를 곱하는 이유????
# 계수: 1달 지날 때 평균가격 상승분, 일 단위로 얼마나 증가하는지를 나타냄. 일 단위로 계수를 나타내기 위해 365를 곱해줌. 회귀계수가 0.1이라면, 한달 지날 때마다 3.65 증가함 ????
# 독립변수(월)는 1~12월, 종속변수(평당가)는 평당 4000~12000원
# 단위 스케일링 필요함
a = list()
for (i in 12){
  a[i] = all$all_py[i+1] - all$all_py[i]
  i = i+1}
a

round(summary(fit_all)$coefficients[2],1)
round(summary(fit_sel)$coefficients[2],1)

mean(all$all_py)
sel$sel_py
mean(sel$sel_py)

## 회귀선 그리기(혼자)
plot(all$month,all$all_py,main="all")
abline(fit_all)

plot(sel$month,sel$sel_py,main="sel")
abline(fit_sel)

library(grid)
grob_1 <- grobTree(textGrob(paste0("전체 지역: ",coef_all, "만원(평당)"), x = 0.05, y = 0.88, hjust = 0, gp = gpar(col = "blue", fontsize = 13, fontface = "italic")))
grob_2 <- grobTree(textGrob(paste0("관심 지역: ",coef_sel, "만원(평당)"), x = 0.05, y = 0.95, hjust = 0, gp = gpar(col = "red", fontsize = 16, fontface = "bold")))


# 관심지역 월별 평균가격 그래프 그리기
install.packages("ggpmisc")
library(ggpmisc)
library(ggplot2)  
gg <- ggplot(sel, aes(x = month, y= sel_py))+
  geom_line() + xlab("month") + ylab("price") +
  theme(axis.text.x = element_text(angle = 90)) +
  stat_smooth(method = 'lm', color = 'dark grey', linetype = 'dashed') +
  theme_bw()

# 전체지역 월별 평균가격 그래프 그리기
gg + geom_line(data = all, aes(x = month, y = all_py), color = "blue", size = 1.5) +
  geom_line(color = "red", size = 1.5) +
  annotation_custom(grob_1) + 
  annotation_custom(grob_2)
gg

sel$floor %>% 
  as.numeric()

# ----------------------------------------
##### 8-4) 주성분분석

load("Data_s/08_chart/sel.rdata")  # 관심지역 데이터
head(sel,2)
pca_01 <- aggregate(list(sel$con_year,
                         sel$floor,
                         sel$py,
                         sel$area), 
                    by = list(sel$apt_nm), 
                    mean)
head(pca_01, 2)
colnames(pca_01) <- c("apt_nm","신축","층수","가격","면적")
m <- prcomp(~신축 + 층수 +가격+ 면적, data=pca_01, scale = T) # 주성분분석
summary(m)   # 주성분 1, 주성분2 만 사용해도 90%정도 설명 가능

# 그래프그리기
install.packages("ggfortify")
library(ggfortify)
autoplot(m, loadings.label = T, loadings.label.size = 6)+
  geom_label(aes(label=pca_01$apt_nm), size = 4)



#-------------------------------------------
##### 코드 정리
faithful <- faithful
head(faithful,2)
hist(faithful$waiting)   # histogram
plot(density(faithful$waiting))   # density function

mpg <- mpg
head(mpg,2)
mpg_lm <- lm(mpg$cty ~ mpg$displ)
mpg_lm
ggplot(mpg, aes(x = displ, y = cty)) +
  geom_point() +
  stat_smooth(method = 'lm', color = 'red', linetype = 'dashed')

library(ggfortify)
df <- iris[1:4]
head(df)
pca <- prcomp(df, scale. = TRUE)
pca
autoplot(pca, data = iris, color = "Species", loadings.label = T, loadings.label.size = 3)
