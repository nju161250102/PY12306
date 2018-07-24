# -*- coding:utf-8 -*-
import requests


class StationInfo:

    def __init__(self, name, pinyin, code_name, abb_pinyin):
        self.name = name
        self.pinyin = pinyin
        self.code_name = code_name
        self.abb_pinyin = abb_pinyin

    def __repr__(self):
        return '{%s, %s, %s, %s}' % (self.name, self.code_name, self.pinyin, self.abb_pinyin)


class StationConvert:
    # the correspondence between stations' name and code
    _station_list = []

    def __init__(self):
        req = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js")
        index = req.content.index("'")
        namelist = req.content[index:-1].split("|")
        for i in range(0, len(namelist)-5, 5):
            s = StationInfo(namelist[i+1], namelist[i+3], namelist[i+2], namelist[i+4])
            self._station_list.append(s)

    def __str__(self):
        return str(self._station_list).decode('string_escape')

    # check name(can be Chinese or English code), if exist return true
    def check_name(self, name):
        for station in self._station_list:
            if station.name == name or station.code_name == name:
                return True
        return False

    # convert Chinese name to code
    def to_name(self, code):
        for station in self._station_list:
            if station.code_name == code:
                return station.name
        return None

    # convert code to Chinese name
    def to_code(self, name):
        for station in self._station_list:
            if station.name == name:
                return station.code_name
        return None
