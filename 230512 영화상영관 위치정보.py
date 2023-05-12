#!/usr/bin/env python
# coding: utf-8

# ## 전국 영화상영관현황 

# In[2]:


import pandas as pd


# In[3]:


screen = pd.read_csv('Data/[공공데이터 행정안전부] 전국 영화상영관 현황(2023업데이트).csv', encoding='cp949')
screen.head()


# In[4]:


screen.columns


# In[5]:


screen.isna().sum()


# In[122]:


screen.소재지전체주소


# In[18]:


sc = screen[['인허가일자','인허가취소일자','영업상태명','소재지전체주소','사업장명','좌표정보(x)','좌표정보(y)','시설면적','최종수정시점']]
sc.info()


# In[19]:


sc.head()


# ### 카카오API로 위도경도값 불러오기

# In[11]:


import requests
from urllib.parse import quote
from tqdm.notebook import tqdm


# In[9]:


filename = 'kakao_API.txt'
with open(filename) as f:
    api_key = f.read()


# In[13]:


lng_list = []
lat_list = []

for i in tqdm(range(0, len(sc.index))):
    search_url = "https://dapi.kakao.com/v2/local/search/address.json"
    addr = str(sc.소재지전체주소[i])
    url = f'{search_url}?query={quote(addr)}'
    result = requests.get(url, headers={"Authorization": f'KakaoAK {api_key}'}).json()
    try:
        lng = float(result['documents'][0]['x'])
        lat = float(result['documents'][0]['y'])
        lng_list.append(lng)
        lat_list.append(lat)
    except:
        lng_list.append('nan')
        lat_list.append('nan')


# In[20]:


# 4936
len(lat_list), len(lng_list), lat_list, lng_list


# In[21]:


sc.head()


# In[22]:


sc['위도'] = lat_list
sc['경도'] = lng_list
sc.head()


# In[24]:


sc.isna().sum()


# In[25]:


# 영화관(사업장명) 이름 정제하기
import re
sc.사업장명


# In[26]:


# 정규식을 적용하여 숫자+관 부분 제거
data = [re.sub('\d+관', '', x) for x in sc.사업장명]
# ' 제' 제거
data = [re.sub(' 제', '', x) for x in data]
sc.사업장명 = data
sc.사업장명


# In[27]:


# 위치정보 NaN 제거
sc_del = sc.dropna(subset=['위도'], how = 'any', axis = 0)
sc_del.isna().sum()


# In[28]:


# 중복 제거하기
df_uniq = sc_del.drop_duplicates(['사업장명'])
df_uniq.head()


# In[29]:


df_uniq = df_uniq[['사업장명','소재지전체주소','위도','경도','영업상태명','인허가일자','인허가취소일자']]


# In[30]:


df_uniq.head()


# In[33]:


df_uniq[df_uniq['영업상태명'] == '영업/정상']


# In[34]:


df_uniq.to_csv('Data/TheaterWhere.csv',index = False)

