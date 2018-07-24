# -*- coding:utf-8 -*-
from .data import get_station_list


def to_name(code):
    for station in get_station_list():
        if station.code_name == code:
            return station.name
    return None


def to_code(name):
    for station in get_station_list():
        if station.name == name:
            return station.code_name
    return None
