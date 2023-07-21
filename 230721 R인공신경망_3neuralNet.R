##### neuralnet : hidden layers 2개 이상 가능

install.packages('neuralnet')
library(neuralnet)

set.seed(100)
x <- as.matrix(sample(seq(-2,2,length=50), 50, replace = FALSE), ncol=1)
                # seq(from, to, 나누는수): -2부터 2까지 50등분
                # sample (데이터, 샘플링개수, replace)
                                # replace=TRUE 복원추출  FALSE 비복원추출
y <- x^2
win.graph(); plot(y~x)   # 2차함수 그래프

df <- as.data.frame(cbind(x,y))
colnames(df) <- c('x','y')
df

# 신경망 모형: neuralnet
nn <- neuralnet(y~x, data=df, hidden=c(10,10))
        # 결과~ 원인 / 종속~독립
        # hidden 은닉층 2개, 노드수 10개씩
win.graph(); plot(nn)  # 신경망그래프

test <- as.matrix(sample(seq(-2,2,length=10), 10, replace = FALSE), ncol=1)
pred <- predict(nn,test)
test^2   # 실제값
pred     # 예측값

# Mean Squared Error 평균제곱오차
mean((pred-test^2)^2)   # 평균((출력-실제)^2)
result <- cbind(test, test^2, pred)
colnames(result) <- c('test','test^2','pred')
result
