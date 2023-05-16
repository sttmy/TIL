#!/usr/bin/env python
# coding: utf-8

# In[525]:


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


# # 티켓가격 vs 소비자물가지수 비교

# ### 소비자물가지수 (오락 및 문화)

# In[526]:


consumerPrice = pd.read_excel('Data/[KOSIS] 지출목적별_소비자물가지수_품목포함__2020100__20230515104059.xlsx')
consumerPrice.head()


# In[527]:


consumerPrice.drop(['시도별'],axis = 1, inplace = True)
cp = consumerPrice.T
cp.columns = cp.iloc[0]
cp.drop(['지출목적별'], inplace = True)
cp.head()


# In[530]:


# 오락 및 문화 분야 소비자물가지수
entertain_cp = cp.iloc[:,9]
et_cp = entertain_cp.to_frame()
et_cp.columns = [['entertain_price']]
et_cp.head()


# ### 티켓가격

# In[532]:


ticketPrice = pd.read_excel('Data/afterpreprocessing/TicketPrice.xlsx')
ticketPrice.head()


# In[533]:


ticketPrice = ticketPrice.set_index(ticketPrice['Unnamed: 0'])
ticketPrice.drop(['Unnamed: 0'], axis = 1, inplace = True)


# In[534]:


ticketMode = ticketPrice.iloc[:,3::4]
ticketMin = ticketPrice.iloc[:,::4]
ticketMedian = ticketPrice.iloc[:,1:14:4]
ticketMax = ticketPrice.iloc[:,2::4]


# In[535]:


# 티켓 월별 최빈값
tm = ticketMode.copy()
tm['mean'] = tm.mean(axis = 1)
tm['trans_mean'] = tm['mean'] / (tm['mean'].iloc[24:36,].mean()/100)   # 2020년 평균을 100으로 변환

# 티켓 월별 최대값
tmax = ticketMax.copy()
tmax['mean'] = tmax.mean(axis = 1)
tmax['trans_mean'] = tmax['mean'] / (tmax['mean'].iloc[24:36,].mean()/100)

# 티켓 월별 최소값
tmin = ticketMin.copy()
tmin['mean'] = tmin.mean(axis = 1)
tmin['trans_mean'] = tmin['mean'] / (tmin['mean'].iloc[24:36,].mean()/100)

# 티켓 월별 중앙값
ticketMedian = ticketPrice.iloc[:,1:14:4]
tmed = ticketMedian.copy()
tmed['mean'] = tmed.mean(axis = 1)
tmed['trans_mean'] = tmed['mean'] / (tmed['mean'].iloc[24:36,].mean()/100)


# In[536]:


(tmax['mean'].iloc[24:36,].mean()/100), (tmax['trans_mean'].iloc[24:36,].mean())


# In[537]:


(tm['mean'].iloc[24:36,].mean()/100), (tm['trans_mean'].iloc[24:36,].mean())


# In[538]:


(tmin['mean'].iloc[24:36,].mean()/100), (tmin['trans_mean'].iloc[24:36,].mean())


# In[539]:


(tmed['mean'].iloc[24:36,].mean()/100), (tmed['trans_mean'].iloc[24:36,].mean())


# In[540]:


et_cp.entertain_price.iloc[24:36].mean()


# ### 시각화) 티켓가격 vs 오락문화 물가지수 단순비교

# In[541]:


fig = plt.figure(figsize = (15,5))

# 티켓가격 추이
ax1 = plt.subplot()
color_1 = 'tab:red'
ax1.set_title('Price transition', fontsize = 20)
ax1.set_xlabel('Month')
ax1.set_ylabel('Ticket Price', fontsize = 14, color = color_1)
ax1.plot(tm.index, tm['mean'], color = color_1, marker='s', markersize=3)
ax1.tick_params(axis = 'y', labelcolor = color_1)

# 오락문화 물가지수 추이
ax2 = ax1.twinx()
color_2 = 'darkgreen'
ax2.set_ylabel('Entertainment Price Index', fontsize = 14, color = color_2)
ax2.plot(tm.index, et_cp.entertain_price, color = color_2, marker = 'o', markersize=3)
ax2.tick_params(axis = 'y', labelcolor = color_2)

# 기준지수: 100
plt.axhline(100, color = 'gray', linestyle = 'solid')

fig.tight_layout()
plt.show()


# ### 시각화) 티켓가격 vs 오락문화 물가지수, 2020년도 평균=100 환산 비교

# In[542]:


fig = plt.figure(figsize = (15,5))

# 티켓가격 추이
ax1 = plt.subplot()
ax1.set_title('Price Index Transition Comparison', fontsize = 20)
ax1.set_xlabel('Month', fontsize = 14)
ax1.set_ylabel('Index', fontsize = 14)
ax1.plot(tm.index, tm['trans_mean'], color = 'tab:red', marker='s', markersize=3)
ax1.plot(tm.index, tmin['trans_mean'], color = 'khaki', marker='s', markersize=3)
ax1.plot(tm.index, tmed['trans_mean'], color = 'goldenrod', marker='s', markersize=3)
ax1.plot(tm.index, tmax['trans_mean'], color = 'darkgoldenrod', marker='s', markersize=3)
# ax1.tick_params(axis = 'y', labelcolor = color_1)

# 오락문화 물가지수 추이
ax1.plot(tm.index, et_cp.entertain_price, color = 'darkgreen', marker = 'o', markersize=3)

# 기준지수: 100 (2020년 평균)
plt.axhline(100, color = 'gray', linestyle = 'solid')

plt.legend(['Ticket Price(Mode)','Ticket Price(Min)', 'Ticket Price(Median)','Ticket Price(Max)','Entertainment Price Index'])
# fig.tight_layout()
plt.show()


# In[ ]:





# In[ ]:




