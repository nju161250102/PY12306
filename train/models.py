# -*- coding:utf-8 -*-
"""
train.models
================

This module contains basic objects used in package
"""


class StationInfo(object):
    """
    车站信息
    :param name: 中文名
    :param pinyin: 拼音
    :param code_name: 英文代号
    :param abb_pinyin: 拼音首字母缩写
    """

    def __init__(self, name, pinyin, code_name, abb_pinyin):
        self.name = name
        self.pinyin = pinyin
        self.code_name = code_name
        self.abb_pinyin = abb_pinyin

    def __repr__(self):
        return '{%s, %s, %s, %s}' % (self.name, self.code_name, self.pinyin, self.abb_pinyin)


class TrainInfo(object):
    """
    车次信息，不包含详细的列车时刻表
    :param code: 车次
    :param start: 始发站[中文]
    :param end  终到站[中文]
    :param train_no: 车次编号
    """

    def __init__(self, code, start, end, train_no):
        self.code = code
        self.start = start
        self.end = end
        self.train_no = train_no

    def __repr__(self):
        return '{%s, %s, %s, %s}' % (self.code, self.start, self.end, self.train_no)


class TrainDetail(object):
    """
    某一站的停靠信息
    :param station_name: 车站中文名
    :param arrive_time: 到达时间[None表示为始发站]
    :param start_time: 开车时间[None表示为终到站]
    """

    def __init__(self, station_name, arrive_time, start_time):
        self.station_name = station_name
        self.arrive_time = arrive_time
        self.start_time = start_time

    def __repr__(self):
        return ('{%s, %s, %s}' % (self.station_name, self.arrive_time, self.start_time)).encode('utf-8')


class Train(object):
    """
    一趟完整的车次信息
    code: 车次
    start: 始发站[中文]
    end  终到站[中文]
    station_details: 停靠站点信息
    """

    def __init__(self, train_info, station_details):
        self.code = train_info.code
        self.start = train_info.start
        self.end = train_info.end
        self.station_details = station_details

    def __repr__(self):
        return ("%s -- %s -- %s\n%s" % (self.start, self.code, self.end, self.station_details)).encode('utf-8')


class Rail(object):

    def __init__(self, rail_id, json_dict):
        self.id = rail_id
        self.name = json_dict["name"]
        self.lineNum = json_dict["lineNum"]
        self.speed = json_dict["designSpeed"]
        self.elec = json_dict["elec"]
        self.service = json_dict["railService"]
        self.type = json_dict["railType"]


class Station(object):

    def __init__(self, name, json_dict):
        self.id = json_dict["id"]
        self.name = name
        self.teleCode = json_dict["teleCode"]
        self.pinyinCode = json_dict["pinyinCode"]
        self.location = json_dict["location"]
        self.bureau = json_dict["bureau"]["name"]
        self.service = json_dict["serviceClass"]


class RailStationRelation(object):

    def __init__(self, rid, sid, mileage):
        self.rid = rid
        self.sid = sid
        self.mileage = mileage
