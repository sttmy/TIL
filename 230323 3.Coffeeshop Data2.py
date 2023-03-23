#!/usr/bin/env python
# coding: utf-8

# ## 커피지수 part2
# 
# 스타벅스.csv, 커피빈.csv, 이디야.csv, 빽다방.csv

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


starbucks = pd.read_csv('./data1/스타벅스.csv')
coffeebean = pd.read_csv('./data1/커피빈.csv')
ediya = pd.read_csv('./data1/이디야.csv')
paik = pd.read_csv('./data1/빽다방.csv')


# In[3]:


starbucks.head()


# In[4]:


starbucks[starbucks.시군구명.str.contains('고성')]


# In[5]:


ediya[ediya.시군구명.str.contains('고성')]    #  시도명이 다른데, 시군구명이 같음. 나중에 집계시 문제


# In[21]:


starbucks['시군구명'].unique(), coffeebean['시군구명'].unique(), ediya['시군구명'].unique(), paik['시군구명'].unique()


# In[6]:


### 동명으로 문제?가 있는 지역들?
### 카토그램 만들기 위해 '시 단위로 조정'

# 고성군: 고성(강원), 고성(경남)
# 광역시: 서울 용산, 서울 서대문, 대전 서구, 대전 유성구, 세종시
# 행정구: 수원 장안, 용인 수지, 고양 일산동, 창원 합포, 창원 회원


# In[28]:


tmp_gu_dict = {
    '수원':['장안구','권선구','팔달구','영통구'],
    '성남':['수정구','중원구','분당구'],
    '안양':['만안구','동안구'],
    '안산':['상록구','단원구'],
    '고양':['덕양구','일산동구','일산서구'],
    '용인':['처인구','기흥구','수지구'],
    '청주':['상당구','서원구','흥덕구','청원구'],
    '천안':['동남구','서북구'],
    '전주':['완산구','덕진구'],
    '포항':['남구','북구'],
    '창원':['의창구','성산구','진해구','마산합포구','마산회원구']
    }


# In[7]:


# 카토그램이랑 연계위해 'id' 추가. 지역표시   ##############이후부터 흐름을 잘 이해할 것
metro_list = ['서울특별시','부산광역시','인천광역시','대구광역시','대전광역시','광주광역시','울산광역시']


# In[26]:


starbucks.시도명[1][:2], starbucks.시군구명[1][:-1]


# In[37]:


starbucks.시군구명[189].split()[-1]


# In[25]:


def get_ID(df):
    city_name = [None] * len(df)    # 시 이름이 없을 때 0으로 처리
    for i in df.index:
        if df.시도명[i] in metro_list:                    #### 시도명이 metro_list에 있으면
            if len(df.시군구명[i]) == 2:  # 서울 중구, 대전 서구
                city_name[i] = df.시도명[i][:2] + ' ' + df.시군구명[i]    
            else:                        # 서울 용산, 서울 서대문
                city_name[i] = df.시도명[i][:2] + ' ' + df.시군구명[i][:-1]    
        else:                                            #### 시도명이 metro_list에 있으면
            city_len = len(df.시군구명[i].split())
            if city_len == 1:                            #### '시군구명'이 띄어쓰기로 안 기록되어 있으면
                if df.시군구명[i][:-1] == '고성':
                    if df.시도명[i] == '강원도':
                        city_name[i] = '고성(강원)'
                    else:
                        city_name[i] = '고성(경남)'
                elif df.시군구명[i].find('세종') == 0:
                    city_name[i] = '세종'
                else:
                    city_name[i] = df.시군구명[i][:-1]   # 세종, 광명, 김포, 강릉
            else:                                        #### '시군구명'이 띄어쓰기로 기록되어 있으면
                admin_gu = df.시군구명[i].split()[-1]    #### '시군구명' split의 마지막을 admin_gu로 저장
                for key, value in tmp_gu_dict.items():
                    if admin_gu in value:
                        if len(admin_gu) == 2:     #포함 북구, 포항 남구
                            city_name[i] = key + ' ' + admin_gu
                        elif len(admin_gu) == 5:   # 창원 합포, 창원 회원
                            city_name[i] = key + ' ' + admin_gu[2:-1]
                        else:                      # 수원 팔달, 용인 수지
                            city_name[i] = key + ' ' + admin_gu[:-1]
    return city_name


# In[29]:


starbucks['ID'] = get_ID(starbucks)
starbucks


# In[38]:


