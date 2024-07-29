# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 15:04:35 2024

@author: jcp
"""

import sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV

df = pd.read_csv("./preprocessed/merged_data.csv", index_col=0)

# LabelEncoder 클래스를 불러옵니다.
from sklearn.preprocessing import LabelEncoder

# LabelEncoder를 객체로 생성합니다.
le = LabelEncoder()

# fit_transform()으로 라벨인코딩을 수행합니다.
df['소멸위험등급'] = le.fit_transform(df['소멸위험등급'])

y = df['소멸위험등급']
X = df.iloc[:,1:-2]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)
# RandomizedSearchCV 사용이유 
# GridSearchCV와 달리, RandomizedSearchCV는 하이퍼파라미터 공간의 모든 조합을 시도하지 않고,
# 사용자 지정 개수(n_iter)만큼의 조합을 랜덤하게 선택합니다. 이렇게 함으로써 계산 시간을 절약하면서도 다양한 설정을 탐색할 수 있습니다.
# 하이퍼파라미터의 범위 내에서 무작위로 조합을 선택하여 시험합니다. 그리드 탐색보다 빠르지만, 최적의 조합을 찾을 확률은 낮아질 수 있습니다. 

#%%
# 의사결정나무 DecisionTree
'''
criterion : 분할 성능 측정 기능

min_samples_split : 노드를 분할하기 위한 최소한의 샘플 데이터수로, 과적합을 제어하는데 주로 사용함.
작게 설정할 수록 분할 노드가 많아져 과적합 가능성이 높아짐

max_depth : 트리의 최대 깊이, 깊이가 깊어지면 과적합될 수 있음.

max_features : 최적의 분할을 위해 고려할 최대 feature 개수
(default = None : 데이터 세트의 모든 피처를 사용)

samples_leaf : 리프노드가 되기 위해 필요한 최소한의 샘플 데이터수 (과적합 제어 용도), 작게 설정 필요

max_leaf_nodes : 리프노드의 최대 개수

param_distributions : 튜닝을 위한 대상 파라미터, 사용될 파라미터를 딕셔너리 형태로 넣어준다.

n_iter : 파라미터 검색 횟수

best score: 최고 평균 정확도 수치
'''
# 최적의 파라미터 조합찾기
dt_clf = DecisionTreeClassifier(random_state=1)

param_dist = {
    'criterion':['gini','entropy'], 
    'max_depth':[None,2,3,4,5,6], 
    'max_leaf_nodes':[None,2,3,4,5,6,7], 
    'min_samples_split':[2,3,4,5,6], 
    'min_samples_leaf':[1,2,3], 
    #'max_features':[None,'sqrt','log2',3,4,5]
    }

rand_search = RandomizedSearchCV(dt_clf, param_distributions = param_dist, n_iter = 50, cv = 5, scoring = 'accuracy', refit=True)
rand_search.fit(X_train, y_train)

print('best parameters : ', rand_search.best_params_)

print('best score : ', round(rand_search.best_score_, 4))

result = pd.DataFrame(rand_search.cv_results_)

#%%
from sklearn.tree import DecisionTreeClassifier

# 최적의 파라미터로 모델 초기화
best_params = rand_search.best_params_
best_model = DecisionTreeClassifier(
    criterion=best_params['criterion'],
    max_depth=best_params['max_depth'],
    max_leaf_nodes=best_params['max_leaf_nodes'],
    min_samples_split=best_params['min_samples_split'],
    min_samples_leaf=best_params['min_samples_leaf'],
    random_state=1
)
# 모델 학습
best_model.fit(X_train, y_train)
#%%
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 테스트 데이터에 대한 예측
y_pred = best_model.predict(X_test)

# 모델 성능 평가
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(report)
print("Confusion Matrix:")
print(conf_matrix)

#%%
# LightGBM
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score

# LightGBM 모델 초기화
lgb_clf = lgb.LGBMClassifier(random_state=1)
'''
num_leaves: 트리의 잎사귀 수.
learning_rate: 학습률.
n_estimators: 트리의 수.
max_depth: 트리의 최대 깊이.
min_child_samples: 리프 노드의 최소 샘플 수.
subsample: 데이터의 일부를 샘플링할 비율.
colsample_bytree: 각 트리를 학습할 때 사용하는 특성의 비율.'''
# 하이퍼파라미터 공간 정의
param_dist_lgb = {
    'num_leaves': [31, 50, 70],
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [100, 200, 300],
    'max_depth': [-1, 10, 20],
    'min_child_samples': [5, 10, 20],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0]
}

# RandomizedSearchCV 수행
rand_search_lgb = RandomizedSearchCV(lgb_clf, param_distributions=param_dist_lgb, n_iter=50, cv=5, scoring='accuracy', random_state=1)
rand_search_lgb.fit(X_train, y_train.values.ravel())  # y_train.values.ravel()는 y_train을 1차원 배열로 변환합니다.

print('Best parameters:', rand_search_lgb.best_params_)
print('Best score:', round(rand_search_lgb.best_score_, 4))


# 최적의 모델로 평가
best_lgb_model = rand_search_lgb.best_estimator_
y_pred_lgb = best_lgb_model.predict(X_test)
print(f"LightGBM Accuracy: {accuracy_score(y_test, y_pred_lgb):.4f}")



#%%
import lightgbm as lgb
from sklearn.metrics import accuracy_score

# 최적의 하이퍼파라미터를 사용하여 LightGBM 모델 초기화
best_params = rand_search_lgb.best_params_
lgb_clf_best = lgb.LGBMClassifier(
    num_leaves=best_params['num_leaves'],
    learning_rate=best_params['learning_rate'],
    n_estimators=best_params['n_estimators'],
    max_depth=best_params['max_depth'],
    min_child_samples=best_params['min_child_samples'],
    subsample=best_params['subsample'],
    colsample_bytree=best_params['colsample_bytree'],
    random_state=1
)

# 최적의 파라미터로 모델 학습
lgb_clf_best.fit(X_train, y_train.values.ravel())

# 테스트 데이터에서 예측 수행
y_pred_lgb = lgb_clf_best.predict(X_test)

# 정확도 평가
accuracy = accuracy_score(y_test, y_pred_lgb)
print(f"LightGBM Accuracy with optimized parameters: {accuracy:.4f}")

# 예측 결과의 혼동 행렬과 분류 리포트 출력 (선택 사항)
from sklearn.metrics import confusion_matrix, classification_report

conf_matrix = confusion_matrix(y_test, y_pred_lgb)
print("Confusion Matrix:")
print(conf_matrix)

class_report = classification_report(y_test, y_pred_lgb)
print("Classification Report:")
print(class_report)



#%%
#XGboost
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# 데이터 불러오기
t = pd.read_csv('C:/Users/Shin/Documents/Final_Project/Data/교육_전국/교육_연도별_전국통합/2015_소멸등급.csv')
d = pd.read_excel("C:/Users/Shin/Documents/Final_Project/Data/교육_전국/교육_연도별_전국통합/교육/EXCEL/교육_2015_전국.xlsx")

X =  d[['교원_1인당_학생수_유치원', '교원_1인당_학생수_초등학교', '교원_1인당_학생수_중학교', '교원_1인당_학생수_고등학교',
        '유치원_학급당 학생 수 (명)', '초등학교_학급당 학생 수 (명)', '중학교_학급당 학생 수 (명)','고등학교_학급당 학생 수 (명)',
        '학교교과 교습학원 (개)', '평생직업 교육학원 (개)', '사설학원당 학생수 (명)','유치원생 수', '초등학생 수']]

y = t['2015_등급']

# 클래스 레이블을 0부터 시작하도록 변환
y = y - 1

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)

# XGBoost 모델 설정
xgb_clf = xgb.XGBClassifier(random_state=1)

# 하이퍼파라미터 그리드 설정
param_dist = {
    'n_estimators': [50, 100, 150, 200],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.1, 0.2, 0.3],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],
    'gamma': [0, 0.1, 0.2, 0.3, 0.4]
}

# RandomizedSearchCV 수행
rand_search = RandomizedSearchCV(xgb_clf, param_distributions=param_dist, n_iter=50, cv=5, scoring='accuracy', random_state=1)
rand_search.fit(X_train, y_train)

# 최적의 하이퍼파라미터와 성능 확인
print('Best parameters:', rand_search.best_params_)
print('Best score:', round(rand_search.best_score_, 4))

# 최적의 모델로 예측 수행 및 평가
best_model = rand_search.best_estimator_
y_pred = best_model.predict(X_test)
print('Test Accuracy:', accuracy_score(y_test, y_pred))
'''
Best parameters: {'subsample': 0.8, 'n_estimators': 100, 'max_depth': 3, 'learning_rate': 0.3, 'gamma': 0.4, 'colsample_bytree': 0.6}
Best score: 0.3629
Test Accuracy: 0.46551724137931033'''
#%%
import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 최적의 하이퍼파라미터로 XGBoost 모델 생성
best_params = {'subsample': 0.8, 'n_estimators': 100, 'max_depth': 3, 'learning_rate': 0.3, 'gamma': 0.4, 'colsample_bytree': 0.6}
xgb_clf_optimized = xgb.XGBClassifier(**best_params, random_state=1)

# 최적의 모델로 학습
xgb_clf_optimized.fit(X_train, y_train)

# 예측 수행
y_pred = xgb_clf_optimized.predict(X_test)

# 정확도 평가
accuracy = accuracy_score(y_test, y_pred)
print('Test Accuracy:', accuracy)

# 혼동 행렬 및 분류 보고서 출력
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))

print('Classification Report:')
print(classification_report(y_test, y_pred))