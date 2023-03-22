#!/usr/bin/env python
# coding: utf-8

# # API 불러오기

# ## @ Jupyter notebook

# In[4]:


filename = 'C:/workspace/API/행안부API.txt'
with open(filename) as f:
    api_key = f.read()


# In[5]:


len(api_key)    #API 제대로 업로드됐는지 확인, 43이 나와야 함


# ## @ Colab
# 
# from google.colab import files
# 
# uploaded = files.upload()
# 
# filename = list(uploaded.keys())[0]
# 
# 
# 
# with open(filename) as f:
# 
#     api_key = f.read()
#     
#     
# len(api_key)

# ### Quote 

# In[6]:


import requests     #html 다루거나 웹에 접속할 때 사용하는, 외부 요청으로 받아오는 패키지
from urllib.parse import quote    # quote


# In[7]:


bldg = '서울특별시청'
quote(bldg)


# #### Q.quote란?
# 
# 1.인터넷에 '서울특별시청' 검색
# 주소창 마지막: query = 서울특별시청
# 
# 복사+붙여넣기 해서 보면 한글(문자)이 아님: %EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%EC%B2%AD
# 
# 위 quote(bldg와 같음)
# 
# https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%EC%B2%AD
# 
# 2. 대구시청
# 
# https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%8C%80%EA%B5%AC%EC%8B%9C%EC%B2%AD

# In[8]:


bldg = '대구시청'
quote(bldg)


# ## 행안부
# 
# https://business.juso.go.kr/addrlink/openApi/searchApi.do
# 
# 기술제공 > API신청 > 검색API > 웹호출소스보기 > '가이드 및 소스 다운로드'
# 
# '검색API활용 가이드'파일 열어보기
# 
# p10 샘플 데이터 보기(json) 복사
# 
# https://business.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage=10&keyword=강남대로12길&confmKey=TESTJUSOGOKR&resultType=json
# 

# In[10]:


base_url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do'
params1 = f'?currentPage=1&countPerPage=10&keyword={quote("서울특별시청")}'   #큰따옴표만 사용
params2 = f'&confmKey={api_key}&resultType=json'
url = f'{base_url}?{params1}?{params2}'   #요청을 보낼 합친 주소


# In[ ]:




