from gensim.models import Word2Vec
from konlpy.tag import Komoran
import time

# naver movie review data
def read_rv_data(filename):
    with open(filename, 'r', encoding = 'utf-8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]  # 헤더 제거
    return data

# 학습시간 측정 시작
start = time.time()

# file reading
print('1. 말뭉치 데이터 읽기 시작')
rv_data = read_rv_data('Data/230620/ratings.txt')
print(len(rv_data))
print('1. 말뭉치 데이터 읽기 완료: ', time.time() - start)

# 문장단위 명사 추출 
print('2. 형태소에서 명사만 추출 시작')
komoran = Komoran()
docs = [komoran.nouns(sentence[1]) for sentence in rv_data]    # sentence[1] : document 컬럼 데이터
print('2. 형태소에서 명사 추출 완료: ', time.time() - start)

# Word2Vec 모델 학습
print('3. Word2Vec 모델 학습 시작')
model = Word2Vec(sentences = docs, vector_size= 400, window = 4, hs = 1, min_count = 2, sg = 1)
# vector_size: 단어 임베딩 벡터 차원(크기)
# hs: 1 (softmax 사용), 0 (negative sampling 사용)
# min_count: 단어 최소 빈도수 제한 (min_count 이하 단어들은 학습하지 않음)
# sg: 0 (CBOW 모델), 1 (skip-gram 모델)
# workers: 학습을 위한 프로세스 수
print('3. Word2Vec 모델 학습 완료: ', time.time() - start)

# 모델 저장
print('4. 학습된 모델 저장 시작')
model.save('Data/230620/nvmc4_400.model')
print('4. 학습된 모델 저장 완료: ', time.time() - start)

# 학습된 말뭉치 수, 코퍼스 내 전체 단어 수
print('corpus_count: ', model.corpus_count)
print('corpus_total_words: ', model.corpus_total_words)
