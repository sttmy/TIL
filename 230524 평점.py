#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 한글 형태소 분석기
from wordcloud import WordCloud, STOPWORDS
from PIL import Image # 그림을 불러오는 패키지
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from konlpy.tag import Okt, Kkma, Komoran # 세가지 방법이 있음

from matplotlib import font_manager, rc 
import matplotlib.pyplot as plt
import matplotlib as mpl

# 마이너스 표시
mpl.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='Malgun Gothic')

# 한글 경로
font_path = r"C:\Windows\Fonts\malgun.ttf"# 워드클라우드 분석


# In[3]:


reviews = pd.read_excel("Data/[크롤링] 역대_네이버_영화_평점_최종_수정.xlsx")
reviews.head()


# In[4]:


reviews.info()


# In[28]:


# 참여자수 데이터타입 int로 변경
reviews.참여자수 = reviews.참여자수.apply(lambda x: x.replace(',','')).astype('int64')


# In[29]:


# 평점 정보만 추출
Star = pd.concat([reviews.iloc[:,1:5], reviews.iloc[:,13:]], axis = 1)
Star


# In[33]:


# 평점 평가 참여자비율 
Star['참여자비율'] = Star.참여자수 / Star.관객수
Star[ Star.참여자비율 >= Star.참여자비율.mean() ]


# In[188]:


Star.참여자비율.describe()


# ### 각 연령대의 분포 정보에 따라서 가중치 부여 해야 하나, 몇 명이 평점을 부여했는지 정보가 없음
# 
# 연령대별 인구통계 정보 반영해 재계산
# 

# In[75]:


# 인구통계 불러오기 (2023.4.기준)
pop = pd.read_csv('Data/[행안부] 주민등록인구통계_202304_202304_연령별인구현황_월간.csv', encoding = 'CP949')

# 필요한 컬럼만 추출, 데이터타입 int로 변경
pops = pop.iloc[:1,].T[0].apply(lambda x: x.replace(',',''))
pops = pops.to_frame()
pops = pops.iloc[2:,]
pops.인구수 = pops.인구수.astype("int64")
pops = pops.reset_index()
pops.columns=['구분','인구수']


# In[87]:


#### 연령별 인구수 추출
pop_ages = pops.iloc[:12,]

# 필요 연령대만 추출
pop_ages.drop([0,1,7,8,9,10,11], axis = 0, inplace = True)

# 연령대별 비율
pop_ages['비율'] = pop_ages.인구수/pop_ages.인구수.sum()

# 컬럼 정리
구분 = ['10대','20대','30대','40대','50대']
pop_ages['구분'] = 구분


# In[95]:


#### 성별 인구수 추출
pop_sex = pd.concat([pops.iloc[13,:], pops.iloc[26,:]], axis = 1).T

# 성별 비율
pop_sex['비율'] = pop_sex.인구수 / (pop_sex.인구수.sum())

# 컬럼 정리
구분 = ['남','여']
pop_sex['구분'] = 구분

## 성별은 인구비율에 큰 차이가 없음


# In[140]:


# 연령별 평점 
Star_ages = pd.concat([Star.iloc[:,:6], Star.iloc[:,8:]], axis = 1)


# In[174]:


# 인구수 비율별 전체 평점 (재)
new = []
for j in range(0, 200):
    s = 0
    for i in range(0,5):
        s += Star_ages.iloc[:,6:11].T[j][i] * pop_ages.비율.iloc[i]
    new.append(round(s,2))
Star['연령비율평점'] = new


# In[177]:


(Star.전체-Star.연령비율평점).describe()   # 최대 차이는 0.28점


# In[205]:


StarTD = Star.sort_values('연령비율평점', ascending = False)
StarTD = StarTD.reset_index()


# ### 관객수 대비 평점 시각화

# In[192]:


fig = plt.figure(figsize = (12,5))
ax1 = plt.subplot()

# 관객수
color_1 = 'orange'
ax1.set_title('관객수 및 평점 비교', fontsize = 20)
ax1.set_xlabel('영화순위')
ax1.set_ylabel('관객수', fontsize = 14, color = color_1)
ax1.plot(Star.index, Star.관객수, color = color_1, marker='s', markersize=3)
ax1.tick_params(axis = 'y', labelcolor = color_1)

cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

# 평점
ax2 = ax1.twinx()
color_2 = 'darkgreen'
ax2.set_ylabel('평점', fontsize = 14, color = color_2)
ax2.plot(Star.index, Star.연령비율평점, color = color_2, marker = 'o', markersize=3)
ax2.plot(Star.index, Star.전체, color = 'yellowgreen', marker = 'o', markersize=3)
ax2.tick_params(axis = 'y', labelcolor = color_2)

plt.legend(['평점(보정)','평점'])
fig.tight_layout()
plt.show()


# In[210]:


StarTD.영화명


# In[223]:


fig = plt.figure(figsize = (12,5))
ax1 = plt.subplot()

# 평점
color_1 = 'darkblue'
ax1.set_title('관객수 및 평점 비교', fontsize = 20)
ax1.set_xlabel('평점순 영화')
ax1.set_ylabel('평점', fontsize = 14, color = color_1)
ax1.plot(StarTD.index, StarTD.연령비율평점, color = color_1, marker='s', markersize=3)
ax1.tick_params(axis = 'y', labelcolor = color_1)

# 관객수
ax2 = ax1.twinx()
color_2 = 'pink'
ax2.set_ylabel('관객수', fontsize = 14, color = color_2)
ax2.plot(StarTD.index, StarTD.관객수, color = color_2, marker = 'o', markersize=3)
# ax2.plot(StarTD.영화명, StarTD.전체, color = 'yellowgreen', marker = 'o', markersize=3)
ax2.tick_params(axis = 'y', labelcolor = color_2)

cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

fig.tight_layout()
plt.show()


# ### Scatter plot

# In[224]:


x = StarTD.연령비율평점
y = StarTD.관객수

np.random.seed(0)
colors = np.random.rand(200)
plt.scatter(x, y, c = colors)
plt.xlabel('평점', fontsize=10)
plt.ylabel('관객수', fontsize=10)
cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.xlim(5, x.sort_values(ascending = False)[0]+ x.sort_values(ascending = False)[0]/10)
plt.title('관객수 vs 평점')
plt.show()


# In[ ]:




