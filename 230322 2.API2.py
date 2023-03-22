#!/usr/bin/env python
# coding: utf-8

# ### Kakao API

# In[3]:


# 화면크기조절
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:85% !important; }</style>"))


# In[1]:


filename = 'C:/workspace/API/카카오API.txt'
with open(filename) as f:
    api_key = f.read()


# In[2]:


len(api_key)


# In[43]:


import requests 
from urllib.parse import quote   
import pandas as pd


# In[6]:


addr = '서울특별시 종로구 종로1길 36(수송동)'  #도로명주소를 입력하고 반환
quote(addr)


# ### kakao developers
# 
# 문서 > 유용한 참고 정보 > 로컬 > 주소 검색하기
# 
# https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord
# 
# Sample > Request 에서 주소 복사
# 
# "https://dapi.kakao.com/v2/local/search/address.json" \
#   -H "Authorization: KakaoAK ${REST_API_KEY}" \
#   --data-urlencode "query=전북 삼성동 100" 

# In[8]:


search_url = "https://dapi.kakao.com/v2/local/search/address.json"
url = f'{search_url}?query={quote(addr)}'    #query를 보낼 때는 ?로 연결됨
url


# In[15]:


# 카카오는 url을 headers형태로 보내고, key값은 그 안에 넣어줌
result = requests.get(url,headers = {"Authorization": f'KakaoAK {api_key}'}).json()  # 따로 보냄, json으로 받아와야 함
result    # json()으로 받지 않은 경우에는, result 대신 result.text로 출력


# In[16]:


# status_code가 200 나와야 정상
# status_code는 json()으로 불러오지 않아야 확인가능. 위 result 코드에서 json()삭제 후 확인
result1 = requests.get(url,headers = {"Authorization": f'KakaoAK {api_key}'})
result1.status_code


# In[42]:


result1.text     # text파일 읽어왔지만 json형태가 아님


# In[18]:


# json으로 불러오지 않았을 경우 아래의 과정을 통해 json형태로 변경
import json
res = json.loads(result1.text)
res


# In[19]:


res.keys()


# In[20]:


res['documents'][0]['x']


# In[21]:


res['documents'][0]['y']


# In[22]:


result['documents'][0]['x']   #처음부터 jason으로 불러온 결과와 같음


# In[23]:


result['documents'][0]['y']    


# In[24]:


# string이기 때문에 float로 바꿔줌

lng = float(result['documents'][0]['x'])   #경도 longitude 동서경
lat = float(result['documents'][0]['y'])   #위도 latitude 남북위


# In[27]:


lng, lat


# In[25]:


# 공공기관.csv파일 활용

import pandas as pd
df = pd.read_csv('./Data/공공기관.csv')
df.head()


# In[30]:


# 도로명주소 옆에 위도, 경도 값 추가

lat_list = []
lng_list = []
for i in df.index:
    search_url = "https://dapi.kakao.com/v2/local/search/address.json"
    url = f'{search_url}?query={quote(df.도로명주소[i])}'   # df.도로명주소[i] 변경
    result = requests.get(url,headers = {"Authorization": f'KakaoAK {api_key}'}).json()
    lng = float(result['documents'][0]['x'])
    lat = float(result['documents'][0]['y'])
    lng_list.append(lng)  #append
    lat_list.append(lat)


# In[31]:


df['위도']=lat_list
df['경도']=lng_list
df.to_csv('./data1/공공기관2.csv', index = False)


# In[32]:


df


# ## 지도에 그려보기

# In[33]:


import folium


# In[35]:


map = folium.Map(location=[df.위도.mean(),df.경도.mean()], zoom_start=15)


# In[38]:


for i in df.index:
    folium.Circle(radius = 300, 
                  location = [df.위도[i], df.경도[i]],
                  popup = folium.Popup(df.도로명주소[i], max_width = 200),   #넓이는 200정도로 픽셀 고정
                  tooltip = df.공공기관[i],    # 마우스오버
                  color = 'red',
                  fill = True,
                  fill_color = '#3186cc').add_to(map)
# 부수적 옵션    
title = '<h3 align = "center" style = "font-size:20"> 서울시 구청</h3>'    #h3는 글자크기, align 정렬, CSS, 태그는 닫아줌
map.get_root().html.add_child(folium.Element(title))


# In[39]:


map


# In[ ]:




