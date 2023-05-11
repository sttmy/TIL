#!/usr/bin/env python
# coding: utf-8

# In[40]:


import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from tqdm.notebook import tqdm
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import datetime
import statistics

from konlpy.tag import Okt, Kkma, Komoran


# In[56]:


base_url = 'https://www.kobis.or.kr/kobis/business/mast/thea/findShowHistorySc.do'
driver = webdriver.Chrome()
driver.get(base_url)
time.sleep(1)


# In[116]:


date = ['2004-01-01', '2004-01-07']
driver.find_element(By.XPATH, '//*[@id="showStartDt"]').clear()
driver.find_element(By.XPATH, '//*[@id="showStartDt"]').send_keys(date[0])
driver.find_element(By.XPATH, '//*[@id="showEndDt"]').clear()
driver.find_element(By.XPATH, '//*[@id="showEndDt"]').send_keys(date[1])
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="searchForm"]/div/div[2]/div[1]/label').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]/option[2]').click()
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]/option[2]').click()
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]/option[2]').click()
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
time.sleep(2)


# In[223]:


soup = BeautifulSoup(driver.page_source, 'html.parser')


# In[224]:


lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[0].text
lis


# In[225]:


lis.split(" ")[1].split('(')[1].split('원')[0]


# In[75]:


list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
list


# In[84]:


lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[0]
int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',',''))


# In[85]:


list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
len(list)


# In[121]:


price = []
nan = 0
for i in range(1, len(list)+1):
    try:
        lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[i]
        price.append(int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',','')))
    except:
        nan += 1


# In[122]:


len(price) + nan


# In[118]:


def solution(array):
    while len(array) != 0 :
        for i, a in enumerate(set(array)):
            array.remove(a)
        if i == 0: return a
    return -1


# In[119]:


solution(price)


# In[127]:


a=0
for i in range(1,len(price)):
    if price[i] == 14000:
        a += 1
    else:
        pass
a


# In[126]:


len(price)


# ### -------------------------

# In[189]:


# 날짜
start = []
end = []
for year in range(2006, 2023):
    for month in range(1,13):
        start.append(datetime.date(year, month, 1).strftime('%Y-%m-%d'))
        end.append(datetime.date(year, month, 7).strftime('%Y-%m-%d'))


# In[193]:


len(start), len(end)


# ### -------------------------------------------------------------------------------

# In[9]:


# 조회일자
import datetime
start = []
end = []
for year in range(2018, 2023):
    for month in range(1,13):
        start.append(datetime.date(year, month, 1).strftime('%Y-%m-%d'))
        end.append(datetime.date(year, month, 7).strftime('%Y-%m-%d'))
for month in range(1,5):
    start.append(datetime.date(2023, month, 1).strftime('%Y-%m-%d'))
    end.append(datetime.date(2023, month, 7).strftime('%Y-%m-%d'))
len(start)


# In[10]:


# 최빈값 함수
from collections import Counter
def modefinder(numbers):
    c = Counter(numbers)
    mode = c.most_common(1)
    return mode[0][0]


# In[11]:


base_url = 'https://www.kobis.or.kr/kobis/business/mast/thea/findShowHistorySc.do'
driver = webdriver.Chrome()
driver.get(base_url)
time.sleep(3)


# In[243]:


# 지역선택
driver.find_element(By.XPATH, '//*[@id="searchForm"]/div/div[2]/div[1]/label').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]/option[2]').click()  #서울시
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]/option[14]').click()  #마포구
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]/option[4]').click()  #CGV홍대
time.sleep(0.2)

ticket = []
for i in range(0,len(start)):
    # 상영기간 선택
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').send_keys(start[i])
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').send_keys(end[i])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
    price = []
    for i in range(0, len(list)+1):
        try:
            lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[i]
            price.append(int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',','')))
        except:
            pass
    ticket.append(modefinder(price))
cgv = pd.DataFrame(ticket, columns = ["CGV"])


# In[247]:


### 롯데시네마
# 지역선택
driver.find_element(By.XPATH, '//*[@id="searchForm"]/div/div[2]/div[1]/label').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]/option[2]').click()  #서울시
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]/option[25]').click()  #중구
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]/option[9]').click()  #롯데시네마 에비뉴엘(명동)
time.sleep(0.2)

ticket = []
for i in range(0,len(start)):
    # 상영기간 선택
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').send_keys(start[i])
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').send_keys(end[i])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
    price = []
    for i in range(0, len(list)+1):
        try:
            lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[i]
            price.append(int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',','')))
        except:
            pass
    ticket.append(modefinder(price))
lotte = pd.DataFrame(ticket, columns = ["LotteCinema"])
lotte


# In[ ]:


