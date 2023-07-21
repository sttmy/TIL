##### Iris(h2o)

# install.packages('RCurl')
# install.packages('h2o')

library(h2o)


# h2o에 접속
localH2O = h2o.init()
train <- h2o.importFile('C:/R_workspace/Data/iris.csv')
test <- h2o.importFile('C:/R_workspace/Data/iris.csv')

train
x <- names(train)[1:4]
y <- names(train)[6]

train[,y] <- as.factor(train[,y])
test[,y] <- as.factor(test[,y])

iris_h2o <- as.h2o(iris, destination_fram = 'iris_h2o')
h2o.ls()

class(iris_h2o)
head(iris_h2o)
(n_rows <- nrow(iris_h2o))
(n_cols <- ncol(iris_h2o))
paste('행의 개수: ', n_rows)

set.seed(123)
train_idx <- sample(1:nrow(iris), size=0.8*nrow(iris), replace = FALSE)
          # sample(데이터, 샘플링사이즈, 중복여부)
          # 1:nrow(iris)  150개, 120개 골라라, 중복여부false 비복원
train_iris <- iris[train_idx,]
test_iris <- iris[-train_idx,]

# 품종별 비율
with(train_iris, prop.table(table(Species)))
with(test_iris, prop.table(table(Species)))

# h2o타입으로 변환
train_iris_h2o <- as.h2o(train_iris, 'train_iris_h2o')
test_iris_h2o <- as.h2o(test_iris, 'test_iris_h2o')

# 종속변수 이름
target <- 'Species'

# 독립변수들의 이름
features <- names(train_iris)[!names(train_iris) %in% target]
features


### 로지스틱 회귀분석 (출력결과: 분류)
glm_model <- h2o.glm(x=features, y=target, training_frame = train_iris_h2o, model_id = 'glm_model', family='multinomial')
        # family: multinomial 다분류  (ROC커브를 바로 도출 못함. 2개씩 고려)
summary(glm_model)

pred_iris_glm <- as.data.frame(h2o.predict(glm_model, newdata = test_iris_h2o))
# 예측값
test_iris$pred_glm <- pred_iris_glm$predict

# 오분류표 dnn (Dimension Names)
# with: 데이터프레임의 필드명으로 직접 접근할 수 있는 함수
with(test_iris, table(Species, pred_glm, dnn=c('Real', 'Predict')))


### 랜덤포레스트
rf_model <- h2o.randomForest(x = features, y = target, training_frame = train_iris_h2o, model_id = 'rf_model', ntrees=100)
    # ntrees: 트리 수
summary(rf_model)

pred_iris_rf <- as.data.frame(h2o.predict(rf_model, newdata = test_iris_h2o))
# 예측값
test_iris$pred_rf <- pred_iris_rf$predict

# 오분류표
with(test_iris, table(Species, pred_rf, dnn=c('Real', 'Predict')))
