# -*- coding:utf-8 -*-
"""
train.api
==========

This module provide api interface
"""
from .data import get_station_list


def to_name(code, station_list=None):
    """
    将英文缩写转换为中文车站名
    :param code: 英文缩写
    :param station_list: 预先提供站点列表
    :return: 中文站名
    """
    if station_list is None:
        station_list = get_station_list()
    for station in station_list():
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
    for station in station_list():
        if station.name == name:
            return station.code_name
    return None
