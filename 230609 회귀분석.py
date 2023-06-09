#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# ### 회귀분석 예제
# 
# https://datascienceschool.net/03%20machine%20learning/04.01%20%ED%9A%8C%EA%B7%80%EB%B6%84%EC%84%9D%20%EC%98%88%EC%A0%9C.html

# #### 당뇨병 진행도 예측

# In[52]:


from sklearn.datasets import load_diabetes
diabetes = load_diabetes()


# In[55]:


df = pd.DataFrame(diabetes.data, columns = diabetes.feature_names)
df.head(3)


# In[56]:


df['target'] = diabetes.target


# In[57]:


df.info()


# In[58]:


# scatter plot
sns.pairplot(df[['target','bmi','bp','s1']])
plt.show()


# ### 선형회귀분석 기초

# In[16]:


import statsmodels.api as sm


# In[5]:


X0 = np.arange(10).reshape(5,2)
X = sm.add_constant(X0)


# ### scikit-learn 패키지 사용

# In[ ]:


# 1) LinearRegression 클래스 객체 생성
model = LinearRegression(fit_intercept = True)  # 상수항 여부, default가 true

# 2) fit 메서드로 가중치값 추정
model = model.fit(X, y)   
model.intercept_, model.coef_  # coef_: 추정된 가중치 벡터, intercept_: 추정된 상수항

# 3) predict 메서드로 새로운 입력 데이터에 대한 출력 데이터 예측
y_new = model.predict(x_new)


# ### statsmodel 패키지 활용

# In[ ]:


# 1) 독립변수와 종속변수가 모두 포함된 데이터프레임 생성, 상수항 결합 안해도 됨

# 2) OLS 클래스 객체 생성. 

model = OLS.from_formula(formula, data = df)
model = OLS.from_formula('y~x', data = df)   # 종속변수 ~ 독립변수
model = OLS(dfy, dfX)   # dfX가 상수항을 갖고 있을 때 사용

# 3) fit메서드로 추정
result = model.fit()

# 4) RegressionResults 클래스 객체는 결과 리포트용 summary 메서드와 prediction 메서드 제공
result.summary()
y_new = result.predict(x_new)    # 예측 데이터는 상수항 결합해줘야 함

# 5) 분석결과 활용
result.params  # 가중치벡터 값 (상수항, 회귀계수)
result.resid  # 잔차 벡터


# In[9]:


from sklearn import datasets
X, y = datasets.fetch_openml('boston', return_X_y=True)


# In[13]:


dfy = pd.DataFrame(y, columns = ['MEDV'])


# In[23]:


dfx = sm.add_constant(X)
dfx


# In[24]:


dfx.info()


# In[30]:


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

dfx['CHAS'] = le.fit_transform(dfx['CHAS'])
dfx['RAD'] = le.fit_transform(dfx['RAD'])


# In[32]:


dfx.info()


# In[33]:


model_bt = sm.OLS(dfy,dfx)
model_bt


# In[35]:


result_bt = model_bt.fit()
print(result_bt.summary())


# In[44]:


dfx.drop('const', axis = 1, inplace = True)


# In[47]:


dfy


# In[45]:


df_boston = pd.concat([dfx,dfy], axis = 1)
df_boston


# In[49]:


model_bt2 = sm.OLS.from_formula('dfy ~' + "+".join(dfx.columns), data=df_boston)
result_bt2 = model_bt2.fit()
print(result_bt2.summary())


# ### 강한 다중공선성이나, 다른 수치적 문제가 있을 수 있음
# - 조건수 conditional number는, 가장 큰 고유치와 가장 작은 고유치의 비율
# - ① 변수들 단위 차이가 큰 경우 >> 스케일링
# <br> ② 상관관계가 큰 독립변수끼리 있는 경우 >> 변수선택 또는 PCA 차원축소

# In[51]:


dfx.describe().loc['std']


# In[53]:


feature_names = list(dfx.columns)
feature_names.remove('CHAS')
feature_names = ['scale({})'.format(name) for name in feature_names] + ['CHAS']
model_bt3 = sm.OLS.from_formula('dfy ~' + "+".join(feature_names), data=df_boston)
result_bt3 = model_bt3.fit()
print(result_bt3.summary())


# ### 범주형 독립변수

# In[ ]:




