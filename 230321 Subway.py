#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))


# In[2]:


import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus'] = False     #마이너스 표시
plt.rc('font', family = 'Malgun Gothic')


# In[3]:


df = pd.read_csv('./Data/Pandas/서울시 지하철 호선별 역별 시간대별 승하차 인원 정보.csv', encoding = 'cp949', low_memory = False)   
df.head(5)


# In[4]:


df.shape


# In[5]:


df.isnull().sum()


# In[6]:


df['사용월'].unique(), df['사용월'].nunique()


# In[7]:


df['호선명'].unique(), df['호선명'].nunique()


# In[8]:


df.dtypes


# In[10]:


# 사용월을 문자열로 형변환
df['사용월'] = df['사용월'].astype('str')


# In[13]:


df.dtypes


# In[14]:


# 불필요한 컬럼 삭제
df.drop(columns=['작업일자'], inplace = True)


# ### 시간 승차/하차

# In[15]:


# 승차테이블 만들기
df.head(3)


# In[ ]:


# 사용월, 호선명, 지하철역 >> df1, 승차컬럼 df2, 하차컬럼 df3


# In[16]:


df1 = df[['사용월','호선명','지하철역']]
df1.head()


# In[22]:


df.columns.str.contains('승차')


# In[29]:


df2 = df.loc[:,df.columns.str.contains('승차')]
df2.head()


# In[30]:


df3 = df.loc[:,df.columns.str.contains('하차')]
df3.tail()


# In[31]:


### tch
df1_t = df.iloc[:,:3]
df2_t = df.iloc[:,3::2]
df3_t = df.iloc[:,4::2]


# In[32]:


# df2에서 '승차인원' 제거
df2.columns = df2.columns.str.split(' ').str[0]
df2.columns


# In[33]:


# 승차테이블
df_in = pd.concat([df1,df2], axis = 1)
df_in.head()


# In[34]:


# df3에서 '하차인원' 제거
df3.columns = df3.columns.str.split(' ').str[0]
df3.columns


# In[35]:


# 하차테이블
df_out = pd.concat([df1,df3], axis = 1)
df_out.head()


# ### 최근월 기준으로 승하차 데이터프레임생성

# In[36]:


df_in_21aug = df_in[df_in['사용월'] == '202108']
df_out_21aug = df_out[df_out['사용월'] == '202108']


# In[41]:


# 출근시간(08~09시)에 가장 많이 승차하는 역?
df_in_21aug.nlargest(10, '08시-09시')[['지하철역','08시-09시']]    # nlargest


# In[42]:


df_out_21aug.nlargest(10, '09시-10시')[['지하철역','09시-10시']]


# In[43]:


# 퇴근 시간에 가장 많은 사람이 승차/하차 하는 역은?
df_in_21aug.nlargest(10, '18시-19시')[['지하철역','18시-19시']]


# In[44]:


df_out_21aug.nlargest(10, '19시-20시')[['지하철역','19시-20시']]


# ### 강남역 최근 시간대별 승하차 정보 분석

# In[46]:


df_in_21aug.head()


# In[53]:


# df_in_21aug 에서 강남역 추출
df_gn_in = df_in_21aug[df_in_21aug['지하철역']=='강남']
# df_gn_in = df_in_21aug[df_in_21aug['지하철역']=='강남'].iloc[:,3:]  
df_gn_in


# In[54]:


df_gn_in = df_gn_in.melt()
df_gn_in


# In[57]:


# column명 변경
df_gn_in.columns = ['시간대','승차건수']
df_gn_in.sort_values('승차건수', ascending = False)


# In[59]:


# 시각화, 시간대별 승차인원

plt.figure(figsize = (7,5))
plt.barh(df_gn_in['시간대'], df_gn_in['승차건수'])
plt.show()


# In[115]:


# 강남역의 최근 하차정보 분석

df_gn_out = df_out_21aug[df_out_21aug['지하철역']=='강남'].iloc[:,3:] 
df_gn_out


# In[116]:


df_gn_out = df_gn_out.melt()
df_gn_out.columns = ['시간대','하차건수']
df_gn_out


# In[118]:


df_gn_out = df_gn_out.sort_index(ascending= False)   # index 재정렬
df_gn_out


# In[71]:


df_gn_out = df_gn_out.T     # melt를 쓸 필요 없고, transpose를 사용해도 무관


# In[72]:


df_gn_out


# In[73]:


df_gn_out.columns = [['하차건수']]
df_gn_out


# In[119]:


# 시각화, 시간대별 승차인원

plt.figure(figsize = (7,5))
plt.barh(df_gn_out['시간대'], df_gn_out['하차건수'])
plt.show()


# ## 지하철 시간대별, 역별 이용현황

# #### 최근(202108) 데이터 중 승차정보 집계 데이터 만들기

# In[82]:


df_in_21aug_agg = df_in_21aug.copy()
df_in_21aug_agg.head(3)


# In[89]:


# 지하철역 컬럼을 인덱스로 지정
df_in_21aug_agg.index = df_in_21aug_agg['지하철역']
df_in_21aug_agg.head(3)


# In[90]:


# 필요없는 컬럼 제거 사용월, 호선명, 지하철역
df_in_21aug_agg.drop(columns = ['사용월', '호선명', '지하철역'], inplace = True)
df_in_21aug_agg.head(3)


# In[97]:


# 행과 열 합계
# 합계 행 추가
df_in_21aug_agg.loc['sum'] = df_in_21aug_agg.apply('sum', axis = 0)
df_in_21aug_agg.tail(3)


# In[107]:


# 합계 열 추가
df_in_21aug_agg['sum'] = df_in_21aug_agg.apply('sum', axis = 1)
df_in_21aug_agg.head(3)


# In[108]:


# 시간대별 승차건수
s_in = df_in_21aug_agg.loc['sum'][:-1]
s_in.sort_values()


# In[109]:


x = s_in.index 
y = s_in.values
plt.bar(x,y)
plt.xticks(rotation=45)
plt.show()


# In[110]:


# 지하철 역별 승차건수 
s_in = df_in_21aug_agg['sum'][:-1]
s_in


# #### 최근(202108) 데이터 중 하차정보 집계 데이터 만들기

# In[120]:


df_out_21aug_agg = df_out_21aug.copy()
df_out_21aug_agg.head(3)


# In[121]:


# 지하철역 컬럼을 인덱스로 지정, 불필요 컬럼 제거
df_out_21aug_agg.index = df_out_21aug_agg['지하철역']
df_out_21aug_agg.drop(columns = ['사용월', '호선명', '지하철역'], inplace = True)
df_out_21aug_agg.head(3)


# In[122]:


# 행과 열 합계
df_out_21aug_agg.loc['sum'] = df_out_21aug_agg.apply('sum', axis = 0)
df_out_21aug_agg['sum'] = df_out_21aug_agg.apply('sum', axis = 1)
df_out_21aug_agg.tail(3)


# In[123]:


# 시간대별 하차건수, 지하철역별 하차건수
s_out_hour = df_out_21aug_agg.loc['sum'][:-1]
s_out_sub = df_out_21aug_agg['sum'][:-1]
s_out_hour, s_out_sub


# In[126]:


x = s_out_hour.index 
y = s_out_hour.values
plt.bar(x,y)
plt.xticks(rotation=45)
plt.title('시간대별 하차건수')
plt.show()


# In[136]:


x = s_out_sub.index 
y = s_out_sub.values
plt.figure(figsize = (50,5))   # 그래프사이즈 설정
plt.bar(x,y)
plt.xticks(rotation=45)
plt.title('지하철역별 하차건수')
plt.show()


# In[ ]:




