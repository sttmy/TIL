df<-read.csv("c:/R_workspace/Data/wine/wine_new.csv")
head(df)

library(dplyr)
df <- df %>% select(-quality)
summary(df)

cor(df)
library(corrplot)
corrplot(cor(df), method='circle')

tbl <- table(df$class)
tbl
barplot(tbl, beside=TRUE, legend=TRUE, col=rainbow(2))

# undersampling
library(ROSE)
df_samp <- ovun.sample(class~., data=df, seed=1, method='under', N=744*2)$data
tbl <- table(df_samp$class)
tbl

library(caret)
set.seed(123)

idx_train <- createDataPartition(y=df_samp$class, p=0.8, list=FALSE)
train <- df_samp[idx_train,]
x_train <- train[, -12]
y_train <- train[, 12]

#검증용
test <- df_samp[-idx_train, ]
x_test <- test[, -12]
y_test <- test[, 12]

# 모델
model <- glm(class~., data=train, family=binomial)
summary(model)
coef(model)

pred <- predict(model, newdata=x_test, type='response')
result <- ifelse(pred>0.5, 1, 0)
mean(y_test==result)
table(y_test, result)

# 후진제거법
reduced <- step(model, direction='backward')
#Deviance:이탈도
#AIC: Akaike 정보지수(Akaike information criterion)
#두 개의 수치가 모두 작을수록 좋은 모형
#첫번째 단계에서 pH 변수가 제거되었고
#Start: AIC=1196.94
#최종모형의 Step: AIC=1195.14로 감소됨
#최종 결과 확인
summary(reduced)

#회귀계수 확인
coef(reduced)

#예측값을 0~1 사이로 설정
pred <- predict(reduced, newdata=X_test, type='response')

#0.5보다 크면 1, 아니면 0으로 설정
result <- ifelse(pred>0.5,1,0)

#예측정확도
mean(y_test == result)

#오분류표 출력
table(y_test, result)



#### 전진선택법과 비교
biggest <- glm(class~., data=train, family=binomial)
smallest <- glm(class~1, train, family=binomial)

model1 <- step(biggest, direction='backward')
model2 <- step(smallest, direction='forward', scope=biggest)

summary(model1)
summary(model2)
