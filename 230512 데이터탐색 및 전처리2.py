#!/usr/bin/env python
# coding: utf-8

# # 일별 영화 집계

# In[3]:


import pandas as pd
import numpy as np
from tqdm.notebook import tqdm


# In[4]:


movieList = pd.read_excel('Data/afterpreprocessing/(완)영화정보 리스트_개봉일자(2017~2023).xlsx')
movieList.head()


# In[5]:


movieList.shape


# In[6]:


movieList.groupby('제작국가').size()


# In[7]:


movieList.groupby('제작사').size()


# In[8]:


movieTop = pd.read_excel('Data/afterpreprocessing/(완)역대_박스오피스(2023.05.11).xlsx')
movieTop.head()


# In[9]:


movieTop.groupby('배급사').size().sort_values(ascending = False)


# In[10]:


theater = pd.read_csv('Data/afterpreprocessing/TheaterWhere.csv')
theater.head()


# In[11]:


theater['영업상태명'].unique()


# In[12]:


theaterOpen = theater[theater['영업상태명'] == '영업/정상']


# In[13]:


theaterOpen = theaterOpen[['사업장명','소재지전체주소','위도','경도']]
theaterOpen


# In[14]:


theaterOpen.소재지전체주소.nunique()


# In[15]:


theaterOpen.사업장명.nunique()


# In[16]:


ticketPrice = pd.read_excel('Data/afterpreprocessing/TicketPrice.xlsx')
ticketPrice.head()


# In[17]:


movieStat = pd.read_excel('Data/afterpreprocessing/MovieStat_Top200.xlsx')
movieStat.head()


# In[18]:


movies = pd.read_csv('Data/afterpreprocessing/완_기간별_일별_170101_to_230509_ver1.csv')
movies.shape


# In[19]:


movies.head(2)


# In[20]:


movies = movies[['개봉일','순위','영화명','대표국적','제작사','배급사','등급','장르','매출액','관객수','스크린수','상영횟수']]
movies.head(2)


# In[21]:


movies.info()


# In[22]:


movies.개봉일.unique()


# In[20]:


movies.copy().개봉일


# In[ ]:


for i in tqdm(movies.index):
    try: 
        movies.개봉일[i] = movies.copy().개봉일[i].split(' ')[0]
    except: 
        pass    
movies.to_csv('Data/afterpreprocessing/dailyMovieList.csv')


# **** copy()해서 원본과 분리하면 warning이 사라짐

# In[ ]:


movies.개봉일


# In[ ]:





# In[58]:


len(set(movies.개봉일))


# In[ ]:


# movieList : 전체영화리스트
# movieTop : top200개 영화
# movieStat : top200개 영화 통계정보
# movies : 일별 영화 (2017~)
# ticketPrice : 티켓가격추이
# theater : 영화상영관 위치


# In[12]:


movieTop.매출액.replace(',','', inplace = True, regex = True)
movieTop.관객수.replace(',','', inplace = True, regex = True)
movieTop.스크린수.replace(',','', inplace = True, regex = True)
movieTop.상영횟수.replace(',','', inplace = True, regex = True)


# In[13]:


top = top.astype({'매출액': 'float64','관객수':'int64','스크린수':'int64','상영횟수':'int64'})


# In[15]:


from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


# In[17]:


num = top[['매출액','관객수','스크린수','상영횟수']]
num.columns = ['sales','attendance','screens','runnum']
num.describe()


# In[18]:


std = StandardScaler()
stdscaling = std.fit_transform(num)
stdscaling = pd.DataFrame(stdscaling, columns=num.columns)
stdscaling.describe()


# In[24]:


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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




