from konlpy.tag import Komoran
import numpy as np

komoran = Komoran()
# text = '오늘 날씨는 구름이 많아요.'
text = '오늘 날씨는 구름과 우주인이 많아요.'
# text = '오늘 날씨는 구름과 우주인과 구름이 많아요.'   # 중복되는 단어는 하나로

# 명사만 추출
nouns = komoran.nouns(text)

# 단어사전 구축 및 단어별 인덱스 부여   
dics = {}
for word in nouns:
    if word not in dics.keys():      # key: value로 저장되므로 중복 없음
        dics[word] = len(dics)

# 원핫 인코딩
nb_classes = len(dics)
targets = list(dics.values())
one_hot_targets = np.eye(nb_classes)[targets]

print(nouns)
print()
print(dics)
print()
print(one_hot_targets)