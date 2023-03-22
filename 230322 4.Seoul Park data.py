#!/usr/bin/env python
# coding: utf-8

# ### 서울 주요 공원, 지도에 표시
# 서울시 주요 공원현황.csv

# In[40]:


import pandas as pd
import json
import folium
import re
import numpy as np


# In[77]:


df = pd.read_csv('./Data/서울시 주요 공원현황.csv', encoding = 'EUC-KR')
df.head()  


# In[4]:


# 위도, 경도값 사용 예정 (X좌표, Y좌표)


# In[5]:


df.info()


# In[9]:


df.shape


# ### 1.공원 면적 정리

# In[33]:


area = df.면적.astype(str).apply(lambda x: x.strip('총 ').split()[0])    #'총 '제거, 공백지우고 [0]
area[-5:]


# In[34]:


area.unique()


# In[35]:


area[(area == 'nan') | (area == '휴양')]


# In[36]:


area[(area == 'nan') | (area == '휴양')] = '0㎡'


# In[27]:


area.unique()


# In[38]:


# ㎡,m²,m2 등 단위표시가 모두 다르므로 정규표현식으로 제거
area.apply(lambda x: re.sub('[㎡m²㎥]','',x))     #리스트가 아니므로 ','쓰지 않음
area = area.apply(lambda x: float(re.sub('[㎡m²㎥]','',x)))  # 실수형으로 변환
area


# In[39]:


area.unique()


# In[42]:


area = area.apply(lambda x: int(np.round(x)))
area


# ### 2. 공원의 면적에 따라 분류

# In[43]:


area_criteria = [-1, 100000, 1000000, 12000000]


# In[49]:


# cut함수를 활용해, 소형 0~100000 / 중형 ~1000000 / 대형 ~ 으로 분류

labels = ['소형', '중형','대형']
pd.cut(area, area_criteria, labels = labels)


# In[50]:


### tch
labels = ['소형', '중형','대형']
size_info = [3, 7, 15]   # label에 따라 반지름 사이즈 달리 표기
scale = pd.cut(area, area_criteria, labels = labels)
size = pd.cut(area, area_criteria, labels = size_info)


# In[51]:


size[:5]


# In[52]:


scale[:5]


# ### 3.새로운 프레임 만들기

# In[53]:


df.head()


# In[54]:


df.info()


# In[78]:


df = df[['공원명','지역','X좌표(WGS84)','Y좌표(WGS84)']]
df.columns = ['공원명','지역','경도','위도']
df.head(3)


# In[79]:


df = pd.concat([df,area,scale,size], axis = 1)
df.columns = ['공원명','지역','경도','위도','면적','분류','크기']
df.head(3)


# In[ ]:


### tch
df['면적'] = area
df['분류'] = scale
df['크기'] = size


# In[80]:


df.isnull().sum()


# In[81]:


# 결측치가 있음. 확인
df[df.지역.isna()]


# In[82]:


df[df.경도.isna()]


# In[83]:


# 모두 빼기로 결정

df = df.dropna()


# In[84]:


df.to_csv('./data1/서울공원요약.csv', index = False)


# In[85]:


df.head()


# ### 4. 공원시각화

# In[89]:


map = folium.Map(location=[df.위도.mean(),df.경도.mean()], zoom_start=15)
folium.TileLayer('cartodbpositron').add_to(map)    

for i in df.index:
    folium.Circle(radius = 300, 
                  location = [df.위도[i], df.경도[i]],
                  popup = folium.Popup(df.지역[i]),
                  tooltip = f"{df.공원명[i]}({df.면적[i]: ,d})㎡",
                  color = 'crimson',
                  fill_color = 'crimson').add_to(map)
# 부수적 옵션    
# title = '<h3 align = "center" style = "font-size:20"> 서울공원요약 </h3>'
# map_gu.get_root().html.add_child(folium.Element(title))
map


# In[95]:


# tch
map2 = folium.Map(location=[37.5502,126.982], zoom_start=15)

for i in df.index:
    folium.CircleMarker(radius = int(df.크기[i]),
                  location = [df.위도[i], df.경도[i]],
                  tooltip = f"{df.공원명[i]}({df.면적[i]: ,d})㎡",
                  color = 'crimson',
                  fill_color = 'crimson').add_to(map2)
map2


# In[ ]:




