# -*- coding:utf-8 -*-
"""
train.tools
==========

This module provides tools used in this package
"""
from .models import *


def to_name(code, station_list: list):
    """
    将英文缩写转换为中文车站名
    :param code: 英文缩写
    :param station_list: 预先提供站点列表
    :return: 中文站名
    """
    for station in station_list:
        if station.code_name == code:
            return station.name
    return None


def to_code(name, station_list: list):
    """
    将中文车站名转换为英文缩写
    :param name: 中文站名
    :param station_list: 预先提供站点列表
    :return: 英文缩写
    """
    for station in station_list:
        if station.name == name:
            return station.code_name
    return None


def get_rs_relation_model(rid: int, sid: int, mileage: int) -> RailStationRelation:
    return RailStationRelation(rid=rid, sid=sid, mileage=mileage)


def get_rail_model(rail_id: int, json_dict: dict) -> Rail:
    return Rail(id=rail_id,
                name=json_dict["name"],
                lineNum=json_dict["lineNum"],
                speed=json_dict["designSpeed"],
                elec=json_dict["elec"],
                service=json_dict["railService"],
                type=json_dict["railType"])


def get_station_model(json_dict: dict) -> Station:
    return Station(id=json_dict["id"],
                   name=json_dict["localName"],
                   teleCode=json_dict["teleCode"],
                   pinyinCode=json_dict["pinyinCode"],
                   location=json_dict["location"],
                   bureau=json_dict["bureau"]["name"],
                   service=json_dict["serviceClass"], )
