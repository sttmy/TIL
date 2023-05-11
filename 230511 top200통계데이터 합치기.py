#!/usr/bin/env python
# coding: utf-8

# In[43]:


import pandas as pd
import numpy as np
import openpyxl


# In[52]:


d = pd.DataFrame()
for i in range(1, 201):
    filename = f'Data/stat_ch/KOBIS_일자별_통계정보_2023-05-11 ({i}).xlsx'
    df = pd.read_excel(filename, header=3)
    wb = openpyxl.load_workbook(filename, data_only = True)
    ws = wb.active
    name = ws['A1'].value
    name = name.split(' ')[1].split("'")[1]
    df.insert(0,'movie name',name)
    d = pd.concat([d, df])
d.to_csv('Data/movie_stat.csv', index = False)


# In[56]:




