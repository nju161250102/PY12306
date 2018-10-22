# -*- coding:utf-8 -*
"""
train.data
===========

This module can get data from Internet or local file
"""
from .models import *
import requests
import re
import json


def get_station_list(path=None):
    """
    获得车站站点列表[从本地已下载的js文件或者从网络获取]
    URL: https://kyfw.12306.cn/otn/resources/js/framework/station_name.js
    :param path: 本地文件地址。默认为None表示从网络获取
    :return: list<Station>站点列表
    """
    station_list = []
    if path is not None:
        with open(path, 'r') as f:
            req = f.read()
    else:
        req = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js").content

    index = req.index("'")
    namelist = req[index:-1].split("|")
    for i in range(0, len(namelist) - 5, 5):
        s = StationInfo(namelist[i + 1], namelist[i + 3], namelist[i + 2], namelist[i + 4])
        station_list.append(s)
    return station_list


def get_train_dict(path=None):
    """
    从本地文件或者网络获取车次信息
    URL: https://kyfw.12306.cn/otn/resources/js/query/train_list.js
    :param path: 本地文件地址。默认为None表示从网络获取
    :return: dict{code: TrainInfo} 键-车次 值-TrainInfo对象
    """
    train_dict = {}
    if path is not None:
        with open(path, 'r') as f:
            req = f.read()
    else:
        req = requests.get("https://kyfw.12306.cn/otn/resources/js/query/train_list.js").content

    for m in re.finditer('"station_train_code":"(\w+)\((.+?)-(.+?)\)","train_no":"(.+?)"', req):
        t = TrainInfo(m.group(1), m.group(2), m.group(3), m.group(4))
        if m.group(1) not in train_dict:
            train_dict[t.code] = t
    return train_dict


def get_train_details(train_no, start_code, end_code, date):
    """
    从网络查询车次信息
    URL: https://kyfw.12306.cn/otn/czxx/queryByTrainNo
    :param train_no: 车次
    :param start_code: 始发站英文缩写
    :param end_code: 终到站英文缩写
    :param date: 发车日期
    :return: list<TrainDetail>
    """
    r = requests.get("https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=" + train_no
                     + "&from_station_telecode=" + start_code
                     + "&to_station_telecode=" + end_code
                     + "&depart_date=" + date)
    res_data = json.loads(r.text)

    station_details = []
    for item in res_data["data"]["data"]:
        arrive_time = None if item["arrive_time"] == "----" else item["arrive_time"]
        start_time = None if item["start_time"] == "----" else item["start_time"]
        if item["isEnabled"]:
            station_details.append(TrainDetail(item["station_name"], arrive_time, start_time))

    return station_details


def get_rails(rail_id):
    """
    从网站获取铁路线路数据
    :param rail_id: 网站使用的铁路id
    :return: Rail, list<int> 数据获取失败返回None, None
    """
    r = requests.get("http://cnrail.geogv.org/api/v1/rail/%s?locale=zhcn" % rail_id)
    result = json.loads(r.text, encoding="utf-8")
    if result["success"]:
        rail = Rail(rail_id, result["data"])
        station_infos = \
            [[station[3][0][1], station[1]] for station in result["data"]["diagram"]["records"] if station[2] in ["MST", "SST"]]
        return rail, station_infos
    return None, None


def get_station(station_id, rail_id, mileage):
    """
    从网站获取站点以及站点-线路关联
    :param station_id: 站点id
    :param rail_id: 线路id
    :param mileage: 线路里程
    :return:
    """
    r = requests.get(
        "http://cnrail.geogv.org/api/v1/station/%s?locale=zhcn&query-override=&requestGeom=true" % station_id)
    result = json.loads(r.text, encoding="utf-8")
    station = Station(result) if result["serviceClass"] != "" else None
    rs_relation = RailStationRelation(rail_id, station_id, mileage)
    return station, rs_relation


def get_station_link(station_id):
    """
    从网站获取站点经过的线路
    :param station_id: 站点id
    :return: 线路id列表
    """
    r = requests.get("http://cnrail.geogv.org/api/v1/station-link/%s?locale=zhcn&query-override=" % station_id)
    result = json.loads(r.text, encoding="utf-8")
    return [line["railId"] for line in result["data"]]
