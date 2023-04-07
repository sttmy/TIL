
##### 10.텍스트마이닝

install.packages("multilinguer")  # 한국어 형태소 분석 패키지
library(multilinguer)
install_jdk()   #자바 언어 기반 Java Developed Kit

install.packages(c("stringr","hash","tau","Sejong","RSQLite","devtools"), type = "binary")  # 의존성 패키지 설치
install.packages("remotes")  #깃허브 버전 설치
remotes::install_github("haven-jeon/KoNLP", upgrade = "never", INSTALL_opts=c("--no-multiarch"))    # 깃허브 업로드?
library(KoNLP)
library(dplyr)

# 사전 설정
useNIADic()

##### global options > code > saving > default text encoding: UTF-8 로 변경

##### 힙합 가사 추출해보기.

txt <- readLines('Data/hiphop.txt')
library(stringr)
txt <- str_replace_all(txt,"\\W"," ")  #특수문자 제거

## 명사 추출하기 샘플
extractNoun("대한민국의 영토는 한반도와 그 부속도서로 한다")

# 가사에서 명사 추출
noun <- extractNoun(txt)
# 추출한 명사 list를 문자열벡터로 변환
wordcount <-  table(unlist(noun))
# 단어별 빈도표 생성
df_word <- as.data.frame(wordcount, stringsAsFactors = F)
table(df_word)
# 변수명 수정
df_word <- rename(df_word, word = Var1, freq = Freq) # 바꿀이름 = 원래변수이름

# 두 글자 이상 단어를 추출
df_word <- filter(df_word, nchar(word) >= 2)
top_20 <- df_word %>% 
  arrange(desc(freq)) %>% 
  head(20)
View(top_20)

### word cloud 패키지설치
install.packages("wordcloud")
library(wordcloud)
library(RColorBrewer)   #색깔 칠하는 것

pal <- brewer.pal(8, "Dark2")   #Dark2 라는 팔레트를 쓰겠다
set.seed(2023)   #난수생성 시드값
wordcloud(words = df_word$word,
          freq = df_word$freq,
          min.freq = 2, # 최소한 2번은 나와야 wordcloud에 그릴 거다
          max.words = 200, #최대 표현하는 단어수, 200개만 선정
          random.order = F, #단어를 중앙에 배치
          rot.per = 0.1, #회전비율
          scale = c(4, 0.3), #단어 크기의 범위
          color = pal)

pal2 <- brewer.pal(9, "Blues")[5:9]
set.seed(1234)   #난수생성 시드값
wordcloud(words = df_word$word,
          freq = df_word$freq,
          min.freq = 2, 
          max.words = 200, 
          random.order = F,
          rot.per = .1, 
          scale = c(4, 0.3), 
          color = pal2)  #팔레트2로 그리기
