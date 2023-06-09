#!/usr/bin/env python
# coding: utf-8

# ### 미세먼지데이터 시각화 실습
# 
# PM 10    미세먼지 /   PM 2.5   초미세먼지
# 

# 서울열린데이터광장> 서울시 대기오염 검색> 대기오염 측정정보 데이터 활용
# https://data.seoul.go.kr/dataList/OA-15526/S/1/datasetView.do
# 
# AIR_HOUR_10YEAR.csv
# 
# 
# 기상청> 기상자료개방포털
# https://data.kma.go.kr/cmmn/main.do
# 
# 자료형태: 시간자료, 2021.1.1.~ 2021. 12. 31. /서울특별시 / 기온, 풍속, 풍향, 습도
# CLIMATE_HOUR_2021.csv
# 
# 
# 방위표 는 방향 설명

# In[ ]:


미세먼지와 초미세먼지와의 상관관계
get_ipython().run_line_magic('pinfo', '있나')
기후요소는 미세먼지에 어떤 영향을 끼치나
내가사는 동네 미세먼지 농도 


# ## 같이 해보기

# 1. 전처리
# 
# ***AIR HOUR 2021.csv 불러오기

# 측정항목 코드 8,9번만 체크
# 
# 측정기상태 0만 체크
# 
# 측정기상태, 국가기준 초과구분,..~ 이후 열 모두 제거
# 
# 측정일시 텍스트로 변경
# 
# 측정일시 열분할, 문자수 기준 왼쪽부터 8개 분리
# 
# 측정일시.2 시간으로 변경
# 
# 측정일시.1 날짜로 변경
# 
# 측정일시.1, 2 열병합 : '측정일시'로, 구분기호'공백'으로 합치기 
# 
# '측정일시' 날짜/시간으로 변경
# 
# 측정항목코드 텍스트로 변경, 8: 미세먼지, 9: 초미세먼지 로 변경
# 
# 측정항목코드 선택 > 변환 > 피벗 열 > 평균값, 고급옵션: 평균
# 
# 측정시간, 오름차순 정렬
# 
# 측정소코드, 오름차순 정렬
# 
# null값: 미세먼지, 초미세먼지 선택> 변환> (아래로)채우기

# ***CLIMATE HOUR.csv 불러오기

# In[ ]:


풍향, 데이터명세에 따라 조건에 맞는 열 추가하기:

데이터변환

열 추가> 조건열> 이름: 풍향명, 

조건: 명세서 보고 추가, 기타값에null 추가

지점명 제거


# ***AIR LOCATION.csv 불러오기

# 측정소코드: 숫자필터 > 작거나 같음, 125 (코드 1~125까지가 서울시임)
# 
# ##서울시 데이터만 있어서 그대로 써도 되지만, 참고삼아 해봄
# 

# ***인구이동_2021 코드.xlsx 불러오기
# 
# '행정구역코드 등록 및 말소내역' sheet 선택

# 첫 행을 머리글로 사용, 2번 
# 
# 쿼리창에서 AIR LOCATION 선택 > 홈> 결합> 쿼리병합 > '측정소이름' 열 선택 > 빈칸: 행정구역등록 및 말소 내역 > '시군구' 선택 > 조인 종류: 왼쪽 외부
# 확장버튼 ←→ 클릭 > '행자부코드', '시도'만 클릭, 원래 열 이름을 접두사로 사용 체크 > 확인
# 
# '행정구역코드등록 및 말소내역. 시도': '서울특별시'만 체크
# 
# '행정구역코드등록 및 말소내역. 코드': 변환> 표준> 정수로 나누기 > 값: 100000
# 
# '측정소 이름' 선택> 홈 > 행 제거 > 중복된 항목 제거
# 
# 표시순서, 공인코드, 행정구역코드등록 및 말소내역. 시도 : 열 제거 (분석에서 사용 안 함
# 
# 쿼리: 행정구역코드 등록 및 말소내역 > 우클릭 > 로드 사용 체크 해제
# 
# 닫기 믿 적용

# ***AIR HOUR 10YEAR.csv 불러오기 

# In[ ]:





# 2. 모델링
# 
# AIR HOUR  2021 측정일시, CLIMATE HOUR 2021 일시 와 연결
# 
# AIR LOCATION, AIR  HOUR 10YEAR 측정소코드 연결

# 

# 3. 시각화

# **참고: 상관관계 
# 
# 양(+)/음(-)/-1이나 1에 가까울수록 상관관계 있음/ 0에 가까울수록 상관관계가 없음
# 
# $$ \frac{\sum(x_i - \overline{x})(y_i - \overline{y})}{\sqrt{(\sum(x_i - \overline{x})^2 \sum(y_i - \overline{y})^2}}  $$

# 1p 미세먼지와 초미세먼지와의 상관관계
# 
# 상관관계: x축 미세먼지, y축 초미세먼지 , 요약안함 체크!
# 
# AIR HOUR 우클릭 > 빠른 새 측정값 > 계산: 상관계수, 범주: 측정일시, 측정값X: 미세먼지, 측정값Y: 초미세먼지 선택
# 상관관계 

# In[ ]:


get_ipython().run_line_magic('pinfo', '있나')

AIR HOUR 10YEAR
y축: 미세먼지/ 초미세먼지, 평균값
돋보기모양: 추세선, 계열결합 해제
    
미세먼지/ 초미세먼지, 개수
고급필터, 보다 큼, 초미세먼지 35, 미세먼지 100 이상


# 3p 기후요소는 미세먼지에 어떤 영향을 끼치나
# 
# 기온, 습도, 풍속, 평균값
# 풍향, 개수
# 기온과 미세먼지의 관계: 기온,미세먼지, 요약안함
# 풍속 분포: 평균

# 4p 내가사는 동네 미세먼지 농도 
# 
# 지역별 미세먼지 수치, 합계로(??)
# 
# 데이터보기, AIR LOCATION, 행정구역코드 등록 및.행자부코드 선택> '행자부코드' 이름변경
# 
# 행자부코드, 텍스트로 형식변경
# 
# 보고서보기, 위치별 미세먼지 현황,
# 위치: 행자부코드, 색 채도: 미세먼지 합계, 도구설명: 측정소이름
# 
