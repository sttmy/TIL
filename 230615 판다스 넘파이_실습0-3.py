'''
다음의 'jumsu' 자료를 딕셔너리를 기초자료로 하여 s1_jumsu 시리즈를 만드세요.
Series 를 만들면 이것을 <실행결과> 와 같이 출력하세요.
실행결과에 출력된 것은 학생개인의 최대점수와 최소 점수입니다.
'''

import numpy as np
import pandas as pd 

jumsu = {
'홍길동' : [50,60,50],
'이순신' : [60,60,60],
'강감찬' : [100,90,90],
'유관순' : [80,80,90],
'강환석' : [95,95,95],
}

s1_jumsu = pd.Series(jumsu)

print()
for i in s1_jumsu.index:
    print('-' + i + '-', end='-')
print()
for i in s1_jumsu.values:
    print( '-{:.2f}점-'.format(np.max(i)), end='')  
print()
for i in s1_jumsu.values:
    print( '-{:.2f}점-'.format(np.min(i)), end='')  
