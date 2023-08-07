df <- data.frame(x=seq(-5,5,length.out = 100))
df

df$y <- exp(df$x)/(1+exp(df$x))

plot(df,type='l')


df<-read.csv("c:/workspace/Data/ozone2.csv")

head(df)
tail(df)

library(dplyr)

# 필드 제거
df<-df %>% select(-Ozone,-Month,-Day)

#상관계수 행렬
(corrmatrix <- cor(df))

# 강한 양의 상관관계, 강한 음의 상관관계
corrmatrix[corrmatrix > 0.5 | corrmatrix < -0.5]

library(corrplot)
corrplot(cor(df), method="circle")

tbl<-table(df$Result)
tbl   # 불균형 데이터셋. ?
barplot(tbl, beside = TRUE, legend = TRUE, col = rainbow(2))

rainbow(7)


# under sampling
# install.packages("ROSE")
library(ROSE)
# method: under,over,both   N: 샘플링 후의 샘플 갯수(적은 쪽 x 2) 또는 p=0.5 50:50으로 선택

df_samp <- ovun.sample(Result ~ . , data = df, seed=1, method = "under", N=144)$data

tbl<-table(df_samp$Result)
tbl

library(caret)
#랜덤 시드 고정
set.seed(123)

# 학습용 검증용 데이터셋 구분
# list=FALSE, 인덱스값들의 리스트를 반환하지 않음
idx_train <- createDataPartition(y=df_samp$Result, p=0.8, list=FALSE)

#학습용
train <- df_samp[idx_train, ]
X_train <- train[, -4]
y_train <- train[, 4]

#검증용
test <- df_samp[-idx_train, ]
X_test <- test[, -4]
y_test <- test[, 4]

head(X_train)

head(y_train)


# 로지스틱 회귀모델
model <- glm(Result~., data=train)
summary(model)

# 회귀계수 확인
coef(model)    # 일조량, 온도: (+), 풍량: (-)

# 예측값을 0~1 사이로 설정
pred <- predict(model, newdata = X_test)
pred

result <- ifelse(pred>0.5, 1, 0)   # 0.5보다 크면 1, 아니면 0

# 예측정확도
mean(y_test == result)

# 오분류표
table(y_test, result)

# install.packages("ROCR")
library(ROCR)
pr <- prediction(pred, y_test)
pr
pr@predictions # 출력값

prf <- performance(pr, measure = 'tpr', x.measure='fpr')
win.graph();plot(prf, main='ROC curve')

# AUC (The Area Under an ROC Curve)
auc <- performance(pr, measure = "auc")
auc@y.values
auc@y.values[[1]]

