# -*- coding:utf-8 -*-
"""
train.api
==========

This module provides api interface
"""
from .data import *
from .tools import *
from .models import Train
import time


def get_train_list():
    return get_train_dict().keys()


def get_train(train_code, station_from=None, station_to=None, date=None):
    """
    获取某日车次的详细信息[必须还未从出发站发车]
    :param train_code: 车次
    :param station_from: 出发站[默认为始发站]
    :param station_to: 到达站[默认为终到站]
    :param date: 日期[默认为当天]
    :return: Train
    """
    if date is None:
        date = time.strftime("%Y-%m-%d")

    train_dict = get_train_dict()
    train_info = train_dict[train_code]
    if station_from is None:
        station_from = train_info.start
    if station_to is None:
        station_to = train_info.end

    station_list = get_station_list()
    train_details = get_train_details(train_info.train_no,
                                      to_code(station_from, station_list),
                                      to_code(station_to, station_list),
                                      date)

    return Train(train_info, train_details)


def import_rails(db_path):
    rail_ids = [3360]
    rail_ids_pos = 0
    station_ids = []

    while rail_ids_pos != len(rail_ids):
        r = requests.get("http://cnrail.geogv.org/api/v1/rail/%s?locale=zhcn" % rail_ids[-1])
        rail_result = json.loads(r.text, encoding="utf-8")
        for station in rail_result["data"]["diagram"]["records"]:
            station_type = station[2]
            if station_type in ["MST", "SST"]:
                station_id = station[3][0][1]
                r = requests.get("http://cnrail.geogv.org/api/v1/station/%s?locale=zhcn&query-override=&requestGeom=true" % station_id)
                station_result = json.loads(r.text, encoding="utf-8")
                if station_result["serviceClass"] != "" and station_id not in station_ids:
                    print(station[3][0][2].encode("utf-8"))
                    station_ids.append(station_id)
                    # save station
                r = requests.get("http://cnrail.geogv.org/api/v1/station-link/%s?locale=zhcn&query-override=" % num)
                relation_result = json.loads(r.text, encoding="utf-8")
                for line in relation_result["data"]:
                    if line["railId"] not in rail_ids:
                        print "新线路："
                        print line["railName"].encode("utf-8")
                        rail_ids.append(line["railId"])
                        # save relation
        rail_ids_pos += 1
