library(dplyr)   #
library(multilinguer) #   multilinguer 패키지는 R 사용자에게 자바 설치를 쉽게 해주는 install_jdk() 함수를 제공
library(KoNLP)
library(stringr)
library(wordcloud)
library(RColorBrewer)
library(ggplot2)
useNIADic()

# Twitter.csv 파일 보는 법: 메모장으로 실행 후 다른이름으로 저장시, 인코딩을 UTF-8(BOM) 으로 저장, csv파일 실행

##### 국정원 트윗 텍스트마이닝

twitter <- read.csv("Data/twitter.csv", header = T, fileEncoding = "UTF-8")
str(twitter)
head(twitter)
twitter <- rename(twitter,
                  no = 번호,
                  id = 계정이름,
                  date = 작성일,
                  tw = 내용)
twitter$tw <- str_replace_all(twitter$tw,"\\W"," ")  #특수문자 제거

# 트윗에서 명사추출
nouns <- extractNoun(twitter$tw)
# 추출한 명사 list 를 문자열 벡터로 변환, 단어별 빈도표 생성
wordcount <- table(unlist(nouns))
# 데이터 프레임으로 변환
df_word <- as.data.frame(wordcount, stringsAsFactors = F)
# 데이터 프레임 형성 시 stringsAsFactors 옵션이 default값 TRUE.
# stringsAsFactor 생략 시 문자열은 무조건 팩터로 저장되는데, 그렇게되면 row(행)를 추가할 수 없음. 만일 데이터 프레임을 생성한 후 행을 더 추가할 필요가 있다면 stringsAsFactor 옵션을 FALSE로 해줘야 함
# 데이터 프레임는 행렬(Matrix)과 출력 결과가 다를 뿐, Key-Value를 갖고 리스트와 문법이 비슷. 다만 행렬(Matrix)과 다른 점은 서로 다른 타입의 데이터를 저장할 수 있다는 것, 그리고 행 번호가 자동으로 부여되는 것임


# 변수명 수정
df_word <- rename(df_word,
                  word = Var1,
                  freq = Freq)
# 두 글자 이상 단어만 추출
df_word <- filter(df_word, nchar(word) >= 2)
# 상위 20 개 추출
top_20 <- df_word %>%
  arrange(desc(freq)) %>%
  head(20)

ggplot()
order <- arrange(top_20, freq)$word   #빈도 순서 변수 생성

ggplot(data = top_20, aes(x= word, y = freq)) +
  geom_col() +
  ylim(0,2500) +
  coord_flip() +
  scale_x_discrete(limit = order) +
  geom_text(aes(label = freq), hjust = -0.3)   #빈도표시 

pal <- brewer.pal(8, "Dark2")   #Dark2 라는 팔레트를 쓰겠다
set.seed(2023)   #난수생성 시드값
wordcloud(words = df_word$word,
          freq = df_word$freq,
          min.freq = 10, # 최소한 2번은 나와야 wordcloud에 그릴 거다
          max.words = 200, #최대 표현하는 단어수, 200개만 선정
          random.order = F, #단어를 중앙에 배치
          rot.per = 0, #회전비율
          scale = c(6, 0.5), #단어 크기의 범위
          color = pal)
