# -*- coding:utf-8 -*-
"""
train.api
==========

This module provide api interface
"""
from .data import get_station_list
from .data import get_train_dict
from .data import get_train_details
from .models import Train
import time


def to_name(code, station_list=None):
    """
    将英文缩写转换为中文车站名
    :param code: 英文缩写
    :param station_list: 预先提供站点列表
    :return: 中文站名
    """
    if station_list is None:
        station_list = get_station_list()
    for station in station_list:
        if station.code_name == code:
            return station.name
    return None


def to_code(name, station_list=None):
    """
    将中文车站名转换为英文缩写
    :param name: 中文站名
    :param station_list: 预先提供站点列表
    :return: 英文缩写
    """
    if station_list is None:
        station_list = get_station_list()
    for station in station_list:
        if station.name == name:
            return station.code_name
    return None


def get_train(train_code, date=None):
    """
    获取某日车次的详细信息[必须还未从始发站发车]
    :param train_code: 车次
    :param date: 日期[默认为当天]
    :return: Train
    """
    if date is None:
        date = time.strftime("%Y-%m-%d")

    train_dict = get_train_dict()
    train_info = train_dict[train_code]
    station_list = get_station_list()
    train_details = get_train_details(train_info.train_no,
                                      to_code(train_info.start, station_list),
                                      to_code(train_info.end, station_list),
                                      date)

    return Train(train_info, train_details)
