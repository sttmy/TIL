#!/usr/bin/env python
# coding: utf-8

# # 단계구분도
# ### 인구데이터, 경계면에 대한 json 데이터 사용
# older_population.csv,
# seoul-dong.geojson

# In[1]:


import pandas as pd
import json
import folium


# In[2]:


df = pd.read_csv('./Data/older_population.csv')
df.head()


# In[8]:


df.describe(), len(df['동'])


# In[5]:


#geojson파일 불러오기
filename = './Data/seoul-dong.geojson'
with open(filename, encoding = 'utf-8') as json_file:
    geo_data = json.load(json_file)


# In[6]:


geo_data['features'][0]    # 잘 나오는지 확인


# In[9]:


# 지도불러오기
map = folium.Map(location = [37.581, 126.986], zoom_start = 11)

# 단계구분도
folium.Choropleth(geo_data = geo_data,       # 지도데이터 파일
                  data = df,                 # 시각화하려는 데이터프레임
                  columns = ('동','인구'),   # 동별로 데이터가 있음, 지도데이터와 mapping할 값, 시각화하려는 변수
                  key_on = 'feature.properties.동',    # json파일의 feature? 데이터파일과 매칭할 값
                  fill_color = 'BuPu',
                  legend_name = '노령인구'   #color의 범주
                 ).add_to(map)

map


# In[10]:


# 다른 지도로 그려보기
map2 = folium.Map(location = [37.581, 126.986], zoom_start = 11, tiles = 'Stamen Toner')

# 단계구분도
folium.Choropleth(geo_data = geo_data,       # 지도데이터 파일
                  data = df,                 # 시각화하려는 데이터프레임
                  columns = ('동','인구'),   # 동별로 데이터가 있음, 지도데이터와 mapping할 값, 시각화하려는 변수
                  key_on = 'feature.properties.동',    # json파일의 feature? 데이터파일과 매칭할 값
                  fill_color = 'RdPu',
                  legend_name = '노령인구'   #color의 범주
                 ).add_to(map2)
title = '<h3 align = "center" style = "font-size:20"> 노령인구</h3>'
map2.get_root().html.add_child(folium.Element(title))
map2


# In[14]:


# 다른 지도 모양 tilelayer 추가해서.
map3 = folium.Map(location = [37.581, 126.986], zoom_start = 11)
# tilelayer추가 가능
folium.TileLayer('cartodbpositron').add_to(map3)    

folium.Choropleth(geo_data = geo_data,       # 지도데이터 파일
                  data = df,                 # 시각화하려는 데이터프레임
                  columns = ('동','인구'),   # 동별로 데이터가 있음, 지도데이터와 mapping할 값, 시각화하려는 변수
                  key_on = 'feature.properties.동',    # json파일의 feature? 데이터파일과 매칭할 값
                  fill_color = 'PiYG',
                  legend_name = '노령인구'   #color의 범주
                 ).add_to(map3)
title = '<h3 align = "center" style = "font-size:20"> 노령인구</h3>'
map3.get_root().html.add_child(folium.Element(title))
map3


# In[15]:


# Quiz '구'로 해보기

df.head()


# In[27]:


df_gu = df.groupby('구').sum()
df_gu.head()


# In[32]:


## tch
df_gu_t = df.groupby('구')[['인구']].sum()
df_gu_t.head()


# In[33]:


df_gu_t.reset_index(inplace = True)   #reset index,, 구를 인덱스에서 컬럼으로 다시 가져옴
df_gu_t.head()


# In[46]:


map_gu = folium.Map(location = [37.581, 126.986], zoom_start = 11)
folium.TileLayer('cartodbpositron').add_to(map_gu)    

folium.Choropleth(geo_data = geo_data,       
                  data = df_gu_t,              
                  columns = ('구','인구'),   
                  key_on = 'feature.properties.구',   
                  fill_color = 'YlOrRd',
                  legend_name = '노령인구'   #color의 범주
                 ).add_to(map_gu)
title = '<h3 align = "center" style = "font-size:20"> 노령인구(구단위) </h3>'
map_gu.get_root().html.add_child(folium.Element(title))
map_gu


# In[41]:


# 경계선을 '구'로 해서 다시 그리기

# '구'경계선 json파일 불러오기
filename_gu = './Data/seoul-gu-simple.json'
with open(filename_gu, encoding = 'utf-8') as json_file:
    gu_geo_data = json.load(json_file)


# In[40]:


gu_geo_data['features'][0]


# In[47]:


map_gu = folium.Map(location = [37.581, 126.986], zoom_start = 11)
folium.TileLayer('cartodbpositron').add_to(map_gu)    

folium.Choropleth(geo_data = gu_geo_data,     # geo_data     
                  data = df_gu_t,              
                  columns = ('구','인구'),   
                  key_on = 'feature.id',      # feature.id
                  fill_color = 'PuBuGn',
                  legend_name = '노령인구'   
                 ).add_to(map_gu)
title = '<h3 align = "center" style = "font-size:20"> 노령인구(구단위)_경계선 구 </h3>'
map_gu.get_root().html.add_child(folium.Element(title))
map_gu


# In[ ]:




