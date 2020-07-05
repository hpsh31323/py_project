#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Your module description
"""
import threading
from queue import Queue

import numpy as np
import pandas as pd
# 引入 train_test_split 分割方法
from sklearn.linear_model import ElasticNet, Lasso
from sklearn.model_selection import train_test_split
# 引入 KNeighbors 模型
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

from py_start.drinkstore_forecast.exportImg import exportImg
from py_start.drinkstore_forecast.getData import get_avg_temp_tpi, get_order_amount, get_future_temp


def forecasting_Order(list_max_temps, list_min_temps, list_orders, dict_future_temp):
    dict_re = {}
    np_max_temps = []
    np_min_temps = []
    np_Order = []
    start_max_Temp = list_max_temps[0]
    start_min_Temp = list_min_temps[0]
    start_Order = list_orders[0]
    for i in range(1, len(list_max_temps)):

        stop_max_Temp = list_max_temps[i]
        stop_min_Temp = list_min_temps[i]
        stop_Order = list_orders[i]
        new_max = np.linspace(start=start_max_Temp, stop=stop_max_Temp, num=100, endpoint=False)
        new_min = np.linspace(start=start_min_Temp, stop=stop_min_Temp, num=100, endpoint=False)
        new_Order = np.linspace(start=start_Order, stop=stop_Order, num=100, endpoint=False)
        start_max_Temp = stop_max_Temp
        start_min_Temp = stop_min_Temp
        start_Order = stop_Order
        if i == 1:
            np_max_temps = new_max
            np_min_temps = new_min
            np_Order = new_Order
        else:
            np_max_temps = np.concatenate((np_max_temps, new_max))
            np_min_temps = np.concatenate((np_min_temps, new_min))
            np_Order = np.concatenate((np_Order, new_Order))

    list_maxT = []
    list_minT = []
    maxT = dict_future_temp["max"]
    minT = dict_future_temp["min"]
    key_set = sorted(maxT.keys())
    for key in key_set:
        list_maxT.append(maxT[key])
        list_minT.append(minT[key])

    dict_re.update({"list_maxT": list_maxT, "list_minT": list_minT, "date_f": key_set})
    # 組成training data
    np_max_temps = np_max_temps.reshape(len(np_max_temps), 1)
    np_min_temps = np_min_temps.reshape(len(np_min_temps), 1)
    df_temps_p = pd.DataFrame(np.hstack([np_max_temps, np_min_temps]))

    list_maxT = np.array(list_maxT)
    list_minT = np.array(list_minT)
    list_maxT = list_maxT.reshape(len(list_maxT), 1)
    list_minT = list_minT.reshape(len(list_minT), 1)
    df_temps_f = pd.DataFrame(np.hstack([list_maxT, list_minT]))
    df_Order = pd.DataFrame(np_Order)
    # 將資料切分為 training data 和 testing data
    # test_size 為切分 training data 和 testing data 的比例
    temps_train, temps_test, order_train, order_test = train_test_split(df_temps_p, df_Order, test_size=0.3)

    elastic_net = train_ElasticNet(temps_train, order_train)
    lasso = train_Lasso(temps_train, order_train)

    # 準確率
    elastic_net_score = elastic_net.score(temps_test, order_test.values.ravel().astype('int'))
    lasso_score = lasso.score(temps_test, order_test.values.ravel().astype('int'))
    # 預測值
    elastic_net_f = elastic_net.predict(df_temps_f)
    lasso_f = lasso.predict(df_temps_f)
    dict_re.update({"elastic_net_score": elastic_net_score, "lasso_score": lasso_score, "elastic_net_f": elastic_net_f,
                    "lasso_f": lasso_f})
    return dict_re


def train_ElasticNet(temps_train, order_train):
    # 初始化 ElasticNet 實例
    elastic_net = ElasticNet()
    # 使用 fit 來建置模型，其參數接收 training data matrix, testing data array，所以進行 order_train.values.ravel() Data Frame 轉換

    elastic_net.fit(temps_train, order_train.values.ravel().astype('int'))
    ElasticNet(alpha=1.0, l1_ratio=0.5, fit_intercept=True, normalize=False, precompute=False, max_iter=1000,
               copy_X=True, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic')
    return elastic_net


def train_Lasso(temps_train, order_train):
    # 初始化 Lasso 實例
    lasso = Lasso()

    # 使用 fit 來建置模型
    lasso.fit(temps_train, order_train.values.ravel().astype('int'))

    Lasso(alpha=1.0, fit_intercept=True, normalize=False, precompute=False, copy_X=True, max_iter=1000,
          tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic')

    return lasso
