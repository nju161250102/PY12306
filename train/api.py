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
import pandas as pd


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


def import_rails():
    """
    从 http://cnrail.geogv.org 抓取铁路线路数据
    """
    station_list = get_station_list()
    data = pd.read_excel("station_data.xlsx", encoding="utf-8")
    rail_ids = ['48317']  # 线路的id
    rail_ids_pos = 0  # 位置指示，隔开已抓取和未抓取的线路
    all_station_ids = []  # 站点id列表，避免重复抓取站点基本信息

    while rail_ids_pos != len(rail_ids):
        rail, station_infos = get_rails(rail_ids[rail_ids_pos])
        rail.save(force_insert=True)
        order_num = 1
        for station_info in station_infos:
            # station_info: [id, 里程数]
            station_id = station_info[0]
            station, rs_relation = get_station(station_id, rail.id, station_info[1], order_num, station_list, data)
            # 排除非客运站点
            if station is None:
                continue
            print("---", station_id, rail.id, station_info[1])
            rs_relation.save()
            order_num += 1
            if station_id not in all_station_ids:
                station.save(force_insert=True)
                print(station.name)
            lines = get_station_link(station_id)
            if len(lines) > 1:
                all_station_ids.append(station_id)
            else:
                continue
            for line_id in lines:
                # 将不在线路列表里的线路加入列表
                if line_id not in rail_ids:
                    print("new line:", line_id)
                    rail_ids.append(line_id)
        rail_ids_pos += 1
