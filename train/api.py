# -*- coding:utf-8 -*-
"""
train.api
==========

This module provides api interface
"""
from .data import *
from .utils import *
import time


def get_train_list():
    return get_train_dict().keys()


def query_train_details(train_code, station_from=None, station_to=None, date=None):
    """获取某日车次的详细信息[必须还未从出发站发车]

    Args:
        :param train_code: 车次
        :param station_from: 出发站[默认为始发站]
        :param station_to: 到达站[默认为终到站]
        :param date: 日期[默认为当天]

    Returns:
        :return: TrainDetail: dict 见data.query_train_info
    """
    train_dict = get_train_dict()
    train_info = train_dict[train_code]
    if station_from is None:
        station_from = train_info["start"]
    if station_to is None:
        station_to = train_info["end"]
    if date is None:
        date = time.strftime("%Y-%m-%d")

    station_list = get_station_list()
    train_details = query_train_info(train_info["train_no"], to_code(station_from, station_list)
                                     , to_code(station_to, station_list), date)
    return train_details
