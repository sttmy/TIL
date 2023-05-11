#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# ## 03_Grouping

# 뉴욕 airBnB : https://www.kaggle.com/ptoscano230382/air-bnb-ny-2019 

# In[4]:


DataUrl = 'https://raw.githubusercontent.com/Datamanim/pandas/main/AB_NYC_2019.csv'
df = pd.read_csv(DataUrl)
df.head()


# In[6]:


df.info()


# 45. 데이터의 각 host_name의 빈도수를 구하고 host_name으로 정렬하여 상위 5개를 출력하라

# In[8]:


df.groupby('host_name').size()


# In[12]:


df.host_name.value_counts().sort_index()


# 46. 데이터의 각 host_name의 빈도수를 구하고 빈도수 기준 내림차순 정렬한 데이터 프레임을 만들어라. 빈도수 컬럼은 counts로 명명하라

# In[23]:


d = df.groupby('host_name').size().sort_values(ascending = False).to_frame()
d.columns = ['counts']
d


# In[28]:


df.groupby('host_name').size().to_frame().rename(columns = {0:'counts'}).sort_values('counts', ascending = False)


# 47. neighbourhood_group의 값에 따른 neighbourhood컬럼 값의 갯수를 구하여라

# In[32]:


df.groupby(['neighbourhood_group','neighbourhood']).size().to_frame()


# In[34]:


df.groupby(['neighbourhood_group','neighbourhood'], as_index = False).size()


# 48.neighbourhood_group의 값에 따른 neighbourhood컬럼 값 중 neighbourhood_group그룹의 최댓값들을 출력하라

# In[44]:


df.groupby(['neighbourhood_group','neighbourhood'], as_index = False).size().groupby(['neighbourhood'], as_index = False).max().sort_values('size', ascending = False)


# 49. neighbourhood_group 값에 따른 price값의 평균, 분산, 최대, 최소 값을 구하여라

# In[61]:


df[['neighbourhood_group','price']].groupby('neighbourhood_group').agg(['mean','var','max','min'])


# 50. neighbourhood_group 값에 따른 reviews_per_month 평균, 분산, 최대, 최소 값을 구하여라

# In[64]:


df[['neighbourhood_group','reviews_per_month']].groupby('neighbourhood_group').agg(['mean','var','max','min'])


# 51. neighbourhood 값과 neighbourhood_group 값에 따른 price 의 평균을 구하라

# In[67]:


df[['neighbourhood','neighbourhood_group','price']].groupby(['neighbourhood','neighbourhood_group']).mean()


# In[68]:


df.groupby(['neighbourhood','neighbourhood_group']).price.mean()


# 52.neighbourhood 값과 neighbourhood_group 값에 따른 price 의 평균을 계층적 indexing 없이 구하라

# In[69]:


df.groupby(['neighbourhood','neighbourhood_group']).price.mean().unstack()


# In[70]:


pd.pivot_table(df, index=['neighbourhood'], columns = ['neighbourhood_group'], values = ['price'], aggfunc = ['mean'])


# 53. neighbourhood 값과 neighbourhood_group 값에 따른 price 의 평균을 계층적 indexing 없이 구하고 nan 값은 -999값으로 채워라

# In[72]:


df.groupby(['neighbourhood','neighbourhood_group']).price.mean().unstack().replace(np.nan,-999)


# 54. 데이터중 neighbourhood_group 값이 Queens값을 가지는 데이터들 중 neighbourhood 그룹별로 price값의 평균, 분산, 최대, 최소값을 구하라

# In[87]:


df[df['neighbourhood_group'] == 'Queens'][['neighbourhood','price']].groupby(['neighbourhood']).agg(['mean','var','max','min'])


# 55.데이터중 neighbourhood_group 값에 따른 room_type 컬럼의 숫자를 구하고 neighbourhood_group 값을 기준으로 각 값의 비율을 구하여라

# In[92]:


df.groupby(['neighbourhood_group','room_type']).size()


# In[109]:


ans = df[['neighbourhood_group','room_type']].groupby(['neighbourhood_group','room_type']).size().unstack()
ans


# In[110]:


ans.sum(axis=1)


# In[148]:


ans


# In[151]:


ans1 = pd.DataFrame(columns=range(3), index = range(5))
for i in range(0,5):
    for j in range(0,3):
        ans1.values[i,j] = ans.values[i,j] / ans.sum(axis =1)[i]


# In[152]:


ans1.columns = ['Entire home/apt','Private room','Shared room']
ans1

