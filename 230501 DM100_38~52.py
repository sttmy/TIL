#!/usr/bin/env python
# coding: utf-8

# ## 02 Filtering & sorting

# In[3]:


import pandas as pd
import numpy as np


# In[1]:


url ='https://raw.githubusercontent.com/Datamanim/pandas/main/chipo.csv'
df = pd.read_csv(url)


# In[2]:


df['new_price'] = df['item_price'].str[1:].astype('float')
df.head()


# ### 38. 데이터 중 choice_description 값이 NaN 인 데이터를 NoData 값으로 대체하라(loc 이용)***

# In[24]:


df.loc[:,'choice_description'] 


# In[29]:


df.choice_description.isnull()


# In[32]:


df.choice_description


# In[30]:


df.choice_description.isnull().sum()


# In[31]:


df.loc[df.choice_description.isnull(),'choice_description'] = 'Nodata'
df.head()


# 39. df의 데이터 중 choice_description 값에 Black이 들어가는 경우를 인덱싱

# In[39]:


df.loc[df.choice_description.str.contains('Black')]


# 40. df의 데이터 중 choice_description 값에 Vegetables 들어가지 않는 경우의 갯수를 출력

# In[45]:


df[-df.choice_description.str.contains("Vegetables")]


# In[51]:


df[-df.choice_description.str.contains("Vegetables")].shape


# In[52]:


len(df[-df.choice_description.str.contains("Vegetables")])


# 41. df의 데이터 중 item_name 값이 N으로 시작하는 데이터를 모두 추출

# In[55]:


df.item_name


# In[58]:


df[df.item_name.str.startswith('N')]


# ### 42. df의 데이터 중 item_name 값의 단어갯수가 15개 이상인 데이터를 인덱싱***

# In[75]:


df.item_name.str.len()


# In[76]:


df[df.item_name.str.len()>=15]


# 43. df의 데이터 중 new_price값이 lst에 해당하는 경우의 데이터 프레임을 구하고 그 갯수를 출력하라 lst =[1.69, 2.39, 3.39, 4.45, 9.25, 10.98, 11.75, 16.98]

# In[77]:


lst =[1.69, 2.39, 3.39, 4.45, 9.25, 10.98, 11.75, 16.98]


# In[83]:


df[df.new_price.isin(lst)]


# In[84]:


len(df[df.new_price.isin(lst)])


# ## 03_Grouping

# In[85]:


뉴욕 airBnB : https://www.kaggle.com/ptoscano230382/air-bnb-ny-2019 


# In[87]:


DataUrl = 'https://raw.githubusercontent.com/Datamanim/pandas/main/AB_NYC_2019.csv'


# 44.데이터를 로드하고 상위 5개 컬럼을 출력

# In[89]:


df = pd.read_csv(DataUrl)
df.head()


# 45. 데이터의 각 host_name의 빈도수를 구하고 host_name으로 정렬하여 상위 5개를 출력

# In[113]:


df.groupby('host_name')['host_name'].count().head()


# ### 46.데이터의 각 host_name의 빈도수를 구하고 빈도수 기준 내림차순 정렬한 데이터 프레임을 만들어라. 빈도수 컬럼은 counts로 명명하라**

# In[121]:


pd.DataFrame(df.groupby('host_name')['host_name'].count(), columns = ['count'])


# In[125]:


df.groupby('host_name').size().to_frame().rename(columns = {0:'counts'}).sort_values('counts',ascending=False)


# In[128]:


df.groupby('host_name').size().to_frame().rename(columns={0:'counts'})


# ### 47. neighbourhood_group의 값에 따른 neighbourhood컬럼 값의 갯수***

# In[129]:


df.head()


# In[138]:


df.groupby(['neighbourhood_group','neighbourhood'], as_index = False).size()


# ### 48. neighbourhood_group의 값에 따른 neighbourhood컬럼 값 중 neighbourhood_group그룹의 최댓값들을 출력***

# In[144]:


df.groupby(['neighbourhood_group','neighbourhood'], as_index = False).size().groupby(['neighbourhood_group'], as_index=False).max()


# 49. neighbourhood_group 값에 따른 price값의 평균, 분산, 최대, 최소값

# In[151]:


df.groupby(['neighbourhood_group','price'], as_index = False).size().groupby(['neighbourhood_group']).describe()


# In[157]:


df[['neighbourhood_group','price']].groupby('neighbourhood_group').agg(['mean','var','max','min'])


# 50. neighbourhood_group 값에 따른 reviews_per_month 평균, 분산, 최대, 최소값

# In[158]:


df.head()


# In[160]:


df[['neighbourhood_group','reviews_per_month']].groupby('neighbourhood_group').agg(['mean','var','max','min'])


# 51. neighbourhood 값과 neighbourhood_group 값에 따른 price 의 평균

# In[161]:


df[['neighbourhood','neighbourhood_group','price']].groupby(['neighbourhood','neighbourhood_group']).mean()


# In[163]:


df.groupby(['neighbourhood','neighbourhood_group']).price.mean()


# ### 52.neighbourhood 값과 neighbourhood_group 값에 따른 price 의 평균을 계층적 indexing 없이 구하기***

# In[166]:


pd.pivot_table(df, index=['neighbourhood'], columns = ['neighbourhood_group'], values = ['price'], aggfunc = ['mean'])


# In[169]:


df.groupby(['neighbourhood','neighbourhood_group']).price.mean().unstack()


# In[ ]:




