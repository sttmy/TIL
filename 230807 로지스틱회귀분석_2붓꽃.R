df <- read.csv('C:/R_workspace/Data/iris.csv')
head(df)
library(dplyr)
df <- df %>% select(-Name)
dim(df)
summary(df)

# 상관계수 행렬
(corrmatrix <- cor(df))

library(corrplot)
corrplot(cor(df), method = 'circle')

library(caret)
set.seed(123)

# 학습용 검증용 구분
idx_train <- createDataPartition(y=df$Species, p = 0.8, list=FALSE)
# list=False: 인덱스값 리스트 반환하지 않음
idx_train

train <- df[idx_train,]
x_train <- train[, -5]
y_train <- train[, 5]

test <- df[-idx_train,]
x_test <- test[, -5]
y_test <- test[, 5]

head(x_train)

library(nnet)
model <- multinom(Species~., data=train)
summary(model)

coef(model)

# 클래스로 출력
pred<-predict(model, newdata=x_test)
pred

mean(y_test == pred)

table(y_test,pred)


# 확률로 출력
pred_prob <- predict(model, newdata = x_test, type='probs')
pred_prob

result <- ifelse(pred_prob>0.5, 1, 0)
result

new_result <- c()
for (i in 1:nrow(result)){    # 행수
  for (j in 1:ncol(result)){    # 열수
    if(result[i,j]==1){
      new_result[i] <- j-1 # 품종이 0,1,2이므로 1을 뺌
    }
  }
}

y_test == new_result
mean(y_test == new_result)

table(y_test,new_result)
