# -*- coding:utf-8 -*
from .models import StationInfo
from .models import TrainInfo
import requests
import re


def get_station_list():
    station_list = []
    req = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js")
    index = req.content.index("'")
    namelist = req.content[index:-1].split("|")
    for i in range(0, len(namelist) - 5, 5):
        s = StationInfo(namelist[i + 1], namelist[i + 3], namelist[i + 2], namelist[i + 4])
        station_list.append(s)
    return station_list


def get_train_dict(path=None):
    train_dict = {}
    if path is not None:
        with open(path, 'r') as f:
            req = f.read()
    else:
        req = requests.get("https://kyfw.12306.cn/otn/resources/js/query/train_list.js").content

    for m in re.finditer('"station_train_code":"(\w+)\((.+?)-(.+?)\)","train_no":"(.+?)"', req):
        t = TrainInfo(m.group(1), m.group(2), m.group(3), m.group(4))
        if m.group(1) not in train_dict:
            train_dict[t.code] = t
    return train_dict
