# -*- coding:utf-8 -*-
"""
train.models
================

This module contains basic objects used in package
"""


class StationInfo:
    """
    车站信息
    :param name: 中文名
    :param pinyin: 拼音
    :param code_name: 英文代号
    :param add_pinyin: 拼音首字母缩写
    """

    def __init__(self, name, pinyin, code_name, abb_pinyin):
        self.name = name
        self.pinyin = pinyin
        self.code_name = code_name
        self.abb_pinyin = abb_pinyin

    def __repr__(self):
        return '{%s, %s, %s, %s}' % (self.name, self.code_name, self.pinyin, self.abb_pinyin)


class TrainInfo:
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
