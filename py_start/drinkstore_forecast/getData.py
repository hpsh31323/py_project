#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Your module description
"""

import datetime
import requests


# 取臺北年間每日高低溫資料
def get_avg_temp_tpi(q):
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/C-B0024-002?Authorization=CWB-F56CCF8D-5917-4BC0-81A0" \
          "-BA01A58465E6&downloadType=WEB&format=JSON"
    dict_max = {}
    dict_min = {}
    dict_avg = {}

    with requests.Session() as s:
        download = s.get(url)
        data1 = download.json().get("cwbopendata").get('dataset').get('location')
        for d in data1:
            if d['stationId'] == '466920':
                data2 = d['weatherElement'][1]['time']
                for d2 in data2:
                    time1 = d2['obsTime']
                    max_temp = d2['weatherElement'][0]['elementValue']['value']
                    min_temp = d2['weatherElement'][1]['elementValue']['value']
                    avg_temp = d2['weatherElement'][2]['elementValue']['value']
                    dict_max.update({time1: max_temp})
                    dict_min.update({time1: min_temp})
                    dict_avg.update({time1: avg_temp})
                break

    return q.put({"dict_max": dict_max, "dict_min": dict_min, "dict_avg": dict_avg})


# 取商店銷售資料
def get_order_amount(q, days=365):
    endDate = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    startDate = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    url = "http://drinkstore-dev3.ap-southeast-1.elasticbeanstalk.com/api/orders/amount/" + startDate + "/" + endDate

    download = requests.get(url)
    data1 = download.json()
    dict1 = {}
    for d in data1:
        day = d['date'][0:10]
        amount = d['sum']
        if day in dict1.keys():
            sum1 = dict1[day] + amount
            dict1.update({day: sum1})
        else:
            dict1.update({day: amount})

    return q.put(dict1)


# 取未來一週氣溫預測
def get_future_temp(q):
    url1 = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-005?Authorization=CWB-F56CCF8D-5917-4BC0-81A0-BA01A58465E6&downloadType=WEB&format=JSON"
    with requests.Session() as s:
        download = s.get(url1)
        data1 = download.json().get('cwbopendata').get("dataset").get("location")
        for d in data1:
            if d['locationName'] == "臺北市":
                data1 = d.get("weatherElement")
                break
        list_maxT = []
        list_minT = []
        dict_maxT = {}
        dict_minT = {}
        for d in data1:
            if d['elementName'] == "MaxT":
                list_maxT = d['time']
            elif d['elementName'] == "MinT":
                list_minT = d['time']

        for maxT in list_maxT:
            date1 = maxT["startTime"][0:10]
            time1 = maxT["startTime"][11:13]
            if time1 == "18": continue
            temp1 = maxT["parameter"]["parameterName"]
            dict_maxT.update({date1: eval(temp1)})

        for minT in list_minT:
            date1 = minT["startTime"][0:10]
            time1 = minT["startTime"][11:13]
            if time1 == "18": continue
            temp1 = minT["parameter"]["parameterName"]
            dict_minT.update({date1: eval(temp1)})

        dict_future_temp = {}
        dict_future_temp.update({"max": dict_maxT})
        dict_future_temp.update({"min": dict_minT})
        return q.put(dict_future_temp)
