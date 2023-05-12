#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# ## 04_Apply , Map

# 카드이용데이터 : https://www.kaggle.com/sakshigoyal7/credit-card-customers 

# 56. 데이터 로드하고 행과 열 갯수 출력

# In[2]:


DataUrl = 'https://raw.githubusercontent.com/Datamanim/pandas/main/BankChurnersUp.csv'
df = pd.read_csv(DataUrl)
df.head()


# In[3]:


df.shape


# In[4]:


df.describe()


# In[5]:


df.info()


# 57. Income_Category의 카테고리를 map 함수를 이용하여 다음과 같이 변경하여 newIncome 컬럼에 매핑하라 
# 
# Unknown : N
# 
# Less than $40K : a
# 
# $40K - $60K : b
# 
# $60K - $80K : c
# 
# $80K - $120K : d
# 
# $120K +’ : e

# In[6]:


df.Income_Category


# In[7]:


df.Income_Category.unique()


# In[8]:


df.groupby(df.Income_Category).size()


# In[36]:


x = pd.Series({'Unknown' : 'N', 'Less than $40K' : 'a',
               '$40K - $60K' : 'b', '$60K - $80K': 'c',
               '$80K - $120K' : 'd', '$120K +' : 'e'})


# In[10]:


df['newIncome'] = df.Income_Category.map(x)


# In[11]:


df.head()


# In[12]:


df.Income_Category.map(lambda a : x[a])


# ※ MAP함수
# 
# 인덱스에 따라서 값을 전환
# 
# Series에서만 사용할 수 있음. DataFrame에서는 join이나 replace 사용

# In[32]:


a = pd.Series({'one':1,'two':2,'three':3})
b = pd.Series({1:'triangle',2:'square',3:'circle'})
a


# In[33]:


a.map(b)


# In[34]:


b.map(a)


# In[35]:


a.apply(lambda v:v*2)


# In[18]:


# df에서는 column별: axis = 0 , row별: axis = 1

d = pd.DataFrame(np.arange(12).reshape(4,3), columns = ['a','b','c'])
d


# In[19]:


d.apply(lambda x:x.sum())


# In[20]:


d.apply(lambda x:x.sum(), axis = 1)


# In[21]:


d['a+b'] = d.apply(lambda x: x.a + x.b, axis = 1)
d


# In[22]:


d.applymap(lambda x:'%.2f'% x)


# In[23]:


d.applymap(lambda x: '%.2f'% x if (x > 5) else x)


# 58. Income_Category의 카테고리를 apply 함수를 이용하여 위와 같이 변경하여 newIncome 컬럼에 매핑하라

# In[24]:


x


# In[25]:


x[0]


# In[26]:


len(x)


# In[27]:


x.index[0]


# In[28]:


x.index


# In[29]:


x


# In[37]:


df['newIncome2'] = df.Income_Category.map(lambda v : x[v])
df.head()


# In[38]:


def changeCategory(x):
    if x =='Unknown':
        return 'N'
    elif x =='Less than $40K':
        return 'a'
    elif x =='$40K - $60K':   
        return 'b'
    elif x =='$60K - $80K':    
        return 'c'
    elif x =='$80K - $120K':   
        return 'd'
    elif x =='$120K +' :     
        return 'e'


# In[39]:


df['newIncome2'] = df.Income_Category.apply(changeCategory)
df.newIncome2


# 59.

# In[40]:


df['AgeState'] = df.Customer_Age.map(lambda x: x//10 *10)
df.groupby('AgeState').size()


# In[41]:


df.AgeState.value_counts().sort_index()


# 60.

# In[42]:


df.Education_Level.str.contains('Graduate')


# In[43]:


df.query('Education_Level.str.contains("Graduate")')


# In[44]:


word = ['Graduate']
df.Education_Level.map(lambda x: all(s in x for s in word))


# In[45]:


df['newEduLevel'] = df.Education_Level.map(lambda x: 1 if 'Graduate' in x else 0)
df['newEduLevel'].value_counts()


# In[46]:


df.groupby('newEduLevel').size()


# 61.

# In[47]:


df['newLimit'] = df.Credit_Limit.map(lambda x: 1 if x >= 4500 else 0)
df['newLimit'].value_counts()


# In[48]:


df.groupby('newLimit').size()


# 62.

# In[49]:


def check(x):
    if x.Marital_Status == 'Married' and x.Card_Category == 'Platinum':
        return 1
    else:
        return 0


# In[50]:


df['newState'] = df.apply(check, axis = 1)
df.newState.value_counts()


# 63.

# In[51]:


sex = {'M':'male','F':'female'}
df['gender'] = df.Gender.map(sex)
df.gender.value_counts()


# In[ ]:




