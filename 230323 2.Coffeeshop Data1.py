#!/usr/bin/env python
# coding: utf-8

# # 소상공인데이터
# 
# 소상공인시장진흥공단_상가(상권)정보_(지역)_202112.csv
# 
# https://www.data.go.kr/
# 
# 카토그램 그려보기

# In[32]:


import numpy as np
import pandas as pd
from glob import glob
from tqdm.notebook import tqdm   # for문 불러올 때, loading bar로 진행현황 확인 가능


# In[33]:


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))


# ## 커피지수 part1

# ### 데이터로부터 4개 커피숍 정보 추출

# In[34]:


data_dir ='./Data/소상공인'    # 폴더 전체를 불러옴
df = pd.read_csv(f'{data_dir}/소상공인시장진흥공단_상가(상권)정보_서울_202112.csv')
df.head(3)


# In[35]:


df.shape


# In[36]:


# 업종중분류코드   Q12 : 카페/커피숍

df = df[df.상권업종중분류코드 == 'Q12']
df.head(3)


# In[37]:


df.columns


# In[38]:


df = df[['상호명','지점명','시도명','시군구명']]
df.head(3)


# In[39]:


df.상호명.unique(), df.상호명.nunique()


# In[40]:


# 스타벅스 커피숍
sb = df[df.상호명.str.contains('스타벅스|STARBUKS', case = False)]    #case: 대소문자 구분여부, default는 True,대소문자 구분함
sb


# In[20]:


sb.isnull().sum()


# In[21]:


# '지점명' 변수에, '스타벅스'가 없는 데이터 검색
df[df.지점명.str.contains('스타벅스|STARBUKS', case = False, na = False)]    # na = False 는 Nan이 존재할 경우 False로 치환


# In[41]:


# 커피빈 커피숍
cb = df[df.상호명.str.contains('커피빈|COFFEEBEAN', case = False)]  
cb.head()


# In[43]:


df[df.지점명.str.contains('커피빈|COFFEEBEAN', case = False, na = False)]  


# In[49]:


# 이디야 커피숍
ed = df[df.상호명.str.contains('이디야|EDIYACOFFEE', case = False)]  
ed.head()


# In[45]:


df[df.지점명.str.contains('이디야|EDIYACOFFEE', case = False, na = False)]  


# In[46]:


# 빽다방 커피숍
pk = df[df.상호명.str.contains('빽다방|PAIKSCOFFEE', case = False)]  
pk.head()


# In[47]:


df[df.지점명.str.contains('빽다방|PAIKSCOFFEE', case = False, na = False)]  


# In[50]:


len(sb), len(cb), len(ed), len(pk)


# ## 전국 데이터에서 4개 매장 정보 추출

# In[66]:


# 빈 데이터프레임 만들기

starbucks = pd.DataFrame(columns = ['상호명','시도명','시군구명'])
coffeebean = pd.DataFrame(columns = ['상호명','시도명','시군구명'])
ediya = pd.DataFrame(columns = ['상호명','시도명','시군구명'])
paik = pd.DataFrame(columns = ['상호명','시도명','시군구명'])


# In[67]:


# 디렉토리내 데이터파일을 for문으로 전처리하면서 불러오기

for file in tqdm(glob(f'{data_dir}/*.csv')):   #data_dir 폴더에서 csv파일은 모두 불러와라, tqdm으로 불러오기 실시간 현황 파악
    df = pd.read_csv(file, low_memory = False)
    df = df[df.상권업종중분류코드 == 'Q12']
    df = df[['상호명','시도명','시군구명']]
    
    sb = df[df.상호명.str.contains('스타벅스|STARBUCKS', case = False)]
    cb = df[df.상호명.str.contains('커피빈|COFFEEBEAN', case = False)]
    ed = df[df.상호명.str.contains('이디야|EDIYA', case = False)]
    pk = df[df.상호명.str.contains('빽다방|PAIKSCOFFEE', case = False)]
    
    starbucks = pd.concat([starbucks, sb])
    coffeebean = pd.concat([coffeebean, cb])
    ediya = pd.concat([ediya, ed])
    paik = pd.concat([paik, pk])    


# In[68]:


starbucks.shape, coffeebean.shape, ediya.shape, paik.shape


# In[69]:


starbucks.head()


# In[71]:


starbucks.to_csv('./data1/스타벅스.csv', index = False)
coffeebean.to_csv('./data1/커피빈.csv', index = False)
ediya.to_csv('./data1/이디야.csv', index = False)
paik.to_csv('./data1/빽다방.csv', index = False)


# In[72]:


pd.read_csv('./data1/스타벅스.csv')


# In[73]:


starbucks.to_csv('./data1/스타벅스1.csv')   


# In[74]:


pd.read_csv('./data1/스타벅스1.csv')     #index = False 는, index를 변수로 저장하지 않겠다는 뜻


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




