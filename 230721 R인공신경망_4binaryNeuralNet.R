##### 이진분류(neuralnet)

df<-read.csv("C:/R_workspace/Data/diabetes.csv")
head(df)

library(dplyr)

# 필드제거
df <- df %>% select(-target)
  # 원본 %>% 선택(-필드)  : 가공해라
df

# target값 확인
tbl <- table(df$target2)
tbl  # 불균형 데이터셋
win.graph(); barplot(tbl, beside = T, legend = T, col=rainbow(2))

# under sampling
install.packages("ROSE")
library(ROSE)

# method: under, over, both 
# N: 샘플링 후 샘플 개수(적은쪽 * 2) 또는 p=0.5 50:50 선택
df_samp <- ovun.sample(target2 ~ ., data=df, seed=1, method = 'under', N=min(tbl)*2)$data
          # 종속변수 ~ 독립변수 (.나머지 모든 것)
          # method: under 언더샘플링 / over 오버샘플링
          # N: 샘플수 적어줘야 함. (낮은쪽이 195)를 2세트로 만들어라
df_samp
# 참고: 오버샘플링 (모델이 과장될 우려가 있음)
df_samp_ov <- ovun.sample(target2 ~ ., data=df, seed=1, method = 'over', N=max(tb1)*2)$data
df_samp_ov


(tbl <- table(df_samp$target2))
library(caret)

set.seed(123)

# 학습용 : 검증용 = 8:2 구분
idx_train <- createDataPartition(y=df_samp$target2, p=0.8, list=FALSE)

train <- df_samp[idx_train, ]
x_train <- train[,-11]
y_train <- train[,11]

test <- df_samp[-idx_train, ]
x_test <- test[,-11]
y_test <- test[,11]

library(neuralnet)

# 모델만들기
set.seed(123)
model <- neuralnet(as.factor(target2) ~ ., data=train, hidden=c(10,10), linear.output = F)
  # 종속변수가 2개인 셈(as.factor(target2))
  # linear.output 회귀분석인 경우 T, 분류인 경우 F
win.graph(); plot(model)
model$result.matrix # 모델 가중치 정보

# 참고. 변수의 중요도 그래프는 출력층의 노드가 1개일 때만 출력 가능함
install.packages('NeuralNetTools')
library(NeuralNetTools)
model2 <- neuralnet(target2 ~ ., data=train, hidden=10, threshold=0.01, linear.output = F)
    # threshold : 에러의 감소분이 threshold 값보다 작으면 stop(학습중지기준)
win.graph(); garson(model2)
pred2<-compute(model2, X_test) # 세부적인 계산 결과
pred2

# 출력결과(확률)
pred<-predict(model, x_test, type='prob')
pred

# 각 샘플에 대해 0,1로 출력
# 0 열방향(세로), 1 행방향(가로)
result <- apply(pred, 1, function(x) which.max(x)-1)
  # 예측, 1값을 뽑아냄. x가 max인 값 (1,2)이므로 -1
result

table(y_test , result)
mean(y_test == result)

install.packages('Epi')
library(Epi)
win.graph(); ROC(test=result, stat=y_test, plot="ROC", AUC=T, main="신경망")
# ROC커브: 민감도 / 특이도
# AUC Area Under Curve 면적이 1에 가까울수록 성능이 좋은 모델임
# threshold 값에 따라서 변경될 수 있으므로, 여러가지 테스트
# 분류기의 판별기준을 높이거나 낮추면 다른 결과가 나올 수 있음