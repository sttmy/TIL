#!/usr/bin/env python
# coding: utf-8

# ### 서울시 공공자전거 대여이력 정보
# ### https://data.seoul.go.kr/dataList/OA-15182/F/1/datasetView.do

# In[44]:


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:85% !important; }</style>"))


# In[1]:


import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus'] = False     #마이너스 표시
plt.rc('font', family = 'Malgun Gothic')


# In[3]:


# 6개 공공자전거 대여이력정보
df1 = pd.read_csv('./Data/Pandas/공공자전거 대여이력 정보_2021.01.csv',
              encoding = 'cp949', low_memory = False)   #encoding utf-8 또는 cp949, 데이터명세서를 보고 판단
df1.head(5)


# In[4]:


df2 = pd.read_csv('./Data/Pandas/공공자전거 대여이력 정보_2021.02.csv', encoding = 'cp949', low_memory = False)
df3 = pd.read_csv('./Data/Pandas/공공자전거 대여이력 정보_2021.03.csv', encoding = 'cp949', low_memory = False)
df4 = pd.read_csv('./Data/Pandas/공공자전거 대여이력 정보_2021.04.csv', encoding = 'cp949', low_memory = False)
df5 = pd.read_csv('./Data/Pandas/공공자전거 대여이력 정보_2021.05.csv', encoding = 'cp949', low_memory = False)
df6 = pd.read_csv('./Data/Pandas/공공자전거 대여이력 정보_2021.06.csv', encoding = 'cp949', low_memory = False)


# In[7]:


df2.info()


# In[35]:


# 데이터 연결
df = pd.concat([df1,df2,df3,df4,df5,df6], axis = 0)
df.tail()


# In[36]:


df.info()


# In[37]:


df.shape


# ## 데이터전처리

# In[38]:


# 불필요한 컬럼 제거
df = df.drop(columns = ['자전거번호','대여거치대','반납거치대'])
# df.drop(columns = ['자전거번호','대여거치대','반납거치대'], inplace =True)
df.info()


# In[39]:


# 카테고리형 형변환: '대여 대여소번호', '반납대여소번호'  > 카테고리형
df[['대여 대여소번호', '반납대여소번호']] = df[['대여 대여소번호', '반납대여소번호']].astype('category')
df.info()


# In[40]:


# 대여일시,반납일시 date time으로 변환
df['대여일시'] = pd.to_datetime(df['대여일시'])
df['반납일시'] = pd.to_datetime(df['반납일시'], errors = 'coerce')

# errors 오류 : {'무시','상승','강제'}, default는 상승
# raise: 잘못된 구문 분석은 예외 발생
# coerce: 잘못된 구문 분석은 NaN로 설정됨
# ignore: 잘못된 구문 분석은 입력을 반환함

# Pandas datetime 참고: https://hazel01.tistory.com/34

df.info()


# In[41]:


# 결측치확인 및 제거
df.isnull().sum()


# In[42]:


df.dropna(inplace = True)
df.isnull().sum()


# ## 분석

# #### 일별 이용현황

# In[43]:


# 대여날짜 컬럼을 추가
df['대여일자'] = df['대여일시'].dt.date
df.head()


# In[51]:


# 대여날짜별 대여건수: 집계가 필요, pivot table, groupby
df_date = df.groupby(df['대여일자']).대여일시.count().to_frame()
df_date.columns = ['대여건수']
df_date


# In[54]:


# 대여날짜별 대여건수 시각화

plt.plot(df_date.index, df_date.values, c = 'coral')
plt.title("서울시 공공자전거 대여날짜별 대여건수")
plt.show()


# #### 대여날짜별 이용시간

# In[55]:


df.head()


# In[58]:


# groupby ('대여날짜') [이용시간] 합계
df_time = df.groupby('대여일자').이용시간.sum().to_frame()
df_time


# In[60]:


# 시각화

plt.plot(df_time.index, df_time.values, c = 'skyblue')    # df_time.values 와 df_time['이용시간'] 같음
plt.title('서울시 공공자전거 대여날짜별 이용시간 합계')
plt.show()


# In[64]:


fig = plt.figure(figsize = (10,3))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.plot(df_date.index, df_date.values, c = 'coral')
ax2.plot(df_time.index, df_time.values, c = 'skyblue')

ax1.set_title("서울시 공공자전거 대여날짜별 대여건수")
ax2.set_title('서울시 공공자전거 대여날짜별 이용시간')

plt.show()


# #### 대여날짜별 이용거리

# In[66]:


df.head()


# In[71]:


df_dist = df.groupby('대여일자').이용거리.sum().to_frame()
df_dist


# In[72]:


plt.plot(df_dist.index, df_dist.values, c = 'olive')
plt.title('서울시 공공자전거 대여날짜별 이용거리')
plt.show()


# In[75]:


fig = plt.figure(figsize = (15,3))
ax1 = fig.add_subplot(1,3,1)
ax2 = fig.add_subplot(1,3,2)
ax3 = fig.add_subplot(1,3,3)

ax1.plot(df_date.index, df_date.values, c = 'coral')
ax2.plot(df_time.index, df_time.values, c = 'skyblue')
ax3.plot(df_dist.index, df_dist.values, c = 'olive')

ax1.set_title("서울시 공공자전거 대여날짜별 대여건수")
ax2.set_title('서울시 공공자전거 대여날짜별 이용시간')
ax3.set_title('서울시 공공자전거 대여날짜별 이용거리')

plt.show()


# ### 데이터프레임 합치기

# In[82]:


# 이용시간, 이용거리, 대여건수

df_all = pd.concat([df_date, df_time, df_dist], axis = 1)
df_all


# ## 시간대별 대여/반납 현황

# In[83]:


df.head(3)


# In[85]:


df['대여시간'] = df['대여일시'].dt.hour
df['반납시간'] = df['반납일시'].dt.hour
df.head(3)


# In[86]:


df.info()


# In[91]:


# 시간대별 대여 현황
df_rental = df['대여시간'].value_counts()
df_rental


# In[92]:


# 시간대별 반납 현황
df_return = df['반납시간'].value_counts()
df_return


# In[97]:


plt.bar(df_rental.index, df_rental.values)
plt.title('시간대별 대여 건수')
plt.show()


# In[99]:


plt.bar(df_return.index, df_return.values)
plt.title('시간대별 반납 건수')
plt.show()


# In[94]:


# 시각화

fig = plt.figure(figsize = (15,3))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.plot.bar(df_rental.index, df_rental.values, c = 'coral')
ax2.plot.bar(df_return.index, df_return.values, c = 'skyblue')

ax1.set_title('시간대별 대여 건수')
ax2.set_title('시간대별 반납 건수')

plt.show()


# In[98]:


df['대여 대여소번호']


# In[100]:


df['반납대여소번호']


# In[107]:


# 대여소번호 규칙 통일(00 제거)하기 위해서 str으로 변환 후 공백제거, category로 변환

df['반납대여소번호'] = df['반납대여소번호'].astype('str')
df['반납대여소번호'] = df['반납대여소번호'].str.lstrip('0')   # 왼쪽 공백제거 lstrip
df['반납대여소번호']


# In[108]:


df['반납대여소번호'] = df['반납대여소번호'].astype('int')   # int형으로 변환
df['반납대여소번호'] = df['반납대여소번호'].astype('category')


# In[109]:


df['반납대여소번호'].unique()


# In[105]:


df['대여 대여소번호'].unique()


# ### 대여/반납건수가 가장 많은 대여소 top10
# 

# In[113]:


df['대여 대여소번호'].value_counts()[:10].to_frame()
df[['대여 대여소번호','대여 대여소명']].value_counts()[:10].to_frame()


# In[114]:


df['반납대여소번호'].value_counts()[:10].to_frame()
df[['반납대여소번호','반납대여소명']].value_counts()[:10].to_frame()


# In[119]:


# 대여/반납 대여소번호 같은 것 추출하는 방법?
# df[조건].groupby('대여날짜')['이용시간'].sum().to_frame()
# 조건: ( df['대여 대여소번호']==207 ) &  (df['반납 대여소번호']==207 ) 
    
df_e = df[( df['대여 대여소번호']==207 ) &  (df['반납대여소번호']==207 ) ].groupby('대여일자')['이용시간'].sum().to_frame()
df_e


# ### 여의나루역 1번출구 앞에서 빌려서 어디로 반납하나

# In[116]:


# df[조건]
df_207 = df[df['대여 대여소번호']==207]
df_207.info()


# In[120]:


df_207[['반납대여소번호','반납대여소명']].value_counts().to_frame()


# In[122]:


# 여의나루에서는 어느 요일에 많이 빌리나
df_207['대여요일'] = df_207['대여일시'].dt.strftime('%a')


# In[124]:


df_207.head()


# In[126]:


df_207['대여요일'].value_counts()


# In[128]:


# df_207 기본통계 평균, 최대, 최소값
df_207['이용시간'].mean(), df_207['이용시간'].min(), df_207['이용시간'].max()


# In[ ]:


df

# 전체데이터의 평균

