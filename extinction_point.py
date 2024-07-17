# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:48:25 2024

@author: jcp
"""

import pandas as pd

df = pd.read_csv('행정구역별_5세별_주민등록인구_2015-2023.csv', encoding='euc-kr')

# 마지막 열 제거, 필요없는 열 제거
df = df[df['항목'] != '남자인구수[명]']
df = df.iloc[:,:-1]
df = df.drop(columns='단위')

'''가임기 여성 데이터 전처리'''
# '5세별' 열에서 특정 연령대에 해당하는 데이터 필터링
age_woman = ['15 - 19세', '20 - 24세', '25 - 29세', '30 - 34세', '35 - 39세', '40 - 44세', '45 - 49세']

# 가임기 여성인구 필터링
df_filtered = df[df['5세별'].isin(age_woman)]
woman_df = df_filtered[df_filtered['항목'] == '여자인구수[명]']
woman_df.drop(columns=['항목', '5세별'], inplace=True)

# 행정구역별 합계 계산
woman_df_grouped = woman_df.groupby('행정구역(동읍면)별').sum()

# 행정구역명을 index로 설정


# %%
'''65세 이상 노인인구 데이터 전처리'''
# 
oldman_df = df[~df['5세별'].isin(age_woman)]
oldman_df.drop(columns=['항목', '5세별'], inplace=True)

# 행정구역별 합계 계산
oldman_df_grouped = oldman_df.groupby('행정구역(동읍면)별').sum()
# %%
'''지역별 소멸위험지수 계산'''
ext_point = woman_df_grouped / oldman_df_grouped

# 엑셀파일 저장
ext_point.to_excel("기존_소멸위험지수_2015-2023.xlsx")
# csv
ext_point.to_csv("기존_소멸위험지수_2015-2023.csv")