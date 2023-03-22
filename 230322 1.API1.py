#!/usr/bin/env python
# coding: utf-8

# # 행안부 API

# ## API 불러오기

# ## @ Jupyter notebook

# In[34]:


filename = 'C:/workspace/API/행안부API.txt'
with open(filename) as f:
    api_key = f.read()


# In[35]:


len(api_key)    #API 제대로 업로드됐는지 확인, 43이 나와야 함


# ## @ Colab

# In[ ]:


from google.colab import files
uploaded = files.upload()


# In[ ]:


filename = list(uploaded.keys())[0]

with open(filename) as f:
    api_key = f.read()
len(api_key)


# ### Quote 

# In[43]:


import requests     #html 다루거나 웹에 접속할 때 사용하는, 외부 요청으로 받아오는 패키지
from urllib.parse import quote    
import json


# In[37]:


bldg = '서울특별시청'
quote(bldg)     #quote: (마지막)주소값인 셈임


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

# In[38]:


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

# In[39]:


base_url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do'
params1 = f'?currentPage=1&countPerPage=10&keyword={quote("서울특별시청")}'   #큰따옴표만 사용
params2 = f'&confmKey={api_key}&resultType=json'
url = f'{base_url}?{params1}?{params2}'   #요청을 보낼 합친 주소


# In[ ]:


url  # chrome에서 열어보면 정보가 있음, 실행하면 key값이 보이므로 github공유시유의할 것


# In[40]:


result = requests.get(url)    #url을 보내서 받아온 정보를 저장
result.status_code            #url주소 잘못 입력되면 404 Error, 200은 정상적 소통이 됐을 때 뜨는 코드임


# In[41]:


result.text     #결과가 안뜨면 주소가 잘못됐거나 API키가 잘못된 것임


# In[ ]:


########### 제대로된 결과가 안 나오면 ############# 위 대신에 아래를 다시 실행해볼 것
base_url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do'
params1 = f'currentPage=1&countPerPage=10&confmKey={api_key}'
params2 = f'keyword={quote("서울특별시청")}&resultType=json'
url = f'{base_url}?{params1}&{params2}'


# In[16]:


# result.text를 json으로 바꾸기

res = json.loads(result.text)
res


# In[20]:


# roadAddr': '서울특별시 중구 세종대로 110(태평로1가) 뽑아보기

road_add = res['results']['juso'][0]['roadAddr']
road_add


# In[22]:


# 여러개 해보기

places = '종로구청 노원구청 송파구청 마포구청 양천구청'
places = places.split(' ')
places


# In[ ]:


base_url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do'        # 위에서 가져옴
params2 = f'&confmKey={api_key}&resultType=json'                        # 위에서 가져옴

addr_list = []
for i in places:
    params1 = f'?currentPage=1&countPerPage=10&keyword={quote(i)}'     # 위에서 가져옴, quote(i)만 변경
    url = f'{base_url}?{params1}?{params2}'                    # 위에서 가져옴
    result = requests.get(url)
    res = json.loads(result.text)
    road_add = res['results']['juso'][0]['roadAddr']
    addr_list.append(road_add)


# In[30]:


addr_list


# In[32]:


df = pd.DataFrame({'공공기관':places, '도로명주소':addr_list})
df.to_csv('./data1/공공기관_행안부.csv')


# In[33]:


df


# In[29]:


########### 제대로된 결과가 안 나오면 ############# 아래 이용

base_url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do'    # 위에서 가져옴
params1 = f'currentPage=1&countPerPage=10&confmKey={api_key}'       # 위에서 가져옴

addr_list = []
for i in places:
    params2 = f'keyword={quote(i)}&resultType=json'     # 위에서 가져옴, quote(i)만 변경
    url = f'{base_url}?{params1}?{params2}'             # 위에서 가져옴
    result = requests.get(url)
    res = json.loads(result.text)
    road_add = res['results']['juso'][0]['roadAddr']
    addr_list.append(road_add)


# In[ ]:




