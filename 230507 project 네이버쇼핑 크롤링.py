#!/usr/bin/env python
# coding: utf-8

# In[7]:


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


# In[51]:


base_url = 'https://shopping.naver.com/home'
driver = webdriver.Chrome()
driver.get(base_url)
time.sleep(1)


# In[45]:


driver.find_element(by = By.CSS_SELECTOR, value = 'div > input._searchInput_search_text_3CUDs')


# In[52]:


keyword = '도시락'
search_box = driver.find_element(by = By.CSS_SELECTOR, value = 'div > input._searchInput_search_text_3CUDs')
search_box.send_keys(keyword)
search_box.send_keys(Keys.ENTER)
time.sleep(1)


# In[53]:


pay = driver.find_elements(by = By.CSS_SELECTOR, value = 'a.subFilter_filter___O_rt')[2]
pay.send_keys(Keys.ENTER)
time.sleep(1)


# In[54]:


review_order = driver.find_elements(by = By.CSS_SELECTOR, value = 'div.subFilter_sort_box__FpfWA > a')[3]
review_order.send_keys(Keys.ENTER)
time.sleep(1)


# In[55]:


# 크롤링 스크롤 내리기
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# In[56]:


soup = BeautifulSoup(driver.page_source, 'html.parser')


# In[20]:


len(soup.select('a.basicList_link__JLQJf'))


# In[57]:


len(soup.select('div.basicList_title__VfX3c'))


# In[58]:


lis = soup.select('div.basicList_title__VfX3c')[0]


# In[78]:


answer_url = lis.select_one('a')['href']
driver.get(answer_url)
time.sleep(1)


# In[87]:


driver.find_element(by = By.XPATH, value = '//*[@id="content"]/div/div[3]/div[3]/ul/li[2]/a').click()
time.sleep(1)


# In[88]:


answer_sp = BeautifulSoup(driver.page_source, 'html.parser')
answer_sp


# In[89]:


review = answer_sp.select('span._3HJHJjSrNK')[0].text


# In[105]:


review


# In[93]:


len(answer_sp.select('li._2389dRohZq'))


# In[94]:


rv = answer_sp.select('li._2389dRohZq')[0]


# In[98]:


rv.select_one('em._15NU42F3kT').text


# In[104]:


rv.select('span._3QDEeS6NLn')[1].text


# In[ ]:


star=[]
text=[]


for 
driver.find_element(by = By.XPATH, value = '//*[@id="content"]/div/div[3]/div[3]/ul/li[2]/a').click()
time.sleep(1)

    answer_sp = BeautifulSoup(driver.page_source, 'html.parser')
    review.append(answer_sp.select('span._3HJHJjSrNK')[0].text)
    for rv in answer_sp:
        star.append(rv.select_one('em._15NU42F3kT').text)
        text.append(rv.select('span._3QDEeS6NLn')[1].text)

