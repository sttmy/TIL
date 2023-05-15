#!/usr/bin/env python
# coding: utf-8

# # 일별 영화 집계

# In[3]:


import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from matplotlib import pyplot as plt
import datetime as dt


# In[4]:


movieList = pd.read_excel('Data/afterpreprocessing/(완)영화정보 리스트_개봉일자(2017~2023).xlsx')
movieList.head()


# In[3]:


movieList.shape


# In[4]:


movieList.groupby('제작국가').size()


# In[7]:


movieList.groupby('제작사').size()


# In[11]:


consumerPrice = pd.read_excel('Data/[KOSIS] 지출목적별_소비자물가지수_품목포함__2020100__20230515104059.xlsx')
consumerPrice.head()


# In[12]:


consumerPrice.drop(['시도별'],axis = 1, inplace = True)


# In[13]:


cp = consumerPrice.T
cp.columns = cp.iloc[0]


# In[14]:


cp.drop(['지출목적별'], inplace = True)


# In[15]:


cp.head()


# In[129]:


cp.iloc[0]


# In[16]:


entertain_cp = cp.iloc[:,9]
entertain_cp.head()


# In[17]:


et_cp = entertain_cp.to_frame()
et_cp.head(2)


# In[18]:


et_cp.columns = [['entertain_price']]
et_cp.info()


# In[19]:


et_cp


# In[21]:


ticketPrice = pd.read_excel('Data/afterpreprocessing/TicketPrice.xlsx')
ticketPrice.head()


# In[24]:


ticketPrice.shape


# **loc: LOCation (label이나 boolean array로 인덱싱)    
# 
# df.loc[행 인덱싱 값, 열 인덱싱 값]
# 
# df.loc[0] index이름 0만 추출
# 
# df.loc[0,'Name'] index이름 0, column이름 Name 추출
# 
# 
# **iloc: Integer LOCation    
# 
# df.iloc[0] 전체df중에서 0번째 행값만 추출

# In[22]:


ticketMode = ticketPrice.loc[:,::4]
ticketMin = ticketPrice.iloc[:,1:14:4]
ticketMedian = ticketPrice.iloc[:,2::4]
ticketMax = ticketPrice.iloc[:,3::4]


# In[23]:


ticketMode.info()


# In[24]:


tm = ticketMode.set_index(ticketMode['Unnamed: 0'])


# In[25]:


tm.drop(['Unnamed: 0'], axis = 1, inplace = True)


# In[26]:


tm['mode'] = tm.mean(axis = 1)


# In[229]:


tm['mode']


# In[27]:


et_cp.entertain_price


# In[30]:


fig = plt.figure(figsize = (15,5))
# fig, ax1 = plt.subplots()
ax1 = plt.subplot()
color_1 = 'tab:blue'
ax1.set_title('Price transition', fontsize = 20)
ax1.set_xlabel('Month')
ax1.set_ylabel('Ticket Price', fontsize = 14, color = color_1)
ax1.plot(tm.index, tm['mode'], color = color_1, marker='s', markersize=3)
ax1.tick_params(axis = 'y', labelcolor = color_1)

ax2 = ax1.twinx()
color_2 = 'tab:red'
ax2.set_ylabel('Entertainment Price Index', fontsize = 14, color = color_2)
ax2.plot(tm.index, et_cp.entertain_price, color = color_2, marker = 'o', markersize=3)
ax2.tick_params(axis = 'y', labelcolor = color_2)
plt.axhline(100, color = 'gray', linestyle = 'solid')

fig.tight_layout()
plt.show()


# In[131]:


movies = pd.read_csv('Data/afterpreprocessing/완_기간별_일별_170101_to_230509_ver1.csv')
movies.shape


# In[252]:


movies.head(2)


# In[132]:


movies = movies[['개봉일','순위','영화명','대표국적','제작사','배급사','등급','장르','매출액','관객수','스크린수','상영횟수']]
movies.head(2)


# In[133]:


movies.info()


# In[136]:


movies.개봉일 = pd.to_datetime(movies.개봉일)
movies.info()


# In[ ]:





# In[ ]:


# movieList : 전체영화리스트
# movieTop : top200개 영화
# movieStat : top200개 영화 통계정보
# movies : 일별 영화 (2017~)
# ticketPrice : 티켓가격추이
# theater : 영화상영관 위치


# #TOP200 영화 ==============================================================

# In[218]:


# TOP200 : 관객수기준 
movieTop = pd.read_excel('Data/afterpreprocessing/(완)역대_박스오피스(2023.05.11).xlsx')
movieTop.head()


# In[231]:


movieTop['영화명'] = movieTop['영화명'].astype('str')


# In[232]:


movieTop[movieTop['영화명'] == '1987']


# In[237]:


movieTop[movieTop['영화명'] == '좋은 놈, 나쁜 놈, 이상한 놈']


# In[233]:


movieTop.info()


# In[154]:


movieStat = pd.read_csv('Data/afterpreprocessing/MovieStat_Top200_수정.csv')
movieStat.head()


