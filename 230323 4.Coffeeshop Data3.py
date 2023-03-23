#!/usr/bin/env python
# coding: utf-8

# # 카토그램 그리기
# 
# draw_korea_raw(2021).xlsx
# 
# draw_map.py            ### 같은 workspace 안에 있어야 함

# In[1]:


import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus'] = False  
plt.rc('font', family = 'Malgun Gothic')
from draw_map import drawKorea


# In[3]:


cf = pd.read_csv('./data1/커피지수.csv')
cf.head()


# In[4]:


map_raw = pd.read_excel('./Data/draw_korea_raw(2021).xlsx')
map_raw.head()


# In[6]:


map = pd.DataFrame(map_raw.stack())    # stack: index가 column으로 배치?됨
map.reset_index(inplace = True)
print(map.shape)
map.head()


# In[7]:


map.columns = ['y','x','ID']
map.head(3)


# In[9]:


df = pd.merge(map, cf, how = 'left')
df.head()


# In[13]:


df.fillna(0,inplace = True)
df.head()


# In[14]:


df.info()


# In[15]:


df.이디야 = df.이디야.astype(int)
df.스타벅스 = df.스타벅스.astype(int)
df.커피빈 = df.커피빈.astype(int)
df.빽다방 = df.빽다방.astype(int)
df.커피지수 = df.커피지수.astype(int)
df.info()


# ## 커피지수로 카토그램 그리기

# In[16]:


drawKorea('커피지수',df, 'Reds')
# 참고: cf['커피지수'] = (cf.스타벅스 + cf.커피빈) / (cf.이디야 + cf.빽다방)


# In[17]:


# 커피지수 Top10
df.sort_values(by = '커피지수',ascending = False).head(10)


# In[ ]:




