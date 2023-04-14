#!/usr/bin/env python
# coding: utf-8

# ### 사이트 내 글 가져오기2

# In[ ]:


https://crawlingstudy-dd3c9.web.app/03/

    [['써니전자','5,000'], ...., ['니케이','2252365662']]


# In[2]:


import requests
from bs4 import BeautifulSoup
url = 'https://crawlingstudy-dd3c9.web.app/03/'
response = requests.get(url)
resp = BeautifulSoup(response.text, 'html.parser')


# In[ ]:


# [기업명, 주가지수] 리스트만들기


# In[20]:


resp.select('#popularItemList > li')


# In[23]:


for item in resp.select('#popularItemList > li'):
    print(item)


# In[25]:


popular = []
for item in resp.select('#popularItemList > li'):
    popular.append([item.select_one('a').text, item.select_one('span').text])
popular


# In[27]:


major = []
for item in resp.select('.lst_major > li'):
    major.append([item.select_one('a').text, item.select_one('span').text])
major


# In[31]:


resp.select('.lst_major>li')[0].select_one('a').text


# In[33]:


resp.select('.lst_major>li')[1].select_one('span').text


# In[40]:


resp.select('.lst_pop > li')[0].find('img').attrs['alt']


# In[ ]:


# [기업명, 상/하한여부] 리스트만들기


# In[41]:


updown = []
for i in resp.select('.lst_pop > li'):
    updown.append([i.select_one('a').text, i.select_one('img').attrs['alt']])
updown


# In[42]:


updown2 = []
for i in resp.select('.lst_major > li'):
    updown2.append([i.select_one('a').text, i.select_one('img').attrs['alt']])
updown2


# In[53]:


# 상한/상승인 기업만 리스트 만들어볼 것

new_lst = []
for i in resp.select('.lst_pop > li'):
    if (i.select_one('img').attrs
        ['alt'] == '상한') | (i.select_one('img').attrs['alt'] == '상승'):
#     if i.select_one('img').attrs['alt'] == '상한' or i.select_one('img').attrs['alt'] == '상승':
        new_lst.append([i.select_one('a').text, i.select_one('img').attrs['alt']])
new_lst


# In[ ]:


lst = resp.select('.lst_pop > li')


# In[54]:


new_lst2 = []
for i in resp.select('.lst_major > li'):
    if (i.select_one('img').attrs['alt'] == '상한'):
        new_lst2.append([i.select_one('a').text, i.select_one('img').attrs['alt']])
new_lst2


# In[ ]:


# 쉼표 제거
# key값 분양유형
# key 세대수
# key 평형
# dictionary로 만들기


# In[55]:


resp


# In[68]:


resp.select('div > a')


# In[81]:


resp.select('ul > li > div')


# In[100]:


resp.select('ul > li > div')[0].find('a').get_text()


# In[103]:


resp.select('ul > li > div')[0].select('.tit')


# In[112]:


resp.select('ul > li > div')[0].select('.txt')[0].get_text()


# In[ ]:


price=[] 
for i in resp.select('ul > li > div'):
    i.find('a').get_text()
    for j in i.select('.tit'):
        append(j)
    
    select('.txt')[0].get_text()


# In[ ]:


# tch
apt = []
for item in resp.select('.sale_list li'):
    apt.append({'이름': 태그.text,
               '보증금': 태그.text,
               '유형': ,
               '분양유형':,
               '세대수':, 
               '평형':})


# In[107]:


apt = []
for item in resp.select('.sale_list li'):
    apt.append({'이름': item.select_one(".sale_tit").text.strip(),
               '보증금': item.select(".detail_info dd.txt")[0].select_one('strong').text.replace(',',''),
               '유형': item.select(".detail_info dd.txt")[1].text.split('|')[0],
               '분양유형': item.select(".detail_info dd.txt")[1].text.split('|')[1],
               '세대수': item.select(".detail_info dd.txt")[2].text.split('|')[0],
               '평형': item.select(".detail_info dd.txt")[2].text.split('|')[1]
               })
apt


# In[ ]:


# key, value로 만들어보기
key = []
value = []

for element in resp.find('table').find_all('th'):
    key.append(element.text)
for element in resp.find('table').find('tbody').find_all('tr'):
    temp = []
    for td_element in element.find_all('td'):
        temp.append(td_element.text)
    value.append(dict(zip(key, temp)))

