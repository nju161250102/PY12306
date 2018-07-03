# -*- coding:utf-8 -*-
import requests
import station


class StationConvert:
    # the correspondence between stations' name and code
    _station_list = []

    def __init__(self):
        req = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js")
        index = req.content.index("'")
        namelist = req.content[index:-1].split("|")
        line = []
        for s in namelist:
            line.append(s)
            if len(line) == 5:
                self._station_list.append(line)
                line = []

    def get_info(self):
        return self._station_list
