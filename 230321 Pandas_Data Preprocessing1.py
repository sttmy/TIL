#!/usr/bin/env python
# coding: utf-8

# ### Groupby

# In[1]:


import pandas as pd
import seaborn as sns
import numpy as np


# In[4]:


df = pd.read_csv('./Data/titanic.csv')
df = df[['Survived','Pclass','Sex','Age','Embarked']]
df = df.dropna()
df.head()


# In[10]:


df.isnull().sum()


# In[7]:


# 성별 통계
df_s1 = df.groupby('Sex').Survived.count().to_frame()
df_s1.columns = ['승선자수']
df_s1


# In[8]:


# 성별 생존자통계
df_s2 = df.groupby('Sex').Survived.sum().to_frame()
df_s2.columns = ['생존자수']
df_s2


# In[11]:


# 성별 생존률
df_s3 = df.groupby('Sex').Survived.mean().to_frame()
df_s3.columns = ['생존률']
df_s3


# In[13]:


pd.concat([df_s1, df_s2, df_s3], axis = 1)


# In[15]:


# 성별, 객실등급별 생존률
df_s4 = (df.groupby(['Sex','Pclass']).Survived.mean().to_frame()).round(3)
df_s4.columns = ['생존률']
df_s4


# #### 사용자정의 함수 활용

# In[18]:


# 내가만든(사용자정의)함수 적용, agg(사용자정의함수, 매개변수)
# 함수선언

def my_mean(values):
    return sum(values) / len(values)


# In[19]:


df_s5 = df.groupby(['Sex','Pclass']).Survived.agg(my_mean).to_frame
df_s5

