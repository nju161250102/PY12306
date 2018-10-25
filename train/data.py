# -*- coding:utf-8 -*
"""
train.data
===========

This module can get data from Internet or local file
"""
from .models import *
from .tools import get_rs_relation_model, get_rail_model, get_station_model, get_column_value
import requests
import re
import json


def get_station_list(path=None) -> list:
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
        req = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js").text

    index = req.index("'")
    namelist = req[index:-1].split("|")
    for i in range(0, len(namelist) - 5, 5):
        s = StationInfo(namelist[i + 1], namelist[i + 3], namelist[i + 2], namelist[i + 4])
        station_list.append(s)
    return station_list


def get_train_dict(path=None) -> dict:
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


def get_train_details(train_no: str, start_code: str, end_code: str, date: str) -> list:
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


def get_rails(rail_id: str) -> tuple:
    """
    从网站获取铁路线路数据
    :param rail_id: 网站使用的铁路id
    :return: Rail, list<int> 数据获取失败返回None, None
    """
    r = requests.get("http://cnrail.geogv.org/api/v1/rail/%s?locale=zhcn" % rail_id)
    result = json.loads(r.text, encoding="utf-8")
    if result["success"]:
        rail = get_rail_model(rail_id, result["data"])
        # 部分线路上没有车站信息
        if result["data"]["diagram"] is None:
            return rail, []
        # 缺少里程时用None代替
        station_infos = [[station[3][0][1], station[1] if station[1] != "" else None]
                         for station in result["data"]["diagram"]["records"] if station[2] in ["MST", "SST"]]
        return rail, station_infos
    return None, None


def get_station(station_id: int, rail_id: int, mileage: int, no: int, station_list, data) -> tuple:
    """
    从网站获取站点以及站点-线路关联
    :param station_id: 站点id
    :param rail_id: 线路id
    :param mileage: 线路里程
    :param no: 站点序号
    :param station_list: 车站信息列表（来自12306网站）
    :param data: 车站位置数据（来自xlsx文件）
    :return: tuple(Station, RailStationRelation)
    """
    r = requests.get(
        "http://cnrail.geogv.org/api/v1/station/%s?locale=zhcn&query-override=&requestGeom=true" % station_id)
    result = json.loads(r.text, encoding="utf-8")
    if result["serviceClass"] != "":
        if result["teleCode"] is None:
            for s in station_list:
                if s.name == result["localName"]:
                    result["teleCode"] = s.tele_code.upper()
        if result["pinyinCode"] is None:
            for s in station_list:
                if s.name == result["localName"]:
                    result["pinyinCode"] = s.pinyin_code.upper()
        result["x"] = get_column_value(result["localName"], "WGS84_Lng", data)
        result["y"] = get_column_value(result["localName"], "WGS84_Lat", data)
    station = get_station_model(result) if result["serviceClass"] != "" else None
    rs_relation = get_rs_relation_model(rail_id, station_id, mileage, no)
    return station, rs_relation


def get_station_link(station_id: int) -> list:
    """
    从网站获取站点经过的线路
    :param station_id: 站点id
    :return: 线路id列表
    """
    r = requests.get("http://cnrail.geogv.org/api/v1/station-link/%s?locale=zhcn&query-override=" % station_id)
    result = json.loads(r.text, encoding="utf-8")
    if result["success"]:
        return [line["railId"] for line in result["data"]]
    else:
        return []