coffeebean['ID'] = get_ID(coffeebean)
ediya['ID'] = get_ID(ediya)
paik['ID'] = get_ID(paik)


# In[39]:


starbucks.ID.nunique(), coffeebean.ID.nunique(), ediya.ID.nunique(), paik.ID.nunique()


# ####  모든 단위 도시를 합한 합집합: set

# In[40]:


# 중복 없이 합침
set(starbucks.ID.unique())


# In[44]:


city_set = set(starbucks.ID.unique()) | set(coffeebean.ID.unique()) | set(ediya.ID.unique()) | set(paik.ID.unique())
len(city_set)


# In[45]:


# starbucks는 있고, ediya / paik가 없는 곳
set(starbucks.ID.unique()) - set(ediya.ID.unique()) - set(paik.ID.unique())


# In[47]:


starbucks.head()


# In[82]:


# 브랜드별 지역별 매장수 계산
pt_sb = starbucks.groupby('ID')[['상호명']].count()
pt_sb.head()


# In[83]:


pt_sb.reset_index(inplace = True)
pt_sb.rename(columns ={'상호명':'스타벅스'}, inplace = True)
pt_sb.head()


# In[84]:


pt_cb = coffeebean.groupby('ID')[['상호명']].count()
pt_ed = ediya.groupby('ID')[['상호명']].count()
pt_pk = paik.groupby('ID')[['상호명']].count()


# In[85]:


pt_cb.head()


# In[86]:


pt_cb.reset_index(inplace = True)
pt_ed.reset_index(inplace = True)
pt_pk.reset_index(inplace = True)


# In[87]:


pt_cb.head()


# In[88]:


pt_cb.rename(columns ={'상호명':'커피빈'}, inplace = True)
pt_ed.rename(columns ={'상호명':'이디야'}, inplace = True)
pt_pk.rename(columns ={'상호명':'빽다방'}, inplace = True)
pt_cb.head()


# In[89]:


len(pt_sb), len(pt_cb), len(pt_ed), len(pt_pk)


# In[90]:


# merge로 커피데이터 병합
cf = pd.merge(pt_ed, pt_sb, how = 'left')          # how 'outer'로 하면 누락없이 합침
cf.head()


# In[91]:


cf = pd.merge(cf, pt_cb, how = 'left') 
cf = pd.merge(cf, pt_pk, how = 'left') 
cf.fillna(0, inplace = True)
cf.dtypes


# In[93]:


cf.스타벅스 = cf.스타벅스.astype(int)
cf.커피빈 = cf.커피빈.astype(int)
cf.빽다방 = cf.빽다방.astype(int)
cf.이디야 = cf.이디야.astype(int)
cf.dtypes


# In[94]:


cf.head()


# In[95]:


cf['커피지수'] = (cf.스타벅스 + cf.커피빈) / (cf.이디야 + cf.빽다방)
cf.head()


# In[126]:


cf.to_csv('./data1/커피지수.csv', index = False)    # 저장할 때는 index = False로 저장할 것!


# In[100]:


cf2 = pd.merge(pt_ed, pt_sb, how = 'outer')          # how 'outer'로 하면 누락없이 합침
cf2 = pd.merge(cf2, pt_cb, how = 'outer')          # how 'outer'로 하면 누락없이 합침
cf2 = pd.merge(cf2, pt_pk, how = 'outer')          # how 'outer'로 하면 누락없이 합침
cf2


# In[102]:


cf3 = pd.merge(pt_ed,pd.merge(pt_sb, pd.merge(pt_cb, pt_pk, how = 'outer'), how ='outer'), how = 'outer')
cf3.head()


# In[106]:


cf2.fillna(0, inplace = True)
cf2.head()


# ### ★ merge
# left, right 끼리만 합침
# how = 'inner', 'outer','left','right 

# In[110]:


df1 = pd.DataFrame({
    '고객번호': [1001,1002,1003,1004,1005,1006,1007],
    '이름': ['둘리','도우너','또치','길동','희동','마이콜','영희']
    })
df2 = pd.DataFrame({
    '고객번호': [1001,1001,1005,1006,1008,1001],
    '금액': [10000,20000,15000,5000,100000,30000]
    })


# In[111]:


pd.merge(df1, df2)   # default : how = inner값임


# In[125]:


pd.merge(df1, df2, how = 'outer')


# In[116]:


pd.concat([df1, df2]).head()


# In[123]:


pd.concat([df1, df2], join='outer', axis = 1)


# In[ ]:




