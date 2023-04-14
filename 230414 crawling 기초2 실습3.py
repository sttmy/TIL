#!/usr/bin/env python
# coding: utf-8

# ### 무신사 사이트 크롤링하기

# In[4]:


import requests
from bs4 import BeautifulSoup
import re


# In[ ]:


# 무신사

url = 'https://crawlingstudy-dd3c9.web.app/03/'
response = requests.get(url)
resp = BeautifulSoup(response.text, 'html.parser')


# In[7]:


resp = []
response = ()
for i in range(1,11):
    url = f'https://www.musinsa.com/categories/item/001?d_cat_cd=001&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    response = requests.get(url)
    resp.append(BeautifulSoup(response.text, 'html.parser'))


# In[8]:


resp


# In[9]:


for i in range(1,11):
    print('PAGE ==================================', i)
    url = f'https://www.musinsa.com/categories/item/001?d_cat_cd=001&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)


# In[10]:


# 옷 상품명 가져오기
for i in range(1,3):
    print('PAGE ==================================', i)
    url = f'https://www.musinsa.com/categories/item/001?d_cat_cd=001&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.select("ul#searchList>li"):
        # 옷의 이름 어디? '.article_info. p.list_info > a (속성:title)'
        print('상품명: ',item.select_one(".article_info p.list_info a").attrs['title'])

    


# In[12]:


# 옷 브랜드정보 가져오기
for i in range(1,3):
    print('PAGE ==================================', i)
    url = f'https://www.musinsa.com/categories/item/001?d_cat_cd=001&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.select("ul#searchList>li"):
        # 브랜드정보 어디? '.article_info p.item_title > a text'
        print('브랜드: ',item.select_one(".article_info p.item_title a").text.strip())  ## strip() 빈칸 없애기


# In[26]:


# 가격정보 가져오기: 할인가와 정상가 따로 취급
# .article_info p.price 
# 할인가: del 태그 이후의 가격, 정상가: p태그
# >>>>> 길이를 1 또는 else로 처리 

for i in range(1,3):
    print('PAGE ==================================', i)
    url = f'https://www.musinsa.com/categories/item/001?d_cat_cd=001&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.select("ul#searchList>li"):
        print('상품명: ',item.select_one(".article_info p.list_info a").attrs['title'])
        
        price = ""
        price = item.select_one(".article_info p.price").text.strip().split(" ")[-1].replace("원","")
    
#         if len(item.select_one(".article_info p.price").text.strip().split(" ")) =
= 1:
#             price = item.select_one(".article_info p.price").text.strip().split(" ")[0]
#         else:
#             price = item.select_one(".article_info p.price").text.strip().split(" ")[16]
        print('가격: ', price)
        print("")


# In[19]:


item.select_one(".article_info p.price").text.strip().split(" ")[-1]


# In[20]:


len(item.select_one(".article_info p.price").text.strip().split(" "))


# In[46]:


for i in range(1,3):
    print('PAGE ==================================', i)
    url = f'https://www.musinsa.com/categories/item/001?d_cat_cd=001&brand=&list_kind=small&sort=pop_category&sub_sort=&page={i}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.select("ul#searchList>li"):
        print('상품명: ',item.select_one(".article_info p.list_info a").attrs['title'])
        
        price = ""
#         price = re.sub('(',*원)',"",item.select_one(".article_info p.price").text.strip().split(" ")[-1])
        price = re.sub(',\원',"",item.select_one(".article_info p.price").text.strip().split(" ")[-1])
        # re.findall'[0-9,]*원'을 찾아서 제거?
        print('가격: ', price)
        print("")


# In[ ]:




