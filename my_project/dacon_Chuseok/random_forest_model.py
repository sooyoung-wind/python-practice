# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 17:54:47 2023

@author: Soo.Y
"""

from sklearn.metrics import make_scorer
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

#######################
# self Gift category
#######################

temp_1 = train.gift.value_counts()
temp_2 = [ii for ii in temp_1.index]

gift_set = set()
for words in temp_2:
    for word in Okt().nouns(words):
        if len(word) > 1:
            gift_set.add(word)

#######################
# 전처리
#######################


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


#####################
# data split
#####################

my_process_define(train)
x = train.drop(columns=['ID', 'target', 'gift'])
y = train['target']


# index
idx = list(range(train.shape[0]))
x_train_idx, x_valid_idx, y_train_idx, y_valid_idx = train_test_split(idx, idx, test_size=0.3, random_state=9234)


#####################
# random forest & Grid serach
#####################
evaluation_metric = mean_squared_error


def my_rmse(true, pred, sample_weight=None):
    return np.sqrt(np.mean((true - pred)**2))


rmse_scorer = make_scorer(lambda y_true, y_pred: np.sqrt(mean_squared_error(y_true, y_pred)), greater_is_better=False)

evaluation_metric = make_scorer(my_rmse, greater_is_better=False)


rf_model = RandomForestRegressor()
rf_params = {'random_state': [9234], 'n_estimators': [500, 1000, 2000],
             'max_depth': [30, 60], 'min_samples_split': [3, 5, 10]}
gridsearch_random_foreset_model = GridSearchCV(estimator=rf_model,
                                               param_grid=rf_params,
                                               cv=5, scoring=rmse_scorer)

gridsearch_random_foreset_model.fit(x.iloc[x_train_idx], y.iloc[y_train_idx])


print(f'train result : {gridsearch_random_foreset_model.score(x.iloc[x_train_idx], y.iloc[y_train_idx]):5f}')
print(f'valid result : {gridsearch_random_foreset_model.score(x.iloc[x_valid_idx], y.iloc[y_valid_idx]):5f}')
print(f'total result : {gridsearch_random_foreset_model.score(x, y):5f}')

gridsearch_random_foreset_model.score(x.iloc[x_train_idx], y.iloc[y_train_idx])
gridsearch_random_foreset_model.score(x.iloc[x_valid_idx], y.iloc[y_valid_idx])
gridsearch_random_foreset_model.score(x, y)

gridsearch_random_foreset_model.best_estimator_


#######################
# Test
#######################
test_input = test.copy()
my_process_define(test_input)
test_input = test_input.drop(columns=['ID', 'gift'])

submission['수요량'] = gridsearch_random_foreset_model.best_estimator_.predict(test_input)
submission.to_csv(base_path + "soo_submission.csv", index=False)
