# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 23:14:18 2023

@author: Soo.Y
"""


import xgboost as xgb
from sklearn.metrics import make_scorer
from konlpy.tag import Okt
from sklearn.preprocessing import MinMaxScaler
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


def my_rmse(true, pred, sample_weight=None):
    return np.sqrt(np.mean((true - pred)**2))


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


# gift_set = ["새우", '특선', '곶감', '샤인머스켓', '스팸',
#             '송이버섯', '자연', '실속', '표고버섯', '행복',
#             '찬스', '유기농', '견과', '최고',
#             '최고급', '프리미엄', '명품', '스페셜', '고급',
#             '올리브유', '견과류', '홍삼', '종합', '재래']

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
    # train['target'] = np.log(train.target)


#####################
# data split
#####################
my_process_define(train)

x = train.drop(columns=['ID', 'gift', 'target'])
y = pd.DataFrame(train['target'])

# index
idx = list(range(train.shape[0]))
x_train_idx, x_valid_idx, y_train_idx, y_valid_idx = train_test_split(idx, idx, test_size=0.3, random_state=9234)

#####################
# Scale
#####################

x_scaler = MinMaxScaler(feature_range=(0, 1))
x_scaler.fit(x)
x = pd.DataFrame(x_scaler.transform(x), columns=x.columns)

y_scaler = MinMaxScaler(feature_range=(0, 1))
y_scaler.fit(y)
y = pd.DataFrame(y_scaler.transform(y), columns=y.columns)


#####################
# random forest & Grid serach
#####################
evaluation_metric = mean_squared_error


def modelfit(pip_xgb, grid_param_xgb, x, y):
    gs_xgb = (GridSearchCV(estimator=pip_xgb,
                           param_grid=grid_param_xgb,
                           cv=5,
                           # scoring='neg_mean_squared_error',
                           # scoring='neg_root_mean_squared_error',
                           n_jobs=-1,
                           verbose=10))

    gs_xgb = gs_xgb.fit(x, y)
    print('Train Done.')

    # Predict training set:
    y_pred = gs_xgb.predict(x)

    # Print model report:
    print("\nModel Report")
    print("\nCV 결과 : ", gs_xgb.cv_results_)
    print("\n베스트 정답률 : ", gs_xgb.best_score_)
    print("\n베스트 파라미터 : ", gs_xgb.best_params_)


# pip_xgb1 = Pipeline([('scl', StandardScaler()),
#     ('reg', MultiOutputRegressor(xgb.XGBRegressor()))])

grid_param_xgb1 = {
    'n_estimators': [500, 1000],
    'max_depth': [3, 5, 10],
    'subsample': [1, 5, 10],
    # 'reg__estimator__gamma' : [1, 0.1, 0.01, 0.001, 0.0001, 0],
    # 'reg__estimator__learning_rate' : [0.01, 0.03, 0.05, 0.07, 0.08],
    # 'reg__estimator__subsample' : [0.4, 0.6, 0.8],
    # 'reg__estimator__colsample_bytree' : [0.2, 0.6, 0.8]
}

modelfit(xgb.XGBRegressor(), grid_param_xgb1, x.iloc[x_train_idx], y.iloc[y_train_idx])


########################################################
# 단일 파라미터 실행
########################################################
xgb_model = xgb.XGBRFRegressor(n_estimators=500, max_depth=3,
                               eval_metric='rmse', random_state=9234)


xgb_model.fit(x.iloc[x_train_idx], y.iloc[y_train_idx])

#######################
# 성능 점검
#######################

predict_result = xgb_model.predict(x.iloc[x_train_idx])
my_rmse(predict_result, y.iloc[y_train_idx].squeeze())

predict_result = xgb_model.predict(x.iloc[x_valid_idx])
my_rmse(np.exp(predict_result), y.iloc[y_valid_idx])

#######################
# Test
#######################
test_input = test.copy()
my_process_define(test_input)
test_input = test_input.drop(columns=['ID', 'gift'])

test_scaled = pd.DataFrame(x_scaler.transform(test_input), columns=test_input.columns)

submission['수요량'] = y_scaler.inverse_transform(pd.DataFrame(xgb_model.predict(test_input)))

submission.to_csv(base_path + "soo_submission.csv", index=False)
