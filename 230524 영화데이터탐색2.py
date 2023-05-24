#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime as dt
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm

# 한글폰트설치
from matplotlib import font_manager, rc
import matplotlib as mpl


# In[2]:


mpl.rcParams['axes.unicode_minus'] = False   # 마이너스 표시
plt.rc('font', family = 'Malgun Gothic')


# In[14]:


Movies = pd.read_csv('Data/Movies_등급수정.csv')


# In[9]:


Movies.head()


# In[15]:


# 개봉일, 기준일 타입 변경
Movies['개봉일'] = Movies['개봉일'].astype('datetime64[ns]')
Movies['기준일'] = pd.to_datetime(Movies['기준일'])


# ## 등급별 비율

# In[19]:


# 전체영화 등급
movie_cum = Movies.drop_duplicates('영화명', keep = 'last')
movie_cum_num = movie_cum.groupby('등급s').size()


# In[20]:


# 액션영화 등급
actions = movie_cum[movie_cum.장르.str.contains('액션')]
actions_num = actions.groupby('등급s').size()


# In[21]:


fig = plt.figure(figsize = (15,5))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

colors = sns.color_palette("Set3")
explode = [0.02, 0.02, 0.02, 0.02, 0.02]

ax1.pie(movie_cum_num.values, labels = movie_cum_num.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors, shadow = True, explode = explode)

ax2.pie(actions_num.values, labels = actions_num.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors, shadow = True, explode = explode)
ax1.set_title('영화등급별 비율')
ax2.set_title('액션영화 등급별 비율')
plt.show()


# In[42]:


# 2004년 이후 개봉영화, 등급 미정 제외, 히트맵
movie_cum_20y = movie_cum[movie_cum.개봉연도>=2004]
movie_cum_20y = movie_cum_20y[movie_cum_20y['등급s'] != '미정']
movie_pv = movie_cum_20y.pivot_table('누적관객수','등급s','개봉연도')
plt.figure(figsize = (15,8))
plt.title('영화등급별 누적관객수 히트맵')

sns.heatmap(movie_pv, cmap='PuRd', annot = True, annot_kws ={'size':10}, linewidths = 1)


# ### 100만이상 영화 등급별 비교

# In[574]:


# 100만이상 영화 비율
print('전체 영화의 100만이상 영화 비율: ', len(million)/len(movie_cum))
print('액션 영화의 100만이상 영화 비율: ', len(million_action)/len(movie_cum[movie_cum.장르.str.contains('액션')]))


# In[43]:


# 관객수 100만 이상 영화 등급
million = movie_cum[movie_cum.누적관객수>=1000000]
million_num = million.groupby('등급s').size()

# 액션, 관객수 100만 이상 영화
million_action = movie_cum[movie_cum.장르.str.contains('액션')][movie_cum.누적관객수>=1000000]
million_action_num = million_action.groupby('등급s').size()


# In[44]:


fig = plt.figure(figsize = (15,5))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

colors = sns.color_palette("Set3")

ax1.pie(million_num.values, labels = million_num.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors, shadow = True)

ax2.pie(million_action_num.values, labels = million_action_num.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors, shadow = True)
ax1.set_title('100만이상 영화 등급별 비율')
ax2.set_title('100만이상 액션영화 등급별 비율')
plt.show()


# In[47]:


# 2004년 이후 개봉영화, 등급 미정 제외, 누적관객수 100만 이상 히트맵
movie_million_20y = million[million.개봉연도>=2004]
movie_million_20y = movie_million_20y[movie_million_20y['등급s'] != '미정']
movie_pv = movie_million_20y.pivot_table('누적관객수','등급s','개봉연도')
plt.figure(figsize = (15,8))
plt.title('영화등급별 누적관객수(100만 이상) 히트맵')

sns.heatmap(movie_pv, cmap='PuRd', annot = True, annot_kws ={'size':10}, linewidths = 1)


# In[ ]:


# 2004년 이후 개봉영화, 등급 미정 제외, 히트맵
movie_million_20y = million[million.개봉연도>=2004]
movie_million_20y = movie_million_20y[movie_million_20y['등급s'] != '미정']
movie_pv = movie_million_20y.pivot_table('누적관객수','등급s','개봉연도')
plt.figure(figsize = (15,8))
plt.title('영화등급별 누적관객수(100만 이상) 히트맵')

sns.heatmap(movie_pv, cmap='PuRd', annot = True, annot_kws ={'size':10}, linewidths = 1)


# ## 개봉월

# In[577]:


# 액션영화 월별 개봉현황
action = Movies[Movies.장르.str.contains('액션')]
action.reset_index()
action_month_num = action.groupby('개봉월').size()
action_month = action_month_num.index


# In[603]:


# 관객수 100만 이상 영화
million = movie_cum[movie_cum.누적관객수>=1000000]
million_month = million.groupby('개봉월').size()

# 액션, 관객수 100만 이상 영화
million_action = movie_cum[movie_cum.장르.str.contains('액션')][movie_cum.누적관객수>=1000000]
million_action_month = million_action.groupby('개봉월').size()


# In[631]:


fig = plt.figure(figsize = (12,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

colors1 = ['silver','whitesmoke', 'silver','silver', 'silver','whitesmoke',
          'whitesmoke', 'silver','gold','silver','gold', 'gold']
explode1 = [0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
          0.02, 0.05, 0.05, 0.05, 0.1, 0.1]
ax1.pie(movie_month_num, labels = movie_month, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors1,
        explode = explode1, shadow = True)

colors2 = ['whitesmoke','silver', 'whitesmoke','gold', 'silver','gold',
          'goldenrod', 'gold', 'gold','whitesmoke','whitesmoke','gold']
explode2 = [0.02, 0.02, 0.02, 0.1, 0.02, 0.05,
          0.1, 0.05, 0.05, 0.02, 0.02, 0.1]
ax2.pie(action_month_num, labels = action_month, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors2,
        explode = explode2, shadow = True)


colors3 = ['gold','whitesmoke', 'whitesmoke','whitesmoke','gold', 'silver',
          'goldenrod','gold','gold','silver','whitesmoke', 'goldenrod']
explode3 = [0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
          0.1, 0.05, 0.05, 0.02, 0.02, 0.1]
ax3.pie(million_month, labels = million_month.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors3,
        explode = explode3, shadow = True)

colors4 = ['silver','whitesmoke', 'silver','gold', 'goldenrod','goldenrod',
          'goldenrod','gold', 'silver','whitesmoke','whitesmoke', 'gold']
explode4 = [0.02, 0.02, 0.02, 0.05, 0.1, 0.1,
          0.1, 0.05, 0.02, 0.02, 0.02, 0.05]
ax4.pie(million_action_month, labels = million_action_month.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors4,
        explode = explode4, shadow = True)


ax1.set_title('Movie Release Month')
ax2.set_title('Action Movie Release Month')
ax3.set_title('Movie over 1 million Release Month')
ax4.set_title('Action Movie over 1 million Release Month')

plt.show()


# ## 개봉요일

# In[579]:


# 액션영화 개봉요일
action_day_num = action.groupby('개봉요일').size()
action_day = action.groupby('개봉요일').size().index


# In[580]:


# 관객수 100만 이상 영화
million = movie_cum[movie_cum.누적관객수>=1000000]
million_day = million.groupby('개봉요일').size()

# 액션, 관객수 100만 이상 영화
million_action = movie_cum[movie_cum.장르.str.contains('액션')][movie_cum.누적관객수>=1000000]
million_action_day = million_action.groupby('개봉요일').size()


# In[581]:


fig = plt.figure(figsize = (12,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

# colors = ['#ff9999','#ffc000','#d395d0', '#99FF66','#66CCFF']
colors = sns.color_palette('Pastel1')
wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

ax1.pie(movie_day_num, labels = movie_day, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors,
        shadow = True, wedgeprops = wedgeprops)
ax2.pie(action_day_num, labels = action_day, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors,
        shadow = True, wedgeprops = wedgeprops)
ax3.pie(million_day, labels = million_day.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors =colors,
        shadow = True, wedgeprops = wedgeprops)
ax4.pie(million_action_day, labels = million_action_day.index, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors =colors,
        shadow = True, wedgeprops = wedgeprops)

ax1.set_title('Movie Release Day')
ax2.set_title('Action Movie Release Day')
ax3.set_title('Movie over 1 million Release Day')
ax4.set_title('Action Movie over 1 million Release Day')
plt.show()


# ## 개봉연도

# In[582]:


# 관객수 100만 이상 영화
million = movie_cum[movie_cum.누적관객수>=1000000]
million_year = million.groupby('개봉연도').size()

# 액션, 관객수 100만 이상 영화
million_action = movie_cum[movie_cum.장르.str.contains('액션')][movie_cum.누적관객수>=1000000]
million_action_year = million_action.groupby('개봉연도').size()


# In[586]:


Year = pd.concat([pd.DataFrame(million_year), pd.DataFrame(million_action_year)], axis = 1)
Year.columns = ['전체영화','액션영화']
Year.info()


# In[595]:


Year.dropna(inplace = True)
Year.액션영화 = Year.액션영화.astype('int64')


# In[600]:


Year['비율'] = Year.액션영화 / Year.전체영화


# In[601]:


Year


# In[627]:


ax = sns.barplot(data = Year, x = Year.index, y = round(Year.비율,3))

for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2, height, 
            height, ha = 'center', size = 9)    
plt.title('연도별 액션영화 비율(누적관객수 100만 이상)')
plt.show()


# ## 개봉일차별 누적관객수 / 관객수 비교

# In[48]:


Movies.개봉일차.describe()


# In[49]:


Movies[Movies.장르.str.contains('액션')].개봉일차.describe()


# ### 전체영화 TOP10

# In[129]:


# 전체영화 TOP10 이름
movie10_name = Movies.sort_values(['영화명','누적관객수'],ascending = False).drop_duplicates('영화명').sort_values('누적관객수',ascending = False).head(10).영화명.values

# 전체영화 TOP10 데이터프레임
Movies10 = pd.DataFrame()
for i in range(0,10):
    df = Movies[Movies.영화명 == movie10_name[i]]
    Movies10 = pd.concat([Movies10, df])
    
# 기준일 기준 정렬
Movies = Movies.sort_values(['영화명','기준일'])

# 개봉일차 100일까지만 추출
Movies10_100days = pd.DataFrame()
for i in range(0,10):
    m = Movies10[Movies10.영화명 == movie10_name[i]].loc[:,['개봉일차','누적관객수','관객수']].iloc[:100]
    Movies10_100days = pd.concat([Movies10_100days, m])


# In[137]:


개봉일차 = Movies10.개봉일차.iloc[:100,]
movie1 = Movies10_100days.iloc[:100,]
movie2 = Movies10_100days.iloc[100:200,]
movie3 = Movies10_100days.iloc[200:300,]
movie4 = Movies10_100days.iloc[300:400,]
movie5 = Movies10_100days.iloc[400:500,]
movie6 = Movies10_100days.iloc[500:600,]
movie7 = Movies10_100days.iloc[600:700,]
movie8 = Movies10_100days.iloc[700:800,]
movie9 = Movies10_100days.iloc[800:900,]
movie10 = Movies10_100days.iloc[900:1000,]


# In[138]:


# 누적관객수
fig = plt.figure(figsize = (15,8))

num_cm1 = movie1['누적관객수']
num_cm2 = movie2['누적관객수']
num_cm3 = movie3['누적관객수']
num_cm4 = movie4['누적관객수']
num_cm5 = movie5['누적관객수']
num_cm6 = movie6['누적관객수']
num_cm7 = movie7['누적관객수']
num_cm8 = movie8['누적관객수']
num_cm9 = movie9['누적관객수']
num_cm10 = movie10['누적관객수']

# 개봉일차별 누적관객수 추이
ax1 = plt.subplot()
color1 = sns.color_palette("PRGn",10)
ax1.set_title('Movie TOP10 개봉일차별 누적관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('누적관객수', fontsize = 14)

ax1.plot(개봉일차, num_cm1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm10, color = color1[9], marker='s', markersize=3)
# ax1.tick_params(axis = 'y')
cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend(movie10_name)
plt.show()


# In[154]:


m1 = movie1[movie1.관객수 == movie1.관객수.max()].개봉일차.values
m2 = movie2[movie2.관객수 == movie2.관객수.max()].개봉일차.values
m3 = movie3[movie3.관객수 == movie3.관객수.max()].개봉일차.values
m4 = movie4[movie4.관객수 == movie4.관객수.max()].개봉일차.values
m5 = movie5[movie5.관객수 == movie5.관객수.max()].개봉일차.values
m6 = movie6[movie6.관객수 == movie6.관객수.max()].개봉일차.values
m7 = movie7[movie7.관객수 == movie7.관객수.max()].개봉일차.values
m8 = movie8[movie8.관객수 == movie8.관객수.max()].개봉일차.values
m9 = movie9[movie9.관객수 == movie9.관객수.max()].개봉일차.values
m10 = movie10[movie10.관객수 == movie10.관객수.max()].개봉일차.values
m1, m2, m3, m4, m5, m6, m7, m8, m9, m10


# In[159]:


# 관객수
fig = plt.figure(figsize = (15,8))

num_cm1 = movie1['관객수']
num_cm2 = movie2['관객수']
num_cm3 = movie3['관객수']
num_cm4 = movie4['관객수']
num_cm5 = movie5['관객수']
num_cm6 = movie6['관객수']
num_cm7 = movie7['관객수']
num_cm8 = movie8['관객수']
num_cm9 = movie9['관객수']
num_cm10 = movie10['관객수']

# 개봉일차별 누적관객수 추이
ax1 = plt.subplot()
color1 = sns.color_palette("PRGn",10)
ax1.set_title('Movie TOP10 개봉일차별 관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('관객수', fontsize = 14)

ax1.plot(개봉일차, num_cm1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm10, color = color1[9], marker='s', markersize=3)

cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend(movie10_name)
plt.show()


# ### Action 영화 TOP10

# In[ ]:


Actions = Movies[Movies.장르.str.contains('액션')]


# In[61]:


# Action영화 TOP10 이름
action10_name = Actions.sort_values(['영화명','누적관객수'],ascending = False).drop_duplicates('영화명').sort_values('누적관객수',ascending = False).head(10).영화명.values

# Action영화 TOP10 데이터프레임
Actions10 = pd.DataFrame()
for i in range(0,10):
    df = Actions[Actions.영화명 == action10_name[i]]
    Actions10 = pd.concat([Actions10, df])
    
# 기준일 기준 정렬
Actions = Actions.sort_values(['영화명','기준일'])

# 개봉일차 100일까지만 추출
Actions10_100days = pd.DataFrame()
for i in range(0,10):
    m = Actions10[Actions10.영화명 == action10_name[i]].loc[:,['누적관객수','관객수']].iloc[:100]
    Actions10_100days = pd.concat([Actions10_100days, m])


# In[76]:


Actions10_100days.iloc[:100,]['누적관객수']


# In[86]:


# 누적관객수
fig = plt.figure(figsize = (15,8))

개봉일차 = Actions10.개봉일차.iloc[:100,]
num_cm1 = Actions10_100days.iloc[:100,]['누적관객수']
num_cm2 = Actions10_100days.iloc[100:200,]['누적관객수']
num_cm3 = Actions10_100days.iloc[200:300,]['누적관객수']
num_cm4 = Actions10_100days.iloc[300:400,]['누적관객수']
num_cm5 = Actions10_100days.iloc[400:500,]['누적관객수']
num_cm6 = Actions10_100days.iloc[500:600,]['누적관객수']
num_cm7 = Actions10_100days.iloc[600:700,]['누적관객수']
num_cm8 = Actions10_100days.iloc[700:800,]['누적관객수']
num_cm9 = Actions10_100days.iloc[800:900,]['누적관객수']
num_cm10 = Actions10_100days.iloc[900:1000,]['누적관객수']

# 개봉일차별 누적관객수 추이
ax1 = plt.subplot()
# color1 = ['red','salmon','orange','gold','yellowgreen',
#           'darkgreen','cadetblue','skyblue', 'royalblue','darkblue']
color1 = sns.color_palette("BrBG",10)
ax1.set_title('Action Movie TOP10 개봉일차별 누적관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('누적관객수', fontsize = 14)

ax1.plot(개봉일차, num_cm1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm10, color = color1[9], marker='s', markersize=3)
# ax1.tick_params(axis = 'y')
cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend(action10_name)
plt.show()


# In[106]:


# 누적관객수
fig = plt.figure(figsize = (15,8))

개봉일차 = Actions10.개봉일차.iloc[:100,]
num_cm1 = Actions10_100days.iloc[:100,]['관객수']
num_cm2 = Actions10_100days.iloc[100:200,]['관객수']
num_cm3 = Actions10_100days.iloc[200:300,]['관객수']
num_cm4 = Actions10_100days.iloc[300:400,]['관객수']
num_cm5 = Actions10_100days.iloc[400:500,]['관객수']
num_cm6 = Actions10_100days.iloc[500:600,]['관객수']
num_cm7 = Actions10_100days.iloc[600:700,]['관객수']
num_cm8 = Actions10_100days.iloc[700:800,]['관객수']
num_cm9 = Actions10_100days.iloc[800:900,]['관객수']
num_cm10 = Actions10_100days.iloc[900:1000,]['관객수']

# 개봉일차별 누적관객수 추이
ax1 = plt.subplot()
color1 = sns.color_palette("BrBG",10)
ax1.set_title('Action Movie TOP10 개봉일차별 관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('관객수', fontsize = 14)

ax1.plot(개봉일차, num_cm1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, num_cm10, color = color1[9], marker='s', markersize=3)
# ax1.tick_params(axis = 'y')
cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend(action10_name)
plt.show()


# In[ ]:




