# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 08:55:49 2024

@author: jcp
"""

import pandas as pd
# 데이터 로드
df = pd.read_csv("./preprocessed/merged_data.csv", index_col=0)
df2 = pd.read_csv("./preprocessed/merged_data.csv", index_col=0)

# LabelEncoder 클래스를 불러옵니다.
from sklearn.preprocessing import LabelEncoder

# LabelEncoder를 객체로 생성합니다.
le = LabelEncoder()

# fit_transform()으로 라벨인코딩을 수행합니다.
df['소멸위험등급'] = le.fit_transform(df['소멸위험등급'])

# %%


# %%
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
xgb_model=XGBClassifier()

y = df['소멸위험등급']

y.value_counts()

X = df.iloc[:,1:-2]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LGBM 데이터셋 생성
train_data = lgb.Dataset(X_train, label=y_train)

# 하이퍼파라미터 설정
params = {
    # 'objetive': 'binary',
    'metric': 'binary_logloss',
    'num_leaves': 31,
    'learning_rate' : 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0}

# 모델 학습
num_rounds = 100
lgbm_model = lgb.train(params, train_data, num_rounds)

# 모델 평가
y_pred = lgbm_model.predict(X_test)
y_pred = y_pred
# accuracy = sum(y_pred == y_test) / len(y_test)
# print(f"Accuracy: {accuracy}")