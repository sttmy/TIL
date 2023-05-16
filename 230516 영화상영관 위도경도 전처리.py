#!/usr/bin/env python
# coding: utf-8

# ## 영화상영관 위치

# In[1]:


import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from matplotlib import pyplot as plt
import datetime as dt
import seaborn as sns

# 한글폰트설치
from matplotlib import font_manager, rc
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus'] = False   # 마이너스 표시
plt.rc('font', family = 'Malgun Gothic')


# In[2]:


theater = pd.read_csv('Data/afterpreprocessing/TheaterWhere.csv')
theater.head()


# In[3]:


theater['영업상태명'].unique()


# In[4]:


theaterOpen = theater[theater['영업상태명'] == '영업/정상']


# In[5]:


theaterOpen = theaterOpen[['사업장명','소재지전체주소','위도','경도']]
theaterOpen


# In[6]:


theaterOpen.isna().sum()


# In[7]:


theaterNan = theaterOpen[theaterOpen['위도'].isna()].drop_duplicates(['소재지전체주소'])
theaterNan = theaterNan.drop_duplicates(['사업장명'])


# In[8]:


theaterNan.drop(index = [673,796,820,1368], inplace = True)


# In[9]:


theaterNan[['소재지전체주소']]


# In[10]:


theaterNan[theaterNan['소재지전체주소'].str.contains('층')]['소재지전체주소']


# In[11]:


" ".join(theaterNan[theaterNan['소재지전체주소'].str.contains('층')]['소재지전체주소'][580].split(' ')[:-1])


# In[12]:


theaterNan[theaterNan['소재지전체주소'].str.contains('필지')]['소재지전체주소'][1367].split('외')[:-1]


# In[13]:


theaterOpen.사업장명.nunique(), theaterOpen.위도.nunique()


# In[14]:


import folium

map = folium.Map(location=[theaterOpen.위도.mean(), theaterOpen.경도.mean()],
                zoom_start=12)

for i in theaterOpen.index:
    folium.Circle(radisu=300,
                 location=[theaterOpen.위도[i], theaterOpen.경도[i]],
                 popup=folium.Popup(theaterOpen.소재지전체주소[i], max_width=200),
                 tooltip=theaterOpen.사업장명[i],
                 color='blue',
                 fill=True,
                 fill_color = '#3186cc').add_to(map)
title='<h3 align="center" style="font-size:20"> 영화상영관위치 </h3>'
map.get_root().html.add_child(folium.Element(title))
map


# In[ ]:




