
######### 인공신경망
##### 1) 붓꽃 품종 분류 : nnet (히든레이어 1개)
df <- read.csv('C:/R_workspace/Data/iris.csv')
head(df)
tail(df)

library(dplyr)

# 필드 제거
df<-df %>% select(-Name)
# 입력데이터 방향 선택 (-:제외 +:추가)
# %>% 파이프연산자 : 파이프를 통과하는 것처럼 함수를 명시해줌

# Species변수타입: int를 factor로 변경   ::::: 매우 중요! 
str(df)
df$Species <- as.factor(df$Species)
str(df)

dim(df)
summary(df)

# 상관계수행렬
corrmatrix <- cor(df[1:4])
corrmatrix
(corrmatrix <- cor(df[1:4]))   # 괄호: 연산 후 출력을 바로 해 줌

library(corrplot)
corrplot(cor(df[1:4]), method='circle')
win.graph();corrplot(cor(df[1:4]), method='circle')  
# win.graph();  별도 창 띄워 실행

install.packages('caret')
library(caret)

# random seed 고정
set.seed(123)
# 학습용: 검증용 8:2로 구분
# list = False, 인덱스값의 리스트를 반환하지 않음
idx_train <- createDataPartition(y=df$Species, p = 0.8, list=FALSE)
idx_train

# 학습용
train <- df[idx_train,]  # R의 인덱스는 1부터
x_train <- train[,-5]    # 5번필드제외
y_train <- train[,5]     # 5번필드만

# 검증용
test <- df[-idx_train,]
x_test <- test[,-5]
y_test <- test[,5]

head(x_train)
head(y_train)

library(nnet)

# 학습용 데이터를 이용해 신경망 모형 생성
# nnet(종속변수 ~ 독립변수), hidden layer 1개
# size 은닉노드의 개수

model <- nnet(Species ~ ., data=train, size=10)
  # nnet(결과~원인)   필드명:a+b+c+d size=10 : hidden layer의 노드수
  # nnet(종속~독립)   . 전체
summary(model)
# 결과: a 4-10-3 network with 83 weights 
    # 입력-은닉-출력 노드수 with 가중치수
# 입력노드수는 독립변수의 개수로 설정됨

# 신경망모형에 대한 다양한 정보들
names(model)

# 최적의 가중치 집합
head(model$wts)

library(devtools)
source_url('https://gist.githubusercontent.com/Peque/41a9e20d6687f2f3108d/raw/85e14f3a292e126f1454864427e3a189c2fe33f3/nnet_plot_update.r')
win.graph(); plot.nnet(model)

# 신경망 모형의 검증(학습용 데이터)
# predict(신경망모델, 데이터셋)
pred <- predict(model, x_train, type = 'class')

# 예측결과가 벡터의 형태로 리턴됨
# 오분류표 생성 confusion matrix
# table(실제결과, 예측결과): 실제결과와 예측결과에 대한 교차표 작성
# result <- ifelse(pred>0.5, 1, 0)

table(y_train, pred)
mean(y_train==pred)

# 신경망 모형의 검증(검증용 데이터)
# predict(신경망모델, 데이터셋)
pred <- predict(model, x_test, type = 'class')
# result <- ifelse(pred>0.5, 1, 0)
table(y_test, pred)
mean(y_test==pred)


