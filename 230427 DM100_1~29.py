#!/usr/bin/env python
# coding: utf-8

# # 데이터마님 전처리 100문제
# 
# https://www.datamanim.com/dataset/99_pandas/pandasMain.html

# ## 01 Getting & Knowing Data

# In[1]:


dataUrl = 'https://raw.githubusercontent.com/Datamanim/pandas/main/lol.csv'


# In[3]:


import pandas as pd
df = pd.read_csv(dataUrl, sep='\t')


# In[4]:


df.head()


# In[6]:


df.shape


# In[7]:


df.columns


# In[9]:


df.columns[5]


# ### 6. 데이터 타입

# In[10]:


type(df.columns[5])


# In[13]:


df.describe()


# In[14]:


df.info()


# In[29]:


df['firstBlood'].dtype


# In[30]:


df[df.columns[5]].dtype


# In[31]:


df.index


# In[34]:


df[df.columns[5]][2]


# ### 9. 데이터 로드, 컬럼 한글 처리 ****

# In[49]:


Dataurl = "https://raw.githubusercontent.com/Datamanim/pandas/main/Jeju.csv"
df2= pd.read_csv(Dataurl, encoding = 'euc-kr')


# In[39]:


df2.tail(3)


# ### 11. 수치형 변수 가진 컬럼 출력 ******
# ### 12. 범주형 변수 가진 컬럼 출력 ******

# In[51]:


df2.info()


# In[56]:


df2.info(type == object)


# In[63]:


df2.columns[0], df2.columns[4]


# In[78]:


df2.select_dtypes(exclude=object).columns


# In[79]:


df2.select_dtypes(object).columns


# ### 13. 각 컬럼 결측치 숫자 ***

# In[90]:


df2.isnull().sum()


# In[91]:


df2.info()


# In[92]:


df2.describe()


# In[93]:


df2['거주인구']


# ### 17. 평균 속도 컬럼의 4분위 범위 IQR

# In[103]:


df2['평균 속도'].quantile(.75) - df2['평균 속도'].quantile(.25)


# In[114]:


df2['읍면동명'].nunique(), df2['읍면동명'].unique()


# In[113]:


df2['읍면동명'].nunique()


# ## 02 Filtering & Sorting

# In[168]:


url ='https://raw.githubusercontent.com/Datamanim/pandas/main/chipo.csv'
df = pd.read_csv(url)


# In[116]:


type(df)


# In[117]:


df.info()


# In[122]:


df[df['quantity'] == 3].head()


# ### 22. quantity 컬럼 값이 3인 데이터 추출, index를 0부터 정렬하고 첫 5행 출력 ***

# In[127]:


df.loc[df['quantity'] == 3].head().reset_index(drop=True)
# drop=True 로 설정하면 기존 인덱스 열을 버림


# 23.quantity , item_price 두개의 컬럼으로 구성된 새로운 데이터 프레임을 정의

# In[146]:


new_df = pd.DataFrame(df[['quantity','item_price']])
type(new_df), new_df


# ### 24. item_price컬럼의 달러표시 문자를 제거하고 float 타입으로 저장하여 new_price컬럼에 저장 ***

# In[147]:


new_df['new_price'] = str(new_df['item_price']).replace("$","")  # 안 됨
new_df


# In[150]:


new_df['item_price'].str[1:]


# In[151]:


new_df['new_price'] = new_df['item_price'].str[1:].astype('float')
new_df['new_price'].head()


# 25. new_price 컬럼이 5 이하의 값을 가지는 df를 추출, 전체 갯수?

# In[153]:


len(new_df[new_df['new_price'] <= 5]), new_df[new_df['new_price'] <= 5]


# 26. item_name명이 Chicken Salad Bowl인 df을 추출하라고 index값을 초기화

# In[156]:


df[df['item_name']=='Chicken Salad Bowl'].reset_index(drop=True)


# 27. new_price값이 9 이하이고 item_name 값이 Chicken Salad Bowl인 데이터 프레임 추출

# In[169]:


df['new_price'] = df['item_price'].str[1:].astype('float')


# In[160]:


df[(df['new_price'] <=9) & (df['item_name'] == 'Chicken Salad Bowl')]


# 28. df의 new_price컬럼값에 따라 오름차순으로 정리, index 초기화

# In[164]:


df.sort_values(by=['new_price'], ascending=True).reset_index(drop=True)


# ### 29. df의 item_name 컬럼 값중 Chips 포함하는 데이터 출력 ***

# In[172]:


df[df.item_name.str.contains('Chips')]

