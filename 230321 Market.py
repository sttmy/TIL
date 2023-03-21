#!/usr/bin/env python
# coding: utf-8

# # 서울시 농수축산물 가격
# ## https://data.seoul.go.kr/dataList/OA-1170/S/1/datasetView.do

# In[27]:


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


# In[7]:


df = pd.read_csv('./Data/Pandas/생필품 농수축산물 가격 정보(2021년1월_6월).csv', encoding = 'cp949', low_memory = False)   
df.head(5)


# In[8]:


df.info()


# In[9]:


df.isnull().sum()


# ## 데이터확인

# In[10]:


df['시장/마트 번호'].unique(), df['시장/마트 번호'].nunique()


# In[11]:


df['시장/마트 이름'].unique(), df['시장/마트 이름'].nunique()


# In[15]:


df['시장/마트 이름'].duplicated().sum()


# In[17]:


# 시장/마트 정보, 중복 제거
df_market = df[['시장/마트 번호', '시장/마트 이름', '자치구 이름', '시장유형 구분(시장/마트) 이름']].drop_duplicates()
df_market


# In[19]:


# 자치구별 시장/마트 갯수
df_market['자치구 이름'].value_counts()


# In[20]:


# 중구의 시장/마트이름을 보고 싶을 때
df_market[df_market['자치구 이름'] == '중구']


# In[21]:


df.head()


# In[23]:


# 품목 목록
df_items = df[['품목 번호', '품목 이름']].drop_duplicates()   # 리스트로 unique/nunique하고 싶을 때, drop.duplicates로 확인
df_items[:30]


# In[25]:


# 자치구 목록
df_gu = df[['자치구 코드', '자치구 이름']].drop_duplicates()
df_gu


# In[26]:


df_gu.shape


# In[29]:


df[['시장유형 구분(시장/마트) 코드', '시장유형 구분(시장/마트) 이름']].drop_duplicates()


# ### 삼겹살 가격분석

# In[55]:


# 특정 문자열 포함되어 있는지 확인하는 방법: .str.contains(문자열)
# 품목 이름 중에서 '삼겹살'이라는 단어가 포함된 셀을 가져오고 싶을 때 확용

df_pork = df [ ( df['품목 이름'].str.contains('삼겹살') )
    & ( df['년도-월']== '2021-06') 
    & ( df['실판매규격'].str.contains('600g'))
   ]
df_pork.head()


# In[34]:


df_pork.shape


# In[39]:


# 삼겹살가격 평균, 최대/최소값
df_pork['가격(원)'].mean(), df_pork['가격(원)'].min(), df_pork['가격(원)'].max()


# In[54]:


# 삼겹살 가격이 5000원 이하인 시장/마트 이름
# df[df_pork['가격(원)']<=5000]['시장/마트 이름']
df_pork[df_pork['가격(원)']<=5000]


# ### 우리동네 삼겹살 가격

# In[44]:


df_pork[['시장/마트 이름', '품목 이름', '실판매규격', '가격(원)']].drop_duplicates(inplace = True)


# In[45]:


gu = input('구이름: ')
df_pork['자치구 이름']== gu


# In[48]:


df_pork['자치구 이름'].unique(), df_pork['자치구 이름'].nunique()


# In[70]:


gu = input('구이름: ')
df_pork_gu = df_pork[df_pork['자치구 이름']== gu][['시장/마트 이름', '품목 이름', '실판매규격', '가격(원)']].drop_duplicates()


# In[71]:


# 시각화
x = df_pork_gu['시장/마트 이름']
y = df_pork_gu['가격(원)']
plt.scatter(x,y)
plt.title(gu + '삼겹살가격')
plt.grid()
plt.show()


# ### 마트 지점별 삼겹살 가격

# In[66]:


df_pork.head()


# In[67]:





# In[72]:


mart = input('시장/마트이름: ')   # 입력 백화점, '백화점'이 답이 포함되어 있어야 함.
df_pork_mart = df_pork[df_pork['시장/마트 이름'].str.contains(mart)][['시장/마트 이름', '품목 이름', '실판매규격', '가격(원)']].drop_duplicates()


# In[74]:


# 시각화
x = df_pork_mart['시장/마트 이름']
y = df_pork_mart['가격(원)']
plt.scatter(x,y)
plt.title(mart + '삼겹살가격')
plt.xticks(rotation = 45)
plt.grid()
plt.show()


# ## 달걀 분석

# In[ ]:


# 21년 6월 데이터 활용, 규격 30개 데이터프레임만들기
# 30개 평균가격, 최대, 최소값, 6000원 이하 어딘지
# 동네 달걀가격
# 백화점 지점별 달걀가격


# In[76]:


df.head()


# In[109]:


df_egg = df[df['품목 이름'].str.contains('달걀')]
df_egg = df_egg[['시장/마트 이름', '품목 이름', '실판매규격', '가격(원)','자치구 이름']]
df_egg


# In[110]:


df_egg30 = df_egg[df_egg['품목 이름'].str.contains('30')]
df_egg30


# In[111]:


df_egg30['가격(원)'].mean(), df_egg30['가격(원)'].min(), df_egg30['가격(원)'].max()


# In[112]:


df_egg30_6000 = df_egg30[df_egg30['가격(원)']<=6000]
df_egg30_6000


# In[113]:


df_egg30_6000 = df_egg30_6000[df_egg30_6000['가격(원)']>0]
df_egg30_6000


# In[115]:


# 동네 달걀가격
gu = input("자치구: ")
df_egg30_6000_gu = df_egg30_6000[df_egg30_6000['자치구 이름']==gu].drop_duplicates()
df_egg30_6000_gu


# In[116]:


# 백화점 지점별 달걀가격
mart = input('시장/마트이름: ')   # 입력 백화점, '백화점'이 답이 포함되어 있어야 함.
df_egg30_6000_mart = df_egg30_6000[df_egg30_6000['시장/마트 이름'].str.contains(mart)].drop_duplicates()
df_egg30_6000_mart


# In[117]:


# 시각화
x = df_egg30_6000_gu['시장/마트 이름']
y = df_egg30_6000_gu['가격(원)']
plt.scatter(x,y)
plt.title(gu + '달걀가격')
plt.grid()
plt.show()


# In[118]:


# 시각화
x = df_egg30_6000_mart['시장/마트 이름']
y = df_egg30_6000_mart['가격(원)']
plt.scatter(x,y)
plt.title(mart + '달걀가격')
plt.xticks(rotation = 45)
plt.grid()
plt.show()


# In[ ]:




