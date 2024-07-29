# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 09:52:45 2024

@author: jcp
"""
'''데이터 통합'''

import pandas as pd

# 종속변수 데이터 로드
ext = pd.read_csv('./preprocessed/개선_소멸위험지수_2015-2021.csv', index_col=0)

ext_grade = pd.read_csv('./preprocessed/소멸위험등급_2015-2021.csv', index_col=0)

# 독립변수들 데이터 로드
edu = pd.read_excel('./preprocessed/종합파일들/교육종합.xlsx')
cure = pd.read_excel('./preprocessed/종합파일들/보건종합.xlsx')
water_sup = pd.read_excel('./preprocessed/종합파일들/상하수도종합.xlsx')
local = pd.read_excel('./preprocessed/지역사회건설/지역사회건설_2015~2021_전국_종합.xlsx')
management = pd.read_excel('./preprocessed/종합파일들/행정.xlsx')
social = pd.read_excel('./preprocessed/종합파일들/사회보호.xlsx')
job = pd.read_excel('./preprocessed/종합파일들/업종종합_v0.1.xlsx')

# 로드한 데이터들 열 이름 등 전처리
edu.rename(columns={'행정구역(동읍면)별':'행정구역'}, inplace=True)
cure.rename(columns={'시도별':'행정구역'}, inplace=True)
water_sup.rename(columns={'시도별':'행정구역'}, inplace=True)
local.rename(columns={'시도별':'행정구역'}, inplace=True)
management.rename(columns={'시군구':'행정구역'}, inplace=True)
social.rename(columns={'시도별':'행정구역'}, inplace=True)
job.rename(columns={'시도별':'행정구역'}, inplace=True)

# %%
# 시도 데이터제거
def remove_sido(data): # 시도 데이터 제거 함수
    
    cities = '서울특별시, 부산광역시, 인천광역시, 대구광역시, 대전광역시, 광주광역시, 울산광역시, 경기도, 충청북도, 충청남도, 전라남도, 경상북도, 경상남도, 강원특별자치도, 전북특별자치도, 제주특별자치도'.split(', ')
    years = list(range(2015,2022))
    cities_years = []
    for city in cities:
        for year in years:
            cities_years.append(city+'_'+str(year))
    return data[~data['행정구역'].isin(cities_years)]

ext_grade = remove_sido(ext_grade)
edu = remove_sido(edu)
cure = remove_sido(cure)
water_sup = remove_sido(water_sup)
local = remove_sido(local)
management = remove_sido(management)
social = remove_sido(social)
job = remove_sido(job)


# %%
# 행정구역명이 다르게 처리된 데이터들 찾기
# 두 데이터프레임 병합 (행정구역을 기준으로)
# merged_df = pd.merge(edu, job, on='행정구역', how='outer', indicator=True)

# # 병합 결과에서 공통으로 존재하지 않는 행정구역만 필터링
# different_values_df = merged_df[merged_df['_merge'] != 'both']
# %%
# merge
merged_df = pd.merge(edu, cure, on='행정구역')
merged_df = pd.merge(merged_df, water_sup, on='행정구역')
# merged_df = pd.merge(merged_df, local, on='행정구역')
merged_df = pd.merge(merged_df, management, on='행정구역')
# merged_df = pd.merge(merged_df, social, on='행정구역')
# merged_df = pd.merge(merged_df, job, on='행정구역')
merged_df = pd.merge(merged_df, ext_grade, on='행정구역')

# 결측값 유무 확인
missing_count_per_column = merged_df.isnull().sum() # 없음
# %%
# 파일 저장
merged_df.to_csv('./preprocessed/merged_data.csv')
merged_df.to_excel('./preprocessed/merged_data.xlsx')
# %%
