##### 회귀 neuralnet

df <- read.csv('C:/R_workspace/Data/ozone2.csv')
head(df)

library(dplyr)
df <- df %>% select(-Month, -Day, -Result)
head(df)

library(caret)
set.seed(123)
(idx_train <- createDataPartition(y=df$Ozone, p=0.8, list=FALSE))
# list = 결과를 리스트로 반환할지, 행렬로 둘지
# list = FALSE : 리스트로 반환하지 않음

train <- df[idx_train,]
x_train <- train[,-dim(train)[2]]
y_train <- train[,dim(train)[2]]

test <- df[-idx_train,]
x_test <- test[,-dim(train)[2]]
y_test <- test[,dim(train)[2]]

library(neuralnet)
set.seed(123)
model <- neuralnet(Ozone ~ ., data=train, hidden=10, threshold=0.05, stepmax = 1e7)
win.graph();plot(model)

pred <- predict(model, x_test)
pred
mean((y_test-pred)^2)
