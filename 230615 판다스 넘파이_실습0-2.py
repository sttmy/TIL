'''
다음의 'jumsu' 자료를 딕셔너리를 기초자료로 하여 s1_jumsu 시리즈를 만드세요.
s1_jumsu 시리즈는 데이터(요소)가 평균이고 인덱스가 이름으로 구성되도록 하세요.
Series 를 만들면 이것을 <실행결과> 와 같이 출력하세요.
'''

import pandas as pd
import numpy as np

jumsu = {
'홍길동' : [50,60,50],
'이순신' : [60,60,60],
'강감찬' : [100,90,90],
'유관순' : [80,80,90],
'강환석' : [95,95,95],
}

js = pd.Series(jumsu)

idx = []
vls = []
for i in range(len(js)):
    idx.append(js.index[i])
    vls.append(round(np.mean(js.values[i]),2))

s1_jumsu = pd.Series(vls, index = idx)

jum = []
for j in range(len(s1_jumsu)):
    v = str("{:.2f}".format(s1_jumsu.values[j]))
    jum.append(str(v)+'점')

print('-'+'---'.join(s1_jumsu.index)+'-')
print('-'+'--'.join(jum)+'-')