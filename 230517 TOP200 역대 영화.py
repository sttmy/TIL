#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# # TOP200 역대 영화 통계

# In[65]:


movieTop_add = pd.read_csv('Data/movieTop_add.csv')
movieTop_add.head()


# In[74]:


# 개봉월
movie_month_num = movieTop_add.groupby('개봉월').size()
movie_month = movie_month_num.index


# ### TOP200 영화 개봉월 

# In[76]:


fig = plt.figure(figsize = (4,4))
colors = ['gold','whitesmoke', 'whitesmoke','whitesmoke', 'silver','silver',
          'goldenrod', 'gold', 'silver','silver','whitesmoke','goldenrod']
# explode = np.full((1,12), 0.1)[0]
explode = [0.05, 0.02, 0.02, 0.02, 0.02, 0.02,
          0.1, 0.05, 0.02, 0.02, 0.02, 0.1]
plt.pie(movie_month_num, labels = movie_month, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors,
        explode = explode, shadow = True)
plt.title('Movie Release Month')
plt.show()


# ### TOP200 영화 개봉요일

# In[77]:


movie_day_num = movieTop_add.groupby('개봉요일').size()
movie_day = movieTop_add.groupby('개봉요일').size().index


# In[78]:


fig = plt.figure(figsize = (4,4))
colors = ['#ff9999','#ffc000','#d395d0']
wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
plt.pie(movie_day_num, labels = movie_day, autopct = '%.1f%%', 
        startangle = 90, counterclock = False, colors = colors,
        shadow = True, wedgeprops = wedgeprops)
plt.title('Movie Release Day')
plt.show()


# ### Top200 영화 개봉일차별 추이

# In[82]:


movieStat = pd.read_csv('Data/afterpreprocessing/MovieStat_Top200_수정.csv')


# In[90]:


# 개봉일차 컬럼 생성
개봉일차 = []
for i in range(1,201):
    m = movieStats[movieStats.TOP200 == i]
    for j in range(0,len(m)):
        개봉일차.append(f'{j+1}일차')
movieStat['개봉일차'] = 개봉일차

# 불필요한 컬럼 제외
movieStats = movieStat[['TOP200','movie name','날짜','관객수','누적관객수','매출액','누적매출액','순위', '개봉일차']]


# In[84]:


# TOP200 영화의 최저 상영일수가 47일 >> 40일차씩 잘라서 비교
np.min(movieTop_add.상영일수), np.mean(movieTop_add.상영일수), np.max(movieTop_add.상영일수)


# In[91]:


movieStats[movieStats.TOP200 == 20].iloc[:40,[0,1,3,4,5,6,7,8]]


# In[92]:


# 개봉 40일차까지 비교
movie40days = pd.DataFrame()
for i in range(1,201):
    m = movieStats[movieStats.TOP200 == i].iloc[:40,[0,1,3,4,5,6,7,8]]
    movie40days = pd.concat([movie40days, m])

# '일차' 삭제
movie40days['개봉일차'] = movie40days['개봉일차'].apply(lambda x : x.replace('일차',''))


# In[112]:


# 개봉 100일차까지 비교, TOP10까지만
movie100days = pd.DataFrame()
for i in range(1,11):
    m = movieStats[movieStats.TOP200 == i].iloc[:100,[0,1,3,4,5,6,7,8]]
    movie100days = pd.concat([movie100days, m])

# '일차' 삭제
movie100days['개봉일차'] = movie100days['개봉일차'].apply(lambda x : x.replace('일차',''))


# In[114]:


len(movie100days)


# In[110]:


# 개봉일차별 순위 vs 관람객수 비교
개봉일차 = movie40days['개봉일차'].iloc[:40,]
rank = movie40days.iloc[:40,]['순위']
num = movie40days.iloc[:40,]['관객수']
name = movie40days.iloc[0,]['movie name']

rank2 = movie40days.iloc[40:80,]['순위']
num2 = movie40days.iloc[40:80,]['관객수']
name2 = movie40days.iloc[40,]['movie name']

rank3 = movie40days.iloc[80:120,]['순위']
num3 = movie40days.iloc[80:120,]['관객수']
name3 = movie40days.iloc[80,]['movie name']

### 개봉일차별 관객수추이 및 순위 비교
fig = plt.figure(figsize = (12,5))

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color_1 = 'tab:red'
ax1.set_title('TOP1, TOP2, TOP3 Movie 개봉일차별 순위 및 관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차')
ax1.set_ylabel('순위', fontsize = 14, color = color_1)
ax1.plot(개봉일차, rank, color = color_1, marker='s', markersize=3)
ax1.plot(개봉일차, rank2, color = 'orange', marker='s', markersize=3)
ax1.plot(개봉일차, rank3, color = 'gold', marker='s', markersize=3)
ax1.tick_params(axis = 'y', labelcolor = color_1)
plt.gca().invert_yaxis()

# 관람객수
ax2 = ax1.twinx()
color_2 = 'darkgreen'
ax2.set_ylabel('관람객수', fontsize = 14, color = color_2)
ax2.plot(개봉일차, num, color = color_2, marker = 'o', markersize=3)
ax2.plot(개봉일차, num2, color = 'lightgreen', marker = 'o', markersize=3)
ax2.plot(개봉일차, num3, color = 'yellowgreen', marker = 'o', markersize=3)
ax2.tick_params(axis = 'y', labelcolor = color_2)

cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend([name, name2, name3, 'TOP1', 'TOP2', 'TOP3'])
fig.tight_layout()
plt.show()


# In[144]:


# 개봉일차별 순위 vs 관람객수 비교
개봉일차 = movie40days['개봉일차'].iloc[:40,]
rank = movie40days.iloc[:40,]['순위']
num = movie40days.iloc[:40,]['관객수']
num_cm = movie40days.iloc[:40,]['누적관객수']
name = movie40days.iloc[0,]['movie name']

rank2 = movie40days.iloc[40:80,]['순위']
num2 = movie40days.iloc[40:80,]['관객수']
num_cm2 = movie40days.iloc[40:80,]['누적관객수']
name2 = movie40days.iloc[40,]['movie name']

rank3 = movie40days.iloc[80:120,]['순위']
num3 = movie40days.iloc[80:120,]['관객수']
num_cm3 = movie40days.iloc[80:120,]['누적관객수']
name3 = movie40days.iloc[80,]['movie name']

### 개봉일차별 관객수추이 및 순위 비교
fig = plt.figure(figsize = (12,5))

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color_1 = 'tab:red'
ax1.set_title('TOP1, TOP2, TOP3 Movie 개봉일차별 순위 및 누적관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차')
ax1.set_ylabel('순위', fontsize = 14, color = color_1)
ax1.plot(개봉일차, rank, color = color_1, marker='s', markersize=3)
ax1.plot(개봉일차, rank2, color = 'orange', marker='s', markersize=3)
ax1.plot(개봉일차, rank3, color = 'gold', marker='s', markersize=3)
ax1.tick_params(axis = 'y', labelcolor = color_1)
plt.gca().invert_yaxis()

# 관람객수
# ax2 = ax1.twinx()
# color_2 = 'darkgreen'
# ax2.set_ylabel('관람객수', fontsize = 14, color = color_2)
# ax2.plot(개봉일차, num, color = color_2, marker = 'o', markersize=3)
# ax2.plot(개봉일차, num2, color = 'lightgreen', marker = 'o', markersize=3)
# ax2.plot(개봉일차, num3, color = 'yellowgreen', marker = 'o', markersize=3)
# ax2.tick_params(axis = 'y', labelcolor = color_2)

# 누적관람객수
ax2 = ax1.twinx()
color_2 = 'darkgreen'
ax2.set_ylabel('누적관람객수', fontsize = 14, color = color_2)
ax2.plot(개봉일차, num_cm, color = color_2, marker = 'o', markersize=3)
ax2.plot(개봉일차, num_cm2, color = 'lightgreen', marker = 'o', markersize=3)
ax2.plot(개봉일차, num_cm3, color = 'yellowgreen', marker = 'o', markersize=3)
ax2.tick_params(axis = 'y', labelcolor = color_2)
cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend([name, name2, name3, 'TOP1', 'TOP2', 'TOP3'])
fig.tight_layout()
plt.show()


# In[95]:


## 1~10위 영화 이름
movieName = []
for i in range(0,10):
    movieName.append(str(movieTop_add.iloc[:10,]['순위'].values[i]) +'위 '+ movieTop_add.iloc[:10,]['영화명'].values[i])


# ### TOP200 영화 개봉일차별 관객수 추이 비교

# In[108]:


fig = plt.figure(figsize = (15,8))

개봉일차 = movie40days['개봉일차'].iloc[:40,]
num1 = movie40days.iloc[:40,]['관객수']
num2 = movie40days.iloc[40:80,]['관객수']
num3 = movie40days.iloc[80:120,]['관객수']
num4 = movie40days.iloc[120:160,]['관객수']
num5 = movie40days.iloc[160:200,]['관객수']
num6 = movie40days.iloc[200:240,]['관객수']
num7 = movie40days.iloc[240:280,]['관객수']
num8 = movie40days.iloc[280:320,]['관객수']
num9 = movie40days.iloc[320:360,]['관객수']
num10 = movie40days.iloc[360:400,]['관객수']

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color1 = ['red','salmon','orange','gold','yellowgreen',
          'darkgreen','cadetblue','skyblue', 'royalblue','darkblue']
color2 = ['tab:red','tab:orange','tab:olive','tab:green','tab:cyan',
          'tab:blue','tab:purple','tab:pink','tab:brown','tab:gray']
color = ['maroon','brown','indianred','lightcoral','rosybrown',
          'lightpink','rosybrown','salmon','orangered','red']
ax1.set_title('TOP10 Movie 개봉일차별 관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('관객수', fontsize = 14)

ax1.plot(개봉일차, num1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, num2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, num3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, num4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, num5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, num6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, num7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, num8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, num9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, num10, color = color1[9], marker='s', markersize=3)
# ax1.tick_params(axis = 'y')
cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend(movieName)
plt.show()


# In[117]:


fig = plt.figure(figsize = (15,8))

개봉일차 = movie100days['개봉일차'].iloc[:100,]
num1 = movie100days.iloc[:100,]['관객수']
num2 = movie100days.iloc[100:200,]['관객수']
num3 = movie100days.iloc[200:300,]['관객수']
num4 = movie100days.iloc[300:400,]['관객수']
num5 = movie100days.iloc[400:500,]['관객수']
num6 = movie100days.iloc[500:600,]['관객수']
num7 = movie100days.iloc[600:700,]['관객수']
num8 = movie100days.iloc[700:800,]['관객수']
num9 = movie100days.iloc[800:900,]['관객수']
num10 = movie100days.iloc[900:1000,]['관객수']

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color1 = ['red','salmon','orange','gold','yellowgreen',
          'darkgreen','cadetblue','skyblue', 'royalblue','darkblue']
color2 = ['tab:red','tab:orange','tab:olive','tab:green','tab:cyan',
          'tab:blue','tab:purple','tab:pink','tab:brown','tab:gray']
color = ['maroon','brown','indianred','lightcoral','rosybrown',
          'lightpink','rosybrown','salmon','orangered','red']
ax1.set_title('TOP10 Movie 100일간 관람객수 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('관객수', fontsize = 14)

ax1.plot(개봉일차, num1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, num2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, num3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, num4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, num5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, num6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, num7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, num8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, num9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, num10, color = color1[9], marker='s', markersize=3)
# ax1.tick_params(axis = 'y')
cv = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cv])

plt.legend(movieName)
plt.show()


# In[111]:


fig = plt.figure(figsize = (15,8))

개봉일차 = movie40days['개봉일차'].iloc[:40,]
num_cm1 = movie40days.iloc[:40,]['누적관객수']
num_cm2 = movie40days.iloc[40:80,]['누적관객수']
num_cm3 = movie40days.iloc[80:120,]['누적관객수']
num_cm4 = movie40days.iloc[120:160,]['누적관객수']
num_cm5 = movie40days.iloc[160:200,]['누적관객수']
num_cm6 = movie40days.iloc[200:240,]['누적관객수']
num_cm7 = movie40days.iloc[240:280,]['누적관객수']
num_cm8 = movie40days.iloc[280:320,]['누적관객수']
num_cm9 = movie40days.iloc[320:360,]['누적관객수']
num_cm10 = movie40days.iloc[360:400,]['누적관객수']

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color1 = ['red','salmon','orange','gold','yellowgreen',
          'darkgreen','cadetblue','skyblue', 'royalblue','darkblue']
color2 = ['tab:red','tab:orange','tab:olive','tab:green','tab:cyan',
          'tab:blue','tab:purple','tab:pink','tab:brown','tab:gray']
color = ['maroon','brown','indianred','lightcoral','rosybrown',
          'lightpink','rosybrown','salmon','orangered','red']
ax1.set_title('TOP10 Movie 개봉일차별 누적관람객수 비교', fontsize = 20)
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

plt.legend(movieName)
plt.show()


# In[118]:


fig = plt.figure(figsize = (15,8))

개봉일차 = movie100days['개봉일차'].iloc[:100,]
num_cm1 = movie100days.iloc[:100,]['누적관객수']
num_cm2 = movie100days.iloc[100:200,]['누적관객수']
num_cm3 = movie100days.iloc[200:300,]['누적관객수']
num_cm4 = movie100days.iloc[300:400,]['누적관객수']
num_cm5 = movie100days.iloc[400:500,]['누적관객수']
num_cm6 = movie100days.iloc[500:600,]['누적관객수']
num_cm7 = movie100days.iloc[600:700,]['누적관객수']
num_cm8 = movie100days.iloc[700:800,]['누적관객수']
num_cm9 = movie100days.iloc[800:900,]['누적관객수']
num_cm10 = movie100days.iloc[900:1000,]['누적관객수']

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color1 = ['red','salmon','orange','gold','yellowgreen',
          'darkgreen','cadetblue','skyblue', 'royalblue','darkblue']
color2 = ['tab:red','tab:orange','tab:olive','tab:green','tab:cyan',
          'tab:blue','tab:purple','tab:pink','tab:brown','tab:gray']
color = ['maroon','brown','indianred','lightcoral','rosybrown',
          'lightpink','rosybrown','salmon','orangered','red']
ax1.set_title('TOP10 Movie 개봉일차별 누적관람객수 비교', fontsize = 20)
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

plt.legend(movieName)
plt.show()


# ### TOP200 영화 개봉일차별 일일순위 비교

# In[109]:


fig = plt.figure(figsize = (15,8))

개봉일차 = movie40days['개봉일차'].iloc[:40,]
rank1 = movie40days.iloc[:40,]['순위']
rank2 = movie40days.iloc[40:80,]['순위']
rank3 = movie40days.iloc[80:120,]['순위']
rank4 = movie40days.iloc[120:160,]['순위']
rank5 = movie40days.iloc[160:200,]['순위']
rank6 = movie40days.iloc[200:240,]['순위']
rank7 = movie40days.iloc[240:280,]['순위']
rank8 = movie40days.iloc[280:320,]['순위']
rank9 = movie40days.iloc[320:360,]['순위']
rank10 = movie40days.iloc[360:400,]['순위']

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color1 = ['red','salmon','orange','gold','yellowgreen',
          'darkgreen','cadetblue','skyblue', 'royalblue','darkblue']
color2 = ['tab:red','tab:orange','tab:olive','tab:green','tab:cyan',
          'tab:blue','tab:purple','tab:pink','tab:brown','tab:gray']
color = ['darkblue','mediumblue','blue','royalblue','dodgerblue',
          'deepskyblue','darkturquoise','aqua','paleturquoise','cadetblue']
ax1.set_title('TOP10 Movie 개봉일차별 순위 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('순위', fontsize = 14)

ax1.plot(개봉일차, rank1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, rank2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, rank3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, rank4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, rank5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, rank6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, rank7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, rank8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, rank9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, rank10, color = color1[9], marker='s', markersize=3)
ax1.tick_params(axis = 'y')
plt.gca().invert_yaxis()

plt.legend(movieName)
plt.show()


# In[143]:


fig = plt.figure(figsize = (15,8))

개봉일차 = movie100days['개봉일차'].iloc[:100,]
rank1 = movie100days.iloc[:100,]['순위']
rank2 = movie100days.iloc[100:200,]['순위']
rank3 = movie100days.iloc[200:300,]['순위']
rank4 = movie100days.iloc[300:400,]['순위']
rank5 = movie100days.iloc[400:500,]['순위']
rank6 = movie100days.iloc[500:600,]['순위']
rank7 = movie100days.iloc[600:700,]['순위']
rank8 = movie100days.iloc[700:800,]['순위']
rank9 = movie100days.iloc[800:900,]['순위']
rank10 = movie100days.iloc[900:1000,]['순위']

# 개봉일차별 순위 추이
ax1 = plt.subplot()
color1 = ['red','salmon','orange','gold','yellowgreen',
          'darkgreen','cadetblue','skyblue', 'royalblue','darkblue']
color2 = ['tab:red','tab:orange','tab:olive','tab:green','tab:cyan',
          'tab:blue','tab:purple','tab:pink','tab:brown','tab:gray']
color = ['darkblue','mediumblue','blue','royalblue','dodgerblue',
          'deepskyblue','darkturquoise','aqua','paleturquoise','cadetblue']
ax1.set_title('TOP10 Movie 개봉일차별 순위 비교', fontsize = 20)
ax1.set_xlabel('개봉일차', fontsize = 14)
ax1.set_ylabel('순위', fontsize = 14)

ax1.plot(개봉일차, rank1, color = color1[0], marker='s', markersize=3)
ax1.plot(개봉일차, rank2, color = color1[1], marker='s', markersize=3)
ax1.plot(개봉일차, rank3, color = color1[2], marker='s', markersize=3)
ax1.plot(개봉일차, rank4, color = color1[3], marker='s', markersize=3)
ax1.plot(개봉일차, rank5, color = color1[4], marker='s', markersize=3)
ax1.plot(개봉일차, rank6, color = color1[5], marker='s', markersize=3)
ax1.plot(개봉일차, rank7, color = color1[6], marker='s', markersize=3)
ax1.plot(개봉일차, rank8, color = color1[7], marker='s', markersize=3)
ax1.plot(개봉일차, rank9, color = color1[8], marker='s', markersize=3)
ax1.plot(개봉일차, rank10, color = color1[9], marker='s', markersize=3)
ax1.tick_params(axis = 'y')
plt.gca().invert_yaxis()
plt.xticks(range(0,100,2), fontsize=8)

plt.legend(movieName)
plt.show()


# ### TOP200 상영횟수와 매출액의 상관관계

# In[120]:


x = movieTop_add.매출액
y = movieTop_add.상영횟수


# In[124]:


np.random.seed(0)
colors = np.random.rand(200)
# area = (30 * np.random.rand(200)**2)
plt.scatter(x, y, c = colors)
plt.xlabel('매출액', fontsize=10)
plt.ylabel('상영횟수', fontsize=10)
plt.xlim(0, x.sort_values(ascending = False)[0]+ x.sort_values(ascending = False)[0]/10)
cv = plt.gca().get_xticks()
plt.gca().set_xticklabels(['{:,.0f}'.format(x) for x in cv], rotation = 45)

plt.show()


# In[ ]:





# # Top200 영화 통계치 비교

# In[113]:


fig = plt.figure(figsize = (15,5))
index = movieTop_add.영화명
label = movieTop_add.매출액
plt.bar(index, label)
plt.title('Sales of Top200 Movies', fontsize=16)
plt.xlabel('Movie', fontsize=10)
plt.ylabel('Sales of movies', fontsize=10)
plt.xticks(index, label, fontsize=15)
plt.show()


# In[114]:


movieTop30 = movieTop_add.iloc[:30,]
movieTop50 = movieTop_add.iloc[:50,]


# In[115]:


movie = movieTop50.영화명.values
sales = movieTop50.매출액
aud = movieTop50.관객수.values
days = movieTop50.상영일수.values
cnt = movieTop50.상영횟수.values


# In[139]:


# 상영일수
plt.figure(figsize = (10,7))
plt.barh(movie, days, height = 0.5, label = 'Sales', color = 'g')
plt.gca().invert_yaxis()
plt.title('Top50 Movies의 상영일수', fontsize=16)
plt.xlabel('상영일수', fontsize=10)
plt.ylabel('Movie', fontsize=10)
plt.xlim(0, days.max() + days.max()/10)
plt.show()


# In[138]:


# 상영횟수
plt.figure(figsize = (10,7))
plt.barh(movie, cnt, height = 0.5, label = 'Sales', color = 'r')
plt.gca().invert_yaxis()
plt.title('Top50 Movies의 상영횟수', fontsize=16)
plt.xlabel('상영횟수', fontsize=10)
plt.ylabel('Movie', fontsize=10)
plt.xlim(0, cnt.max() + cnt.max()/10)
plt.show()


# In[135]:


# 매출액
plt.figure(figsize = (10,7))
plt.barh(movie, sales, height = 0.5, label = 'Sales', color = 'b')
plt.gca().invert_yaxis()
plt.title('Sales of Top50 Movies', fontsize=16)
plt.xlabel('매출액', fontsize=10)
plt.ylabel('Movie', fontsize=10)
plt.xlim(0, sales.sort_values(ascending = False)[0]+ sales.sort_values(ascending = False)[0]/10)
cv = plt.gca().get_xticks()
plt.gca().set_xticklabels(['{:,.0f}'.format(x) for x in cv], rotation = 45)

plt.show()


# In[145]:


movieTop_add.to_excel('Data/movieTop_add(엑셀).xlsx')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