# In[32]:


movieStat['movie name'].nunique()


# In[234]:


# 상영일수 합
movieDays = movieStat.groupby('movie name').size()
movieDays.sort_values(ascending = False)
movieDays = movieDays.to_frame()
movieDays.reset_index(inplace = True)
movieDays.columns = ['영화명','상영일수']
movieDays.info()


# In[294]:


movieDays['영화명'].unique()


# In[290]:


movieDays[movieDays.loc[:,'영화명'] == '좋은 놈, 나쁜 놈, 이상한 놈 ']


# In[292]:


movieDays.iloc[156,0] = '좋은 놈, 나쁜 놈, 이상한 놈'


# In[293]:


movieDays.iloc[156,0]


# In[428]:


movieTop_add = pd.merge(movieTop, movieDays, how = 'inner', on = '영화명')
movieTop_add.info()


# In[429]:


movieTop_add.head()


# In[432]:


movieTop.shape


# In[342]:


# 영화별 1위 일수


# In[437]:


rank = movieStat[['TOP200','movie name','순위']]
rank


# In[391]:


rank[rank['TOP200'] == 1].groupby('순위').size().index[0]


# In[392]:


rank[rank['TOP200'] == 1].groupby('순위').size().iloc[0]


# In[393]:


rank[rank['TOP200'] == 200]


# In[394]:


rank[rank['TOP200'] == 200].groupby('순위').size()


# In[438]:


movieRank = []
movieRank1Days = []
for i in range(1,201):
    movieRank.append(rank[rank['TOP200'] == i].groupby('순위').size().index[0])
    movieRank1Days.append(rank[rank['TOP200'] == i].groupby('순위').size().iloc[0])


# In[439]:


len(movieRank)


# In[440]:


movieTop_add['최고순위'] = movieRank


# In[441]:


movieTop_add['최고순위일수'] = movieRank1Days
movieTop_add.head()


# In[442]:


movieTop_add.to_csv('Data/movieTop_add0515.csv', index= False)


# In[444]:


movieTop_add = pd.read_csv('Data/movieTop_add0515.csv')


# In[445]:


ticket = tm['mode'].to_frame()
ticket.reset_index(inplace = True)
ticket.columns = ['일자','관람료']
ticket.info()


# In[454]:


movieTop_add['개봉일'] = pd.to_datetime(movieTop_add['개봉일'])


# In[456]:


movieTop_add['개봉월'] = movieTop_add['개봉일'].dt.strftime('%Y-%m')


# In[457]:


movieTop_add.head()


# In[458]:


ticket['개봉월'] = ticket['일자'].dt.strftime('%Y-%m')


# In[459]:


ticket.head()


# In[462]:


pd.merge(movieTop_add, ticket, how = 'left', on = '개봉월')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[37]:


# 상영횟수 합
movieNums = movieStat[['movie name','상영횟수']].groupby(['movie name']).sum()
movieNums.sort_values(by = '상영횟수', ascending = False)


# In[42]:


# 관객수 합
movieAudiences = movieStat[['movie name','관객수']].groupby(['movie name']).sum()
movieAudiences.sort_values(by = '관객수', ascending = False)


# In[286]:


# 매출액 합
movieSales = movie_stat.groupby(['movie name']).sum()['매출액']


# In[43]:


movieS = pd.concat([movieTop, movieDays], axis = 1)


# In[46]:


movieTop


# In[145]:





# In[257]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





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


# In[7]:


theater = pd.read_csv('Data/afterpreprocessing/TheaterWhere.csv')
theater.head()


# In[8]:


theater['영업상태명'].unique()


# In[9]:


theaterOpen = theater[theater['영업상태명'] == '영업/정상']


# In[10]:


theaterOpen = theaterOpen[['사업장명','소재지전체주소','위도','경도']]
theaterOpen


# In[70]:


theaterOpen.isna().sum()


# In[ ]:


theaterNan = theaterOpen[theaterOpen['위도'].isna()].drop_duplicates(['소재지전체주소'])
theaterNan = theaterNan.drop_duplicates(['사업장명'])


# In[104]:


theaterNan.drop(index = [673,796,820,1368], inplace = True)


# In[94]:


theaterNan[['소재지전체주소']]


# In[108]:


theaterNan[theaterNan['소재지전체주소'].str.contains('층')]['소재지전체주소']


# In[114]:


" ".join(theaterNan[theaterNan['소재지전체주소'].str.contains('층')]['소재지전체주소'][580].split(' ')[:-1])


# In[130]:


theaterNan[theaterNan['소재지전체주소'].str.contains('필지')]['소재지전체주소'][1367].split('외')[:-1]


# In[ ]:


lambda x: " ".join(x.split(' ')[:-1]) if 


# In[71]:


theaterOpen.소재지전체주소.nunique()


# In[73]:


theaterOpen.사업장명.nunique(), theaterOpen.위도.nunique()


# In[68]:


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




