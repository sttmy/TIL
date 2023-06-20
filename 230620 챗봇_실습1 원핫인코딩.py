from konlpy.tag import Komoran
import numpy as np

komoran = Komoran(userdic = 'Data/230620/user_dict.tsv')
# komoran = Komoran()
# text = '뜨거운 여름이 오면 바다에 가고 싶다.'
# text = '겨울에는 스키나 스노우보드를 제일 즐긴다.'
text = '제일 좋아하는 계절은 가을이지만, 가을에 내리는 비는 좋아하지 않는다.'

nouns = komoran.nouns(text)

dics = {}
for word in nouns:
    if word not in dics.keys():
        dics[word] = len(dics)

targets = list(dics.values())
oh_targets = np.eye(len(dics))

print()
print(nouns)
print()
print(dics)
print()
print(oh_targets)