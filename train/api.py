# -*- coding:utf-8 -*-
"""
train.api
==========

This module provides api interface
"""
from .data import *
from .tools import *
from .models import Train
from .database import *
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
    all_station_ids = []
    data_service = SqlliteDataImpl(db_path)

    while rail_ids_pos != len(rail_ids):
        rail, station_infos = get_rails(rail_ids[-1])
        data_service.save_rail(rail)
        for station_info in station_infos:
            station_id = station_info[0]
            station, rs_relation = get_station(station_id, rail.id, station_info[1])
            if station is None:
                continue
            data_service.save_relation(rs_relation)
            if station_id not in all_station_ids:
                data_service.save_station(station)
                print station.name
                all_station_ids.append(station_id)
            lines = get_station_link(station_id)
            for line_id in lines:
                if line_id not in rail_ids:
                    print line_id
                    rail_ids.append(line_id)
        rail_ids_pos += 1
