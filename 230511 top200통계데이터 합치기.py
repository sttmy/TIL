#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import numpy as np
import openpyxl


# In[60]:


d = pd.DataFrame()
for i in range(1, 201):
    # Excel 파일 불러오기 (200개 하나씩)
    filename = f'Data/stat_ch/KOBIS_일자별_통계정보_2023-05-11 ({i}).xlsx'
    df = pd.read_excel(filename, header=3)
    # Excel 내에 있는 제목 불러오기
    wb = openpyxl.load_workbook(filename, data_only = True)
    ws = wb.active
    name = ws['A1'].value
    name = name.split(' ')[1].split("'")[1]
    # 제목 컬럼 df에 삽입
    df.insert(0,'movie name',name)
    # dataframe에 합치기
    d = pd.concat([d, df])
d.to_csv('Data/MovieStat.csv', index = False)


# In[61]:


df = pd.read_csv('Data/MovieStat.csv')
df.head()


# In[62]:


df.info()


# In[63]:


df.describe()


# In[ ]:




