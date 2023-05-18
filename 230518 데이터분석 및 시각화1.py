#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from matplotlib import pyplot as plt
import datetime as dt
import seaborn as sns

# 한글폰트설치
from matplotlib import font_manager, rc
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus'] = False   # 마이너스 표시
plt.rc('font', family = 'Malgun Gothic')


# In[56]:


# 영화리스트
movieList = pd.read_excel('Data/afterpreprocessing/(완)영화정보 리스트_개봉일자(2017~2023).xlsx')

# 일별영화데이터
movies = pd.read_csv('Data/afterpreprocessing/완_기간별_일별_170101_to_230509_ver1.csv')

# TOP200영화 : 관객수기준 
movieTop = pd.read_excel('Data/afterpreprocessing/(완)역대_박스오피스(2023.05.11).xlsx')

# TOP200영화
movieTop_add = pd.read_excel('Data/movieTop_add(엑셀).xlsx')
movieTop200 = movieTop_add[['순위','영화명','개봉일','매출액','관객수','스크린수','상영횟수','대표국적','배급사','상영일수','개봉연월','개봉월','개봉요일','일일최다관람객수','등급','장르','분']]


# In[57]:


movieTop200.info()


# In[58]:


movieTop200['개봉일'] = movieTop200['개봉일'].astype('datetime64[ns]')


# In[59]:


movieTop200['개봉연도'] = movieTop200['개봉일'].dt.year


# ### 영화 개봉연월별 관객수

# In[74]:


mv = movies.drop_duplicates(['영화명','개봉일'], keep = 'last')


# In[76]:


mv.info()


# In[79]:


mv2 = mv[['영화명','개봉일','대표국적','등급','장르','제작사','배급사','감독','배우','누적매출액','누적관객수']]
mv2['개봉일'] = mv2['개봉일'].astype('datetime64[ns]')


# In[81]:


mv2['개봉월'] = mv2['개봉일'].dt.month
mv2['개봉연도'] = mv2['개봉일'].dt.year


# In[84]:


pv = mv2.pivot_table('누적관객수','개봉월','개봉연도')


# In[102]:


plt.figure(figsize = (7,5))
plt.title('개봉연월별 누적관객수 히트맵')

sns.heatmap(pv, cmap='YlGnBu', annot = True, annot_kws ={'size':10}, linewidths = 1)


# ### 영화등급별 누적관객수

# In[132]:


mv2.등급.unique()


# In[138]:


mv2.replace({'등급':'12세관람가'}, '12세이상관람가',inplace = True)
mv2.replace({'등급':'12세이상관람가,15세이상관람가'}, '12세이상관람가',inplace = True)
mv2.replace({'등급':'15세관람가'}, '15세이상관람가',inplace = True)
mv2.replace({'등급':'연소자관람불가,청소년관람불가'}, '청소년관람불가',inplace = True)


# In[139]:


pv2 = mv2.pivot_table('누적관객수','등급','개봉연도')
plt.figure(figsize = (7,5))
plt.title('영화등급별 누적관객수 히트맵')

sns.heatmap(pv2, cmap='PuRd', annot = True, annot_kws ={'size':10}, linewidths = 1)


# In[141]:


visit = pd.read_excel('Data/[서울열린데이터광장] 2005-2021 연간 영화관 평균 방문횟수 통계.xlsx')
visit.head()


# In[149]:


vs = visit.T


# In[151]:


vs.columns = vs.iloc[2]


# In[172]:


vs.reset_index(inplace = True)


# In[176]:


vs.drop(index=[0,1,2], axis = 0, inplace = True)


# In[185]:


vs.reset_index(inplace = True)


# In[195]:


vs['index'] = vs['index'].apply(lambda x : x.split(' ')[-1])


# In[200]:


vs.drop(columns = ['level_0'], axis = 1, inplace = True)


# In[223]:


visit_age = vs.iloc[:,:10]
visit_age.reset_index('index')


# In[202]:


v = vs.T
v.columns = v.iloc[0]