### 메가박스
# 지역선택
driver.find_element(By.XPATH, '//*[@id="searchForm"]/div/div[2]/div[1]/label').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]/option[2]').click()  #서울시
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]/option[2]').click()  #강남구
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]/option[11]').click()  #메가박스 코엑스
time.sleep(0.2)

ticket = []
for i in range(0,len(start)):
    # 상영기간 선택
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').send_keys(start[i])
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').send_keys(end[i])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
    price = []
    for i in range(0, len(list)+1):
        try:
            lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[i]
            price.append(int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',','')))
        except:
            pass
    ticket.append(modefinder(price))
megabox = pd.DataFrame(ticket, columns = ["Megabox"])
megabox


# In[ ]:


pd.concat(cgv, lotte, megabox)


# In[39]:


price


# In[38]:


modefinder(price), max(price), min(price), statistics.median(price)


# In[43]:


a = [1,2,3,4,5]
b = [6,7,8,9,0]
c = ["A","B","C","D","E"]

A = pd.DataFrame(a, columns = ['a'])
B = pd.DataFrame(b, columns = ['b'])
C = pd.DataFrame(c, columns = ['c'])
pd.concat([A,B,C], axis = 1)


# In[34]:


min1 = []
max1 = []
mode1 = []

# 지역선택
driver.find_element(By.XPATH, '//*[@id="searchForm"]/div/div[2]/div[1]/label').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sWideareaCd"]/option[2]').click()  #서울시
time.sleep(0.2)

### CGV
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]/option[14]').click()  #마포구
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]/option[4]').click()  #CGV홍대
time.sleep(0.2)
for i in range(0,len(start)):
    # 상영기간 선택
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').send_keys(start[i])
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').send_keys(end[i])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
    price = []
    for i in range(0, len(list)+1):
        try:
            lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[i]
            price.append(int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',','')))
        except:
            pass
    min1.append(min(price))
    max1.append(max(price))
    mode1.append(modefinder(price))
min1 = pd.DataFrame(min1, columns = ['min'])
max1 = pd.DataFrame(max1, columns = ['max'])
mode1 = pd.DataFrame(mode1, columns = ['mode'])
cgv = pd.concat([min1, max1, mode1], axis = 1)
cgv.to_csv('CGV.csv')


# In[48]:


### 롯데시네마
min2 = []
max2 = []
mode2 = []
median2 = []

driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]/option[25]').click()  #중구
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]/option[9]').click()  #롯데시네마 에비뉴엘(명동)
time.sleep(0.2)

for i in range(0,len(start)):
    # 상영기간 선택
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').send_keys(start[i])
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').send_keys(end[i])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
    price = []
    for i in range(0, len(list)+1):
        try:
            lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[i]
            price.append(int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',','')))
        except:
            pass
    min2.append(min(price))
    max2.append(max(price))
    mode2.append(modefinder(price))
    median2.append(statistics.median(price))
min2 = pd.DataFrame(min2, columns = ['min'])
max2 = pd.DataFrame(max2, columns = ['max'])
mode2 = pd.DataFrame(mode2, columns = ['mode'])
median2 = pd.DataFrame(median2, columns = ['median'])
lotte = pd.concat([min2, median2, max2, mode2], axis = 1)
lotte.to_csv('LotteCinema.csv')


# In[51]:


### 메가박스
min3 = []
max3 = []
mode3 = []
median3 = []

driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sBasareaCd"]/option[2]').click()  #강남구
time.sleep(0.2)
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]').click()
driver.find_element(By.XPATH, '//*[@id="sTheaCd"]/option[11]').click()  #메가박스 코엑스
time.sleep(0.2)

for i in range(0,len(start)):
    # 상영기간 선택
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showStartDt"]').send_keys(start[i])
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').clear()
    driver.find_element(By.XPATH, '//*[@id="showEndDt"]').send_keys(end[i])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list = soup.select('table.tbl3.info3 > tbody > tr > td.left')
    price = []
    for i in range(0, len(list)+1):
        try:
            lis = soup.select('table.tbl3.info3 > tbody > tr > td.left')[i]
            price.append(int(lis.text.split(" ")[1].split('(')[1].split('원')[0].replace(',','')))
        except:
            pass
    min3.append(min(price))
    max3.append(max(price))
    mode3.append(modefinder(price))
    median3.append(statistics.median(price))
min3 = pd.DataFrame(min3, columns = ['min'])
max3 = pd.DataFrame(max3, columns = ['max'])
mode3 = pd.DataFrame(mode3, columns = ['mode'])
median3 = pd.DataFrame(median3, columns = ['median'])
megabox = pd.concat([min3, median3, max3, mode3], axis = 1)
megabox.to_csv('Megabox.csv')


# In[ ]:




