#!/usr/bin/env python
# coding: utf-8

# ### 코로나 확진자 발생동향 데이터
# 참고: 서울 열린데이터광장 https://data.seoul.go.kr/dataList/OA-20461/S/1/datasetView.do

# In[54]:


import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus'] = False     #마이너스 표시
plt.rc('font', family = 'Malgun Gothic')


# In[3]:


cr = pd.read_csv('./Data/Corona/서울시 코로나19 확진자 현황.csv', low_memory = False)
cr.head()


# ### 데이터 확인 및 전처리

# In[4]:


cr.info()


# In[9]:


# 불필요한 컬럼
cr = cr.drop(columns = ['환자번호','국적','환자정보','조치사항','이동경로','등록일','수정일','노출여부'])
cr.info()


# In[10]:


cr.head(3)


# In[22]:


# 확진일을 datetime타입으로 타입변경
cr['확진일'] = pd.to_datetime(cr['확진일'])
cr.info()


# In[23]:


# 지역 변수 갯수 확인
cr['지역'].unique(), len(cr['지역'].unique())


# In[24]:


cr['지역'].nunique()   # len(cr['지역'].unique())와 같음


# In[25]:


# 변수 내 공백제거 strip(), 컬럼별로 적용하려면 .str. 을 입력해줘야 함
cr['지역'] = cr['지역'].str.strip()  
cr['지역'].unique(), cr['지역'].nunique()


# In[26]:


cr['지역'] = cr['지역'].astype('category')
cr.info()


# ### 구별 확진자동향
# #### 확진일, 구별로  pivot_table집계

# In[27]:


cr.head()


# In[51]:


cr_gu = cr.pivot_table('연번', '확진일','지역', aggfunc = 'count', margins = True)
cr_gu


# In[40]:


pd.pivot_table(cr, '연번', '확진일','지역').head()


# In[42]:


### tch
cr_gu_t = pd.pivot_table(cr, index = '확진일', columns = '지역', values = '연번', aggfunc = 'count', margins = True)
cr_gu_t


# #### 서울시 일별 추가확진자 동향

# In[52]:


daily = cr_gu['All'][:-1]    # row별 합계, 마지막 총 합계는 불필요
daily


# In[49]:


daily_t = cr_gu_t['All'][:-1]  
daily_t


# In[53]:


# 2020-01-24 ~ 2021-09-28 중 가장 많은 추가확진자 발생일? 많은 순으로 정렬
daily.sort_values(ascending = False)    # series임


# In[58]:


# 서울시 일별 추가 확진자 시각화
x = daily.index
y = daily.values
plt.plot(x,y, c = 'coral')
plt.title('서울시 일별 확진자 시각화')
plt.xlabel('확진일')
plt.ylabel('확진자수')
plt.xticks(rotation=45)
plt.show()


# #### 서울시 구별 누적 확진자 비교

# In[59]:


s_gu = cr_gu.loc['All'][:-1]    # column별 합계
s_gu = s_gu.sort_values(ascending = False)
s_gu


# In[63]:


# 서울시 구별 누적확진자 많은 순으로 시각화
x = s_gu.index
y = s_gu.values
plt.figure(figsize=(5,4))
plt.barh(x,y)
plt.title('서울시 구별 누적 확진자수', size = 10)
plt.show()


# #### 최종집계일(21-09-28) 많은 확진자순으로 정렬

# In[69]:


sep28 = cr_gu.iloc[-2][:-1]
sep28_sort = sep28.sort_values(ascending = False)
sep28_sort


# In[70]:


x = sep28_sort.index
y = sep28_sort.values
plt.figure(figsize=(5,4))
plt.barh(x,y)
plt.title('2021-09-28 구별 확인자수', size = 10)
plt.show()


# #### 접촉력에 따른 확진 분석

# In[74]:


cr['접촉력'].unique(), cr['접촉력'].nunique()


# In[73]:


# 접촉력에 따른 확진 건수 best 10
cr.info()


# In[76]:


cr['접촉력'].value_counts()[:10].to_frame()


# #### 최근 월(9월) 접촉력에 따른 확진건수 Best10

# In[77]:


# 확진일을 연도 2021 & 9월 추출해서 ['접촉력'], value_counts()[:10].to_frame
cr.info()


# In[84]:


mask = (cr['확진일']>='2021-09-01') & (cr['확진일']<='2021-09-30')
filtered = cr.loc[mask]
filtered


# In[85]:


filtered['접촉력'].value_counts()[:10].to_frame()


# ### https://kibua20.tistory.com/195

# In[89]:


### tch
# df[조건]['접촉력'].value_counts()[:10].to_frame()
# 조건: cr['확진일'].dt.year == 2021) & (cr['확진일'].dt.month == 9

cr[(cr['확진일'].dt.year == 2021) & (cr['확진일'].dt.month == 9)]['접촉력'].value_counts()[:10].to_frame()


# In[ ]:




