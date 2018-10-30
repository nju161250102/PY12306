# -*- coding:utf-8 -*-
"""
train.tools
==========

This module provides tools used in this package
"""
from .models import *
import pandas as pd


def to_name(code, station_list: list):
    """将电报码转换为中文车站名

    Args:
        :param code: 英文缩写
        :param station_list: 预先提供站点列表

    Returns:
        :return: 中文站名
    """
    for station in station_list:
        if station.tele_code == code:
            return station.name
    return None


def to_code(name, station_list: list):
    """将中文车站名转换为电报码

    Args:
        :param name: 中文站名
        :param station_list: 预先提供站点列表

    Returns:
        :return: 电报码
    """
    for station in station_list:
        if station.name == name:
            return station.tele_code
    return None


def get_column_value(station_name: str, column_name: str, data: pd.DataFrame):
    """ 获取数据框中某站点记录的字段值

    SELECT column_name FROM data WHERE 站名=station_name

    Args:
        :param station_name: 站点名
        :param column_name: 列名
        :param data: 数据

    Returns:
        :return: 返回值，不存在则返回None
    """
    s = data.loc[data['站名'] == station_name][column_name].values
    return s[0] if s.size > 0 else None


def get_rs_relation_model(rid: int, sid: int, mileage: int, no: int) -> RailStationRelation:
    """封装数据库模型RailStationRelation

    Args:
        :param rid: rail_id
        :param sid: station_id
        :param mileage: 里程
        :param no: 序号

    Returns:
        :return: 返回封装后的RailStationRelation
    """
    return RailStationRelation(rid=rid, sid=sid, mileage=mileage, no=no)


def get_rail_model(rail_id: str, json_dict: dict) -> Rail:
    """封装数据库模型Rail

    Args:
        :param rail_id:
        :param json_dict: 抓取的json数据

    Returns:
        :return: 返回封装后的Rail
    """
    return Rail(id=rail_id,
                name=json_dict["name"],
                lineNum=json_dict["lineNum"],
                speed=json_dict["designSpeed"],
                elec=json_dict["elec"],
                service=json_dict["railService"],
                type=json_dict["railType"])


def get_station_model(json_dict: dict) -> Station:
    """封装数据库模型Station

    Args:
        :param json_dict: 抓取的json数据

    Returns:
        :return: 返回封装后的Station
    """
    return Station(id=json_dict["id"],
                   name=json_dict["localName"],
                   teleCode=json_dict["teleCode"],
                   pinyinCode=json_dict["pinyinCode"],
                   location=json_dict["location"],
                   bureau=json_dict["bureau"]["name"] if json_dict["bureau"] is not None else None,
                   service=json_dict["serviceClass"],
                   x=json_dict["x"],
                   y=json_dict["y"])
