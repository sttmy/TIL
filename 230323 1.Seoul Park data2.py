#!/usr/bin/env python
# coding: utf-8

# # 공원시각화2
# 
# 자치구별 공원 현황.csv, seoul-gu-simple.json, 서울공원요약.csv

# In[1]:


import numpy as np
import pandas as pd
import json
import folium


# In[4]:


df = pd.read_csv('./data1/자치구별 공원 현황.csv')    
df.head()


# In[6]:


# geojson파일 불러오기
filename_gu = './Data/seoul-gu-simple.json'
with open(filename_gu, encoding = 'utf-8') as json_file:
    geo_data = json.load(json_file)


# In[8]:


geo_data['features'][0]


# ### 1.자치구별면적 대비 공원면적

# In[28]:


map = folium.Map(location = [37.581, 126.986], zoom_start = 11)
folium.TileLayer('cartodbpositron').add_to(map)

folium.Choropleth(geo_data = geo_data,
                 data = df,
                 columns = ('지역','면적비율'),
                 key_on = 'feature.id',
                 fill_color = 'PuBuGn',
                 legend_name = '자치구면적 대비 공원면적비율'
                 ).add_to(map)
  
title = '<h3 align = "center" style = "font-size:20"> 자치구별 면적 대비 공원면적이 큰 자치구 </h3>'
map.get_root().html.add_child(folium.Element(title))
map


# In[25]:


######## tch
# 자치구 면적대비 공원면적
center = [37.581, 126.986]
map_t = folium.Map(location = center, zoom_start = 11)
folium.Choropleth(geo_data = geo_data,
                 data = df,
                 columns = ('지역','면적비율'),
                 key_on = 'feature.id',
                 fill_color = 'BuPu',
                 legend_name = '공원면적'
                 ).add_to(map_t) 

for i in park.index:
    folium.CircleMarker(radius = int(park.크기[i]),
                        location = [park.위도[i], park.경도[i]],
                         popup = folium.Popup(park.지역[i]),
                         tooltip = f"{park.공원명[i]}({park.면적[i]: ,d})㎡",
                         color = 'green',
                         fill_color = 'green').add_to(map_t)
map_t


# ### 2. 자치구별인구 대비 공원면적

# In[14]:


map2 = folium.Map(location = [37.581, 126.986], zoom_start = 11)
folium.TileLayer('cartodbpositron').add_to(map2)

folium.Choropleth(geo_data = geo_data,
                 data = df,
                 columns = ('지역','인당면적'),
                 key_on = 'feature.id',
                 fill_color = 'BuGn',
                 legend_name = '인당 공원 면적'
                 ).add_to(map2)
  
title = '<h3 align = "center" style = "font-size:20"> 1인당 공원면적이 큰 자치구 </h3>'
map2.get_root().html.add_child(folium.Element(title))
map2


# ### 3.공원위치, 공원 크기별로 원크기 표시

# In[15]:


park = pd.read_csv('./data1/서울공원요약.csv')
park.head()


# In[16]:


df.head()


# In[29]:


map3 = folium.Map(location = [37.581, 126.986], zoom_start = 11)
folium.TileLayer('cartodbpositron').add_to(map3)

folium.Choropleth(geo_data = geo_data,
                 data = df,
                 columns = ('지역','면적비율'),
                 key_on = 'feature.id',
                 fill_color = 'PuBuGn',
                 legend_name = '자치구면적 대비 공원면적비율'
                 ).add_to(map3)
  
title = '<h3 align = "center" style = "font-size:20"> 자치구별 면적 대비 공원면적이 큰 자치구 </h3>'
map3.get_root().html.add_child(folium.Element(title))

for i in park.index:
    folium.CircleMarker(radius = int(park.크기[i]),
                        location = [park.위도[i], park.경도[i]],
                         popup = folium.Popup(park.지역[i]),
                         tooltip = f"{park.공원명[i]}({park.면적[i]: ,d})㎡",
                         color = 'coral',
                         fill_color = 'coral').add_to(map3)
map3


# ### folium.Circle vs folium.CircleMarker
# 
# circle location(위/경도), radius = '반지름, popup, tooltip
# circleMarker location(위/경도), radius = '반지름(fixcel), popup, tooltip
# 
# add가 겹쳐지면 다시 실행

# In[27]:


######## tch
# 자치구 인구대비 공원면적
center = [37.581, 126.986]
map_t2 = folium.Map(location = center, zoom_start = 11, tiles = 'Stamen Toner')
folium.Choropleth(geo_data = geo_data,
                 data = df,
                 columns = ('지역','인당면적'),
                 key_on = 'feature.id',
                 fill_color = 'BuPu',
                 legend_name = '인당 공원면적'
                 ).add_to(map_t) 

for i in park.index:
    folium.CircleMarker(radius = int(park.크기[i]),
                        location = [park.위도[i], park.경도[i]],
                         popup = folium.Popup(park.지역[i]),
                         tooltip = f"{park.공원명[i]}({park.면적[i]: ,d})㎡",
                         color = 'green',
                         fill_color = 'green').add_to(map_t2)
map_t2


# In[ ]:




