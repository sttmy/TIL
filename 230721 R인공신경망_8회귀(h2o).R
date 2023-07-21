##### 회귀분석(h2o)

df <- read.csv('C:/R_workspace/Data/ozone2.csv')
head(df)

library(dplyr)
df <- df %>% select(-Result, -Month, -Day)
head(df)

library(caret)
set.seed(123)
idx_train <- createDataPartition(y = df$Ozone, p=0.8, list = F)
train <- df[idx_train,]
head(train)
dim(train)[2]
x_train <- train[,-dim(train)[2]]
y_train <- train[,dim(train)[2]]
test <- df[-idx_train,]
x_test <- test[,-dim(train)[2]]
y_test <- test[,dim(train)[2]]
head(x_train)
head(y_train)


library(h2o)
h2o.init()
set.seed(123)
tr_data <- as.h2o(train)
te_data <- as.h2o(test)

target <- 'Ozone'
features <- names(train)[1:4]
model <- h2o.deeplearning(x = features, y = target, training_frame = tr_data, ignore_const_cols = FALSE, hidden = c(8,7,5,5))
summary(model)

# 예측값
pred <- h2o.predict(model, te_data)
pred

# MSE
perf <- h2o.performance(model, newdata = te_data)
perf

# H2ORegressionMetrics: deeplearning
# MSE:  270.5656   
# RMSE:  16.44888
# MAE:  12.20236   평균절대오차
# RMSLE:  0.6822756
# Mean Residual Deviance :  270.5656

h2o.mse(perf)



##### 날짜데이터 처리
# 월: 범주형으로 처리하거나
# 기준일을 정해서, 며칠이 지났는지 추가
# 요일 기준으로 정리
# 1년 중 몇주차
# 주말/평일
# 시계열데이터 time series로 처리
