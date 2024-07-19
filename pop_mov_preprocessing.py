# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:48:25 2024

@author: jcp
"""

import pandas as pd

df = pd.read_excel('시군구별_인구이동.xlsx')

# 결측치 확인
df.info()


# %%

# 데이터 탐색
df['행정구역(시군구)별'].unique()

# \u3000 제거
df['행정구역(시군구)별'] = df['행정구역(시군구)별'].str.replace('\u3000', '')
df['행정구역(시군구)별'] = df['행정구역(시군구)별'].str.replace('  ', '')

# 필요없는 행 제거

df.info()
# %%
# 시군구 중복 지명 구분 처리

seoul_dstr = '강남구, 강동구, 강북구, 강서구, 관악구, 광진구, 구로구, 금천구, 노원구, 도봉구, 동대문구, 동작구, 마포구, 서대문구, 서초구, 성동구, 성북구, 송파구, 양천구, 영등포구, 용산구, 은평구, 종로구, 중구, 중랑구'.split(', ')
incheon_dstr = '중구, 동구, 미추홀구, 연수구, 남동구, 부평구, 계양구, 서구, 강화군, 옹진군, 남구'.split(', ')
busan_dstr = '중구, 서구, 동구, 영도구, 부산진구, 동래구, 남구, 북구, 해운대구, 사하구, 금정구, 강서구, 연제구, 수영구, 사상구, 기장군'.split(', ')
daegu_dstr = '중구, 동구, 서구, 남구, 북구, 수성구, 달서구, 달성군, 군위군'.split(', ')
gwangju_dstr = '동구, 서구, 남구, 북구, 광산구'.split(', ')
daejeon_dstr = '동구, 중구, 서구, 유성구, 대덕구'.split(', ')
ulsan_dstr = '중구, 남구, 동구, 북구, 울주군'.split(', ')

gyunggi_cities = '수원시,용인시,고양시,화성시,성남시,부천시,남양주시,안산시,평택시,안양시,시흥시,파주시,김포시,의정부시,광주시,하남시,광명시,군포시,양주시,오산시,이천시,안성시,구리시,의왕시,포천시,양평군,여주시,동두천시,과천시,가평군,연천군'.split(',')
gangwon_cities = '춘천시,원주시,강릉시,동해시,태백시,속초시,삼척시,홍천군,횡성군,영월군,평창군,정선군,철원군,화천군,양구군,인제군,고성군,양양군'.split(',')
chungbuk_cities = '청주시,충주시,제천시,보은군,옥천군,영동군,증평군,진천군,괴산군,음성군,단양군'.split(',')
chungnam_cities = '천안시,공주시,보령시,아산시,서산시,논산시,계룡시,당진시,금산군,부여군,서천군,청양군,홍성군,예산군,태안군'.split(',')
jeonbuk_cities = '전주시,군산시,익산시,정읍시,남원시,김제시,완주군,진안군,무주군,장수군,임실군,순창군,고창군,부안군'.split(',')
jeonnam_cities = '목포시,여수시,순천시,나주시,광양시,담양군,곡성군,구례군,고흥군,보성군,화순군,장흥군,강진군,해남군,영암군,무안군,함평군,영광군,장성군,완도군,진도군,신안군'.split(',')
gyungbuk_cities = '포항시,경주시,김천시,안동시,구미시,영주시,영천시,상주시,문경시,경산시,의성군,청송군,영양군,영덕군,청도군,고령군,성주군,칠곡군,예천군,봉화군,울진군,울릉군'.split(',')
gyungnam_cities = '창원시,진주시,통영시,사천시,김해시,밀양시,거제시,양산시,의령군,함안군,창녕군,고성군,남해군,하동군,산청군,함양군,거창군,합천군'.split(',')
jeju_cities = '제주시,서귀포시'.split(',')

# 행정구역 순서 파악하기
cities_dict = {}
cities = '서울특별시, 부산광역시, 인천광역시, 대구광역시, 대전광역시, 광주광역시, 울산광역시, 경기도, 충청북도, 충청남도, 전라남도, 경상북도, 경상남도, 강원특별자치도, 전북특별자치도, 제주특별자치도'.split(', ')
for city in cities:
    index = next(iter(df[df['행정구역(시군구)별'] == city].index), None)
    cities_dict[city] = index
    print(city, index)
    
# 순서대로 시도 목록 정렬
cities_dict = dict(sorted(cities_dict.items(), key=lambda x: x[1]))
# cities_tup = sorted(cities_dict.items(), key=lambda x: x[1])

# 시도명-시군구list 형태로 딕셔너리 생성
cities_dstr = dict(zip(list(cities_dict.keys()),[seoul_dstr,busan_dstr,daegu_dstr,incheon_dstr,gwangju_dstr,daejeon_dstr,ulsan_dstr,gyunggi_cities, gangwon_cities,chungbuk_cities,chungnam_cities,jeonbuk_cities,jeonnam_cities,gyungbuk_cities,gyungnam_cities,jeju_cities]))

# 시군구 앞에 시도명을 접두사로 추가
i = 0
index = list(cities_dict.values())
for city in cities_dstr:
    
    i+=1
    if i >= len(cities_dstr):
        df.loc[:,'행정구역(시군구)별'] = df['행정구역(시군구)별'].apply(lambda x: f'{city} {x}' if x in cities_dstr[city] else x) 
        break
    df.loc[:index[i],'행정구역(시군구)별'] = df['행정구역(시군구)별'].apply(lambda x: f'{city} {x}' if x in cities_dstr[city] else x)
    
# %%
# 인천광역시 남구(현 미추홀구) 데이터 결합
df_michuholgu = df[df['행정구역(시군구)별'] =='인천광역시 미추홀구'].replace('-', 0)
df_namgu = df[df['행정구역(시군구)별'] =='인천광역시 남구'].set_index(df_michuholgu.index)
df_mic = df_michuholgu + df_namgu

df2 = df.drop(df[df['행정구역(시군구)별'] =='인천광역시 남구'].index)

df2.update(df_mic.iloc[:,1:], overwrite=True)

# 경상북도 군위군(현 대구광역시) 데이터 결합
gunwi_daegu = df2[df2['행정구역(시군구)별'] =='대구광역시 군위군'].replace('-', 0)
gunwi_gyungbuk = df2[df2['행정구역(시군구)별'] =='군위군'].set_index(gunwi_daegu.index)
df_gun = gunwi_daegu + gunwi_gyungbuk
df3 = df2.drop(df2[df2['행정구역(시군구)별'] =='군위군'].index)

df3.update(df_gun.iloc[:,1:], overwrite=True)

# 결측치 확인
df3.info()

# 사라진 시군구 행 제거

df4 = df3.set_index('행정구역(시군구)별')
df4 = df4.dropna(axis=0, how='all')
    
# %%
'''가임기 여성 데이터 전처리'''
# '5세별' 열에서 특정 연령대에 해당하는 데이터 필터링
age_woman = ['15 - 19세', '20 - 24세', '25 - 29세', '30 - 34세', '35 - 39세', '40 - 44세', '45 - 49세']

# 가임기 여성인구 필터링
df_filtered = df3[df3['5세별'].isin(age_woman)]
woman_df = df_filtered[df_filtered['항목'] == '여자인구수[명]']
woman_df.drop(columns=['항목', '5세별'], inplace=True)

# 행정구역별 합계 계산
woman_df_grouped = woman_df.groupby('행정구역(동읍면)별').sum()

# %%
'''65세 이상 노인인구 데이터 전처리'''
# 
oldman_df = df3[~df3['5세별'].isin(age_woman)]
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
