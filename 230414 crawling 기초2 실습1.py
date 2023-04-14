#!/usr/bin/env python
# coding: utf-8

# ### 사이트 내 글 가져오기

# In[ ]:


https://crawlingstudy-dd3c9.web.app/01/


# In[5]:


import requests   # 인터넷에서 필요한 정보를 가져오는 함수
from bs4 import BeautifulSoup


# In[9]:


url = "https://crawlingstudy-dd3c9.web.app/01/"
response = requests.get(url)
resp = BeautifulSoup(response.text, 'html.parser')


# In[10]:


resp


# In[13]:


# id = cook 의 text 가져오기
resp.select_one('#cook').getText()


# In[17]:


resp.select_one('#cook').string


# In[18]:


resp.select_one('#cook').text


# In[ ]:


# tch
trs = soup.find('table').find_all('tr')
for tr in trs:
    tdd = tr.find_all('td')
    for td in tdd:
        print(td.get_text(), end=' ')
    print()


# In[59]:


# table의 내용을 dictionary로 가져오기
# [{'이름':'이몽룡','나이':'34'},{'이름':'홍길동','나이':'23'} ]

dic = dict()
a = []
hd = resp.find('table').find_all('th')
for h in hd:
    a.append(hd.text)
a


# In[56]:


b = []
vl = resp.find('table').find('tbody').find_all('td')
for v in vl:
    b.append = vl[v].text()


# In[ ]:


zip(a, b[0,1], b[2,3])


# In[57]:


#tch

key = []

for element in resp.find('table').find_all('th'):
    key.append(element.text)
key


# In[63]:


value = []
for element in resp.find('table').find('tbody').find_all('tr'):
    temp = []
    for td_element in element.find_all('td'):
        temp.append(td_element.text)
    value.append(dict(zip(key, temp)))
value


# In[64]:


resp.find('table').find('tbody').find_all('tr')


# In[68]:


element.find_all('td')


# In[67]:


element.find_all('td')[0]

