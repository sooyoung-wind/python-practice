# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 11:23:14 2023

@author: Soo.Y
"""
from konlpy.tag import Okt
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

base_path = 'C:\\Users\\Soo.Y\\Downloads\\open\\'
train = pd.read_csv(base_path + "train.csv")
test = pd.read_csv(base_path + "test.csv")
submission = pd.read_csv(base_path + "sample_submission.csv")

train.columns = ["ID", "weeks", "shop_num", 'price', 'promotion',
                 'city', 'region', 'shop_type', 'gift', 'target']
test.columns = ["ID", "weeks", "shop_num", 'price', 'promotion',
                'city', 'region', 'shop_type', 'gift']

# ID 불필요 개별로 1개씩 있음
# 추석까지 남은 기간 weeks 필요 0 :1996, 1:1978, 2:1989
train.weeks.value_counts()
test.weeks.value_counts()


def my_process_define(train):
    # 쇼핑몰 구분 필요
    # 쇼핑몰 54 => int 54
    train['shop_num'] = train.shop_num.map(lambda x: int(x.split(" ")[1]))

    # 도시, 지역, 쇼핑몰 유형 숫자형으로 변경
    train['city'] = train.city.map(lambda x: int(x.split(" ")[1]))
    train['region'] = train.region.map(lambda x: int(x.split(" ")[1]))
    train['shop_type'] = train.shop_type.map(lambda x: int(x.split(" ")[2]))

    # create gift set category
    for for_name in gift_set:
        train[for_name] = 0

    for idx, gift_full_name in enumerate(train.gift):
        for gift_word in gift_set:
            if gift_word in gift_full_name:
                train[gift_word][idx] = 1
    # only gift_factorize
    # train['gift_factorize'] = pd.factorize(train.gift, sort=True)[0]

    # train['프리미엄'] = 0
    # train['최고급'] = 0
    # train['한우'] = 0
    # train['명품'] = 0
    # train['새우'] = 0
    # for idx, gift_name in enumerate(train.gift):
    #     if '프리미엄' in gift_name:
    #         train['프리미엄'][idx] = 1
    #     if '최고급' in gift_name:
    #         train['최고급'][idx] = 1
    #     if '한우' in gift_name:
    #         train['한우'][idx] = 1
    #     if '명품' in gift_name:
    #         train['명품'][idx] = 1
    #     if '새우' in gift_name:
    #         train['새우'][idx] = 1


train.groupby('gift').agg({'target': 'count'})

train.pivot_table(index=['city', 'region', 'shop_type', 'shop_num', 'gift'], values='target', aggfunc='count')

#####################
# data split
#####################

x = train.drop(columns=['ID', 'target'])
# x = train.drop(columns=['ID', 'target', 'gift'])
y = train['target']


idx = list(range(train.shape[0]))
x_train_idx, x_valid_idx, y_train_idx, y_valid_idx = train_test_split(idx, idx, test_size=0.3, random_state=9234)

#####################
# random forest
#####################

evaluation_metric = mean_squared_error
rf_model = RandomForestRegressor()
rf_params = {'random_state': [9234], 'n_estimators': [300, 500],
             'max_depth': [30, 60], 'min_samples_split': [6, 8]}
gridsearch_random_foreset_model = GridSearchCV(estimator=rf_model,
                                               param_grid=rf_params,
                                               cv=5)

gridsearch_random_foreset_model.fit(x.iloc[x_train_idx], y.iloc[y_train_idx])


gridsearch_random_foreset_model.score(x.iloc[x_train_idx], y.iloc[y_train_idx])
gridsearch_random_foreset_model.score(x.iloc[x_valid_idx], y.iloc[y_valid_idx])
gridsearch_random_foreset_model.score(x, y)

gridsearch_random_foreset_model.best_estimator_

###################
# 단일 파라미터 동작
###################

rf_model = RandomForestRegressor(n_estimators=100,
                                 # criterion = evaluation_metric,
                                 oob_score=True,
                                 max_depth=10,
                                 min_samples_split=20,
                                 min_samples_leaf=10,
                                 random_state=9234)

# rf_model.fit(x.iloc[x_train_idx], y.iloc[y_train_idx])
rf_model.fit(x, y)

rf_model.score(x.iloc[x_train_idx], y.iloc[y_train_idx])
rf_model.score(x.iloc[x_valid_idx], y.iloc[y_valid_idx])
rf_model.score(x, y)

#######################
# Test
#######################
test_input = test.copy()
my_process_define(test_input)
test_input = test_input.drop(columns=['ID', 'gift'])

submission['수요량'] = rf_model.predict(test_input)
submission.to_csv(base_path + "soo_submission.csv", index=False)

#######################
# Factorize of Gift
#######################
my_process_define(train)
x = train.drop(columns=['ID', 'target', 'gift'])
y = train['target']

# 0.64 정도 나옴

#######################
# one-hot encoding of Gift
#######################
my_process_define(train)
train = pd.get_dummies(data=train, columns=['gift'])
x = train.drop(columns=['ID', 'target'])
y = train['target']

# 0.64 정도 나옴

#######################
# self Gift category
#######################

temp_1 = train.gift.value_counts()
temp_2 = [ii for ii in temp_1.index]

gift_set = set()
for words in temp_2:
    for word in Okt().nouns(words):
        gift_set.add(word)

gift_set

for for_name in gift_set:
    train[for_name] = 0
