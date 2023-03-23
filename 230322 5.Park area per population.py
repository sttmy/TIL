#!/usr/bin/env python
# coding: utf-8

# ### 인구 대비 공원 면적

# 공원 면적의 합/ 인구수 대비 공원의 면적 구하기
# 
# 단계구분도 그려서, 인구수 대비 공원 면적이 넓은지 표시
# 
# 만들었던 '서울공원요약.csv', 서울시 인구와 면적.txt 

# In[2]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl

# 한글나오도록
import matplotlib.pyplot as plt    
from matplotlib import font_manager, rc
mpl.rcParams['axes.unicode_minus'] = False   # 마이너스 표시
plt.rc('font', family = 'Malgun Gothic')


# In[69]:


park = pd.read_csv('./data1/서울공원요약.csv')
park.head()


# ### 자치구별 공원 면적과 수

# In[6]:


area = park.groupby('지역')[['면적']].sum()
area.head()


# In[11]:


count = park.groupby('지역')[['면적']].count()
count.columns = ['갯수']
count.head()


# In[13]:


all = pd.concat([area,count], axis = 1)
all.head()


# In[70]:


### tch
df = park.groupby('지역')['면적'].agg(['sum','count'])
df.head()


# In[15]:


df.info()


# In[71]:


df.drop(index ='과천시', inplace = True)
df.shape


# ### 구별 공원면적 비율 및 인당 공원면적 비교

# In[72]:


seoul_df = pd.read_csv('./Data/서울시 인구와 면적.txt', sep = '\t')  
# sep ='\t'  tab으로 구분된 데이터 불러올 때
seoul_df.head()


# In[73]:


# '합계'열, '기간'행 삭제
seoul_df.drop(index = 0, inplace = True)
seoul_df.drop(columns = '기간', axis = 1, inplace = True)


# In[74]:


seoul_df.shape


# In[75]:


seoul_df.set_index('지역', inplace = True)
seoul_df.head()


# In[76]:


# 공원집계 데이터와 인구데이터 합치기

df = df.join(seoul_df[['인구','면적']])
df.head()


# In[77]:


# '면적' 컬럼, km^2이므로, 단위조정 필요. 공원면적(sum, m^2)과 맞춰줘야 함
df['면적'] = df.면적*1000000
df.head()


# In[78]:


df.info()


# In[79]:


# 인구 ',' int로 바꿔줘야 나눗셈이 가능
# df['인구'] = df.인구.apply(lambda x: str(x))
df['인구'] = df.인구.apply(lambda x: int(x.replace(',','')))
df.head(3)


# In[81]:


df['면적비율'] = df['sum']/ df.면적 * 100   # 전체 면적대비 공원면적   
# df.sum으로 쓰면 sum을 method로 인식해버리므로 주의'
df['인당면적'] = df['sum']/ df.인구        # 구 내 인원 대비 공원면적
df.head()


# In[84]:


df.rename(columns = {'sum':'공원면적','count':'공원갯수'}, inplace = True)
df.head()


# ## 시각화

# In[87]:


# 자치구별 공원 면적비율
df.면적비율.sort_values().plot(kind = 'barh',
                          grid = True,
                          figsize = (6,4))
plt.title('자치구 공원면적 비율(%)', size = 15)


# In[88]:


# 인당공원 면적
df.인당면적.sort_values().plot(kind = 'barh',
                          grid = True,
                          figsize = (6,4))
plt.title('자치구별 인당 공원면적', size = 15)


# In[89]:


df.to_csv('./data1/자치구별 공원 현황.csv')    
# index= False는 안넣기. 인덱스가 지역으로 되어있으므로, 나중에 사용하려면 없는 것으로 저장


# In[ ]:




