#!/usr/bin/env python
# coding: utf-8

# ## 02 Filtering & sorting

# In[42]:


import pandas as pd
url ='https://raw.githubusercontent.com/Datamanim/pandas/main/chipo.csv'
df = pd.read_csv(url)


# In[2]:


df.head()


# In[43]:


df['new_price'] = df['item_price'].str[1:].astype('float')
df.head()


# ### 30. df의 짝수번째 컬럼만을 포함하는 데이터프레임을 출력***

# In[26]:


df.iloc[:,::2]


# In[27]:


df.iloc[:,:]


# In[28]:


df.shape[0]  #전체 행수


# In[30]:


df.shape


# In[33]:


df.iloc[0] # data의 첫번째 행만


# In[36]:


df.iloc[-1] # 마지막 행만


# In[37]:


df.iloc[:,0] # 첫번째 열만


# In[38]:


df.iloc[:,-1]  # 마지막째 열만


# In[4]:


df.iloc[:,:] #전체


# In[5]:


df.iloc[::2,:]   # 짝수행


# In[6]:


df.iloc[:,::2]   # 짝수열


# 31. df의 new_price컬럼값에 따라 내림차순으로 정리, index 초기화

# In[14]:


df.sort_values('new_price', ascending=False).reset_index(drop=True)


# 32. df의 item_name 컬럼 값이 Steak Salad 또는 Bowl 인 데이터를 인덱싱

# In[22]:


df[(df['item_name']=='Steak Salad')|(df['item_name']=='Bowl')]


# ### 33.df의 item_name 컬럼 값이 Steak Salad 또는 Bowl 인 데이터를 데이터 프레임화 한 후, item_name를 기준으로 중복행이 있으면 제거하되 첫번째 케이스만 남겨라***

# In[23]:


df_n = df[(df['item_name']=='Steak Salad')|(df['item_name']=='Bowl')]


# In[27]:


df_n.drop_duplicates(['item_name'])


# ### 34. df의 item_name 컬럼 값이 Steak Salad 또는 Bowl 인 데이터를 데이터 프레임화 한 후, item_name를 기준으로 중복행이 있으면 제거하되 마지막 케이스만 남겨라***

# In[28]:


df_n.drop_duplicates('item_name', keep='last')


# 35. df의 데이터 중 new_price값이 new_price값의 평균값 이상을 가지는 데이터들을 인덱싱

# In[32]:


import numpy as np


# In[33]:


df[df.new_price >= np.mean(df.new_price)]


# ### 36.df의 데이터 중 item_name의 값이 Izze 데이터를 Fizzy Lizzy로 수정***

# In[40]:


df.item_name.replace("lzze","Fizzy Lizzy", inplace=True)   # 안 됨


# In[44]:


df.loc[df.item_name =="Izze", 'item_name'] = 'Fizzy Lizzy'
df.head(3)


# 37. df의 데이터 중 choice_description 값이 NaN 인 데이터의 갯수

# In[46]:


df.choice_description.isnull().sum()


# In[ ]:




