cost <- c(1800, 1500, 3000)
sale <- c(24, 38, 13)
product <- c('apple','strawberry','watermelon')
df <- data.frame(product, cost, sale)
mean(df$cost); mean(df$sale)

eng <- c(90, 80, 60, 70)
math <- c(50, 60, 100, 20)
df_midterm <- data.frame(eng, math)

class <- c(1,1,2,2)
df_midterm <- data.frame(df_midterm, class)
df_midterm <- data.frame(eng, math, class)



### 4-3 외부데이터 이용하기
install.packages("readxl")
library(readxl)

df_exam <- read_excel("excel_exam.xlsx")
df_exam$english
mean(df_exam$english)
mean(df_exam$science)



#### 데이터 불러오기
novar <- read_excel("Data/excel_exam_novar.xlsx")
novar
# 컬럼명이 없으므로 옵션값이 필요함
novar <- read_excel("Data/excel_exam_novar.xlsx", col_names = F)

# sheet3의 데이터를 선택해서 가져올 때
sheet <- read_excel("Data/excel_exam_sheet.xlsx", sheet = 3)

#### 데이터 저장하기
write.csv(df_midterm, file = 'data1/df_midterm.csv')
