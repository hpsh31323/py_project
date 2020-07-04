#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from time import time

from py_start.drinkstore_forecast.data_analysis import task1_get_past_TempAndOrder, task2_forecasting_Order
from py_start.drinkstore_forecast.exportImg import exportImg, exportImgF


def forecasting():
    # TODO implement
    start = time()
    dict1 = task1_get_past_TempAndOrder(180)
    point1 = time()
    task1 = "task1 cost %f sec" % (point1 - start)
    point2 = time()
    dict2 = task2_forecasting_Order(dict1["list_max_temps"], dict1["list_min_temps"], dict1["list_orders"],
                                    dict1["dict_future_temp"])
    point3 = time()
    task2 = "task2 cost %f sec" % (point3 - point2)
    exportImgF(dict2)
    end = time()
    total_time = "total cost %f sec" % (end - start)

    # return {"task1": task1, "task2": task2, "total_time": total_time}
