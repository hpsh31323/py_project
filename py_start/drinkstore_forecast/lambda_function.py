#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
from py_start.drinkstore_forecast.data_analysis import forecasting_Order


def forecasting():

    s3 = boto3.client('s3')
    object = s3.get_object(Bucket='drinkstore-static', Key='json/avg_temp_tpi.json')
    serializedObject = object['Body'].read()
    dict_year_temp = json.loads(serializedObject)

    s3 = boto3.client('s3')
    object = s3.get_object(Bucket='drinkstore-static', Key='json/order_amount.json')
    serializedObject = object['Body'].read()
    dict_order_amount = json.loads(serializedObject)

    s3 = boto3.client('s3')
    object = s3.get_object(Bucket='drinkstore-static', Key='json/future_temp.json')
    serializedObject = object['Body'].read()
    dict_future_temp = json.loads(serializedObject)

    dict_max = dict_year_temp["dict_max"]
    dict_min = dict_year_temp["dict_min"]
    dict_avg = dict_year_temp["dict_avg"]

    key_set = sorted(dict_order_amount.keys()) if len(dict_order_amount.keys()) < len(dict_max.keys()) else sorted(
        dict_max.keys())
    list_keys = []
    list_avg_temps = []
    list_max_temps = []
    list_min_temps = []
    list_orders = []

    for key in key_set:
        if not (key in (dict_max if len(dict_order_amount.keys()) < len(dict_max.keys()) else dict_order_amount)):
            continue
        list_keys.append(key)
        list_max_temps.append(eval(dict_max[key]))
        list_min_temps.append(eval(dict_min[key]))
        list_avg_temps.append(eval(dict_avg[key]))
        list_orders.append(dict_order_amount[key])

    forecast = forecasting_Order(list_max_temps, list_min_temps, list_orders, dict_future_temp)

    s3 = boto3.client('s3')
    serializedMyData = json.dumps(forecast)
    s3.put_object(Body=serializedMyData, Bucket='drinkstore-static', Key="json/" + "forecast.json")


    # return {"task1": task1, "task2": task2, "total_time": total_time}
