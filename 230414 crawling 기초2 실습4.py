#!/usr/bin/env python
# coding: utf-8

# ## 다음 영화순위 정보 가져오기

# In[1]:


import requests
from bs4 import BeautifulSoup
import re


# In[2]:


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36 Edge/17.17134'}
url = 'https://search.daum.net/search?w=tot&DA=UME&t__nil_searchbox=suggest&sug=&sugo=15&sq=%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&o=2&q=%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84'

# 다음 영화 사이트는 headers 정보를 보내줘야 함


# In[3]:


response = requests.get(url, headers=headers)
resp = BeautifulSoup(response.text, 'html.parser')


# In[4]:


resp


# In[7]:


# 1위, 2위,... 순위정보 가져오기
# ol (class: movie_list)> li 에서 가져옴
movieInfoList = resp.find('ol',attrs={'class':'movie_list'}).find_all('li')


# In[10]:


movieInfo = movieInfoList[0]
movieInfo


# In[9]:


movieRank = movieInfo.find('span', attrs={'class':'num_rank01'}).get_text()
movieRank


# In[12]:


# 순위 순으로 제목 가져오기
# ol class: ~movie_list > li > div > a. 속성값 class:"tit_main"
movieTitle = movieInfo.find('a', attrs={'class':'tit_main'}).get_text()
movieTitle


# In[13]:


movieInfo


# In[20]:


# 점수, 평가참여자수, 예매율, 개봉일자

# 점수: dl dd em > text
movieScore = movieInfo.find('em', attrs={'class':'rate'}).get_text()
movieScore


# In[57]:


# 평가참여자수
movieScoreCnt = movieInfo.find('dd', attrs={'class':'review'}).get_text()
movieScoreCnt


# In[58]:


# 예매율
movieTicketSales = movieInfo.find('dd', attrs={'class':'cont'}).get_text()
movieTicketSales


# In[54]:


movieInfo.find_all('dd', attrs={'class':'cont'})[0].get_text()


# In[60]:


# 개봉일자
movieOpenDate = movieInfo.find_all('dd', attrs={'class':'cont'})[1].get_text().strip()
movieOpenDate


# In[ ]:




