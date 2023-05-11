#!/usr/bin/env python
# coding: utf-8

# In[33]:


import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tqdm.notebook import tqdm
import numpy as np

from konlpy.tag import Okt, Kkma, Komoran


# In[34]:


base_url = 'https://shopping.naver.com/home'
driver = webdriver.Chrome()
driver.get(base_url)
time.sleep(1)


# In[35]:


keyword = '도시락'
search_box = driver.find_element(by = By.CSS_SELECTOR, value = 'div > input._searchInput_search_text_3CUDs')


# In[36]:


search_box.send_keys(keyword)
search_box.send_keys(Keys.ENTER)
time.sleep(1)


# In[38]:


pay = driver.find_element(by = By.CSS_SELECTOR, value = 'a.subFilter_filter___O_rt')
pay.send_keys(Keys.ENTER)
time.sleep(1)
review_order = driver.find_elements(by = By.CSS_SELECTOR, value = 'div.subFilter_sort_box__FpfWA > a')[3]
review_order.send_keys(Keys.ENTER)


# In[42]:


# 크롤링 스크롤 내리기
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# In[43]:


soup = BeautifulSoup(driver.page_source, 'html.parser')


# In[44]:


len(soup.select('a.basicList_link__JLQJf'))


# In[55]:


len(soup.select('div.basicList_title__VfX3c'))


# In[56]:


lis = soup.select('div.basicList_title__VfX3c')[0]


# In[58]:


answer_url = lis.select_one('a')['href']
driver.get(answer_url)
time.sleep(1)


# In[59]:


answer_sp = BeautifulSoup(driver.page_source, 'html.parser')
answer_sp


# In[61]:


answer_sp.select_one('a._11xjFby3Le N=a:tab.review')


# In[ ]:




