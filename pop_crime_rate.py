# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 16:14:23 2024

@author: jcp
"""


import pandas as pd


''' 범죄율 데이터 정제'''
crime_df = pd.read_excel('./data/안전/범죄율(세종_충북_충남).xlsx', header=2)

crime_df = crime_df.drop(0, axis=0)

crime_df = crime_df.iloc[:-4, 1:]

crime_df = crime_df.rename(columns={'Unnamed: 1':'loc'})

df_melted = crime_df.melt(id_vars=['loc'], var_name='year', value_name='crime_rate')

# %%
'''인구밀도 데이터 정제'''
pop_df = pd.read_excel('./data/인구이동/인구밀도.xlsx', header=1)

filtered_df = pop_df[pop_df['항목'].str.contains('세종|충청')]

filtered_df = filtered_df.iloc[:,:-1]

pop_melted = filtered_df.melt(id_vars=['항목'], var_name='year', value_name='pop_by_land')

# %%

'''데이터 병합'''
merged = pd.concat([df_melted.loc[:, 'crime_rate'], pop_melted.loc[:, 'pop_by_land']], axis=1)


# %%

'''산점도 그리기'''

import matplotlib.pyplot as plt

# 예시 데이터프레임 생성 (실제 데이터를 사용해야 함)
# 여기서는 예시로 데이터프레임을 생성하지 않고 있습니다. 실제 데이터를 사용할 때는 데이터프레임을 정의해야 합니다.
# merged = ...

# 산점도 그리기
plt.figure(figsize=(8, 6))  # 그림 크기 설정
plt.scatter(merged['pop_by_land'], merged['crime_rate'], alpha=0.5)  # 산점도 그리기
plt.title('Scatter Plot of Population by Land vs. Crime Rate')  # 제목 설정
plt.xlabel('Population by Land')  # x축 레이블 설정
plt.ylabel('Crime Rate')  # y축 레이블 설정
plt.grid(True)  # 그리드 표시
plt.show()