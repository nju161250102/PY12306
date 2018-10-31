# -*- coding:utf-8 -*
"""
train.data
===========

This module can get data from Internet
"""
import re
import json
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

from .utils import get_rs_relation_model, get_rail_model, get_station_model, get_ticket_num
from .file import ExcelReader


def get_station_list() -> list:
    """获得车站站点列表

    URL: https://kyfw.12306.cn/otn/resources/js/framework/station_name.js

    Returns:
        :return: list<Station> 站点列表
            Station: dict
            "name": 中文
            "pinyin": 拼音
            "tele_code": 电报码（三位字母）
            "pinyin_code": 拼音缩写（三位字母）
    """
    station_list = []
    req = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js").text

    index = req.index("'")
    namelist = req[index:-1].split("|")
    for i in range(0, len(namelist) - 5, 5):
        s = {"name": namelist[i + 1],
             "pinyin": namelist[i + 3],
             "tele_code": namelist[i + 2],
             "pinyin_code": namelist[i + 4]}
        station_list.append(s)
    return station_list


def get_train_dict() -> dict:
    """获取车次信息

    URL: https://kyfw.12306.cn/otn/resources/js/query/train_list.js

    Returns:
        :return: dict{code: TrainInfo} { 车次: TrainInfo }
            TrainInfo: dict
            "code": 编号
            "start": 始发站（中文）
            "end": 终到站（中文）
            "train_no": 车次
    """
    train_dict = {}
    req = requests.get("https://kyfw.12306.cn/otn/resources/js/query/train_list.js").text

    for m in re.finditer('"station_train_code":"(\w+)\((.+?)-(.+?)\)","train_no":"(.+?)"', req):
        t = {"code": m.group(1),
             "start": m.group(2),
             "end": m.group(3),
             "train_no": m.group(4)}
        if m.group(1) not in train_dict:
            train_dict[t["code"]] = t
    return train_dict


def query_train_info(train_no: str, start_code: str, end_code: str, date: str) -> list:
    """从网络查询车次信息

    URL: https://kyfw.12306.cn/otn/czxx/queryByTrainNo

    Args:
        :param train_no: 车次
        :param start_code: 始发站电报码
        :param end_code: 终到站电报码
        :param date: 发车日期

    Returns:
        :return: list<TrainDetail>
            TrainDetail: dict
            "station_name": 停靠站点名
            "arrive_time": 到达时间[None表示为始发站]
            "start_time": 开车时间[None表示为终到站]
            "isEnabled": 是否在查询区间内
    """
    r = requests.get("https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=" + train_no
                     + "&from_station_telecode=" + start_code
                     + "&to_station_telecode=" + end_code
                     + "&depart_date=" + date)
    res_data = json.loads(r.text)

    station_details = []
    for item in res_data["data"]["data"]:
        arrive_time = None if item["arrive_time"] == "----" else item["arrive_time"]
        start_time = None if item["start_time"] == "----" else item["start_time"]
        station_details.append({"station_name": item["station_name"],
                                "arrive_time": arrive_time,
                                "start_time": start_time,
                                "isEnabled": item["isEnabled"]})

    return station_details


def query_left_tickets(start_code: str, end_code: str, date: str) -> dict:
    """查询余票情况

    URL: https://kyfw.12306.cn/otn/leftTicket/query
    无此席位: None, 有票: -1, 无票: 0

    Args:
        :param start_code: 出发站电报码
        :param end_code: 到达站电报码
        :param date: 日期

    Returns:
        :return: dict{train_no: TicketInfo} 车次; 余票信息
            TicketInfo:
            "train_code": 编号
            "train_no": 车次
            "from_station_code": 始发站电报码
            "to_station_code": 终到站电报码
            "start_time": 发车时间
            "arrive_time": 到达时间
            "total_time": 用时
            "business_seat": 商务座
            "first_class_seat": 一等座
            "second_class_seat": 二等座
            "advanced_sleep": 高级软卧
            "bullet_sleep": 动卧
            "soft_sleep": 软卧
            "hard_sleep": 硬卧
            "soft_seat": 软座
            "hard_seat": 硬座
            "no_seat": 无座

    """
    r = requests.get("https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + date +
                     "&leftTicketDTO.from_station=" + start_code +
                     "&leftTicketDTO.to_station=" + end_code +
                     "&purpose_codes=ADULT")
    res_data = json.loads(r.text)

    result = {}
    for s in res_data["data"]["result"]:
        array = s.split("|")
        result[array[3]] = {"train_code": array[2],
                            "train_no": array[3],
                            "from_station_code": array[4],
                            "to_station_code": array[5],
                            "start_time": array[8],
                            "arrive_time": array[9],
                            "total_time": array[10],
                            "business_seat": get_ticket_num(array[32]),
                            "first_class_seat": get_ticket_num(array[31]),
                            "second_class_seat": get_ticket_num(array[30]),
                            "advanced_sleep": get_ticket_num(array[21]),
                            "bullet_sleep": get_ticket_num(array[33]),
                            "soft_sleep": get_ticket_num(array[23]),
                            "hard_sleep": get_ticket_num(array[28]),
                            "soft_seat": get_ticket_num(array[24]),
                            "hard_seat": get_ticket_num(array[29]),
                            "no_seat": get_ticket_num(array[26])}
    return result


def query_train_by_station(station_name: str, date: str) -> list:
    """按站点查询经停车次信息

    外部网站，数据可能不会及时更新
    URL: http://www.huochepiao.com/huoche/chezhan_ + XXX

    Args:
        :param station_name 车站中文名
        :param date 查询日期

    Returns:
        :return: list(TrainInfo) 车次列表
            TrainInfo
            "train_no": 车次
            "type": 类别
            "start_time": 发车时间
            "end_time": 到达终点站的时间
            "time": 总用时
            "mileage": 里程
    """
    train_list = []
    r = requests.get("http://www.huochepiao.com/huoche/czsearch/?txtChezhan=" + quote(station_name.encode("gbk"))
                     , allow_redirects=False)
    pinyin_code = re.match("/huoche/chezhan_([a-z]*)", r.headers["Location"]).group(1)
    # 查询车站不存在
    if pinyin_code == "beijing" and station_name != "北京":
        return train_list
    r = requests.get("http://www.huochepiao.com/huoche/date_%s_%s" % (pinyin_code, date))
    res = r.content.decode("gbk")
    soup = BeautifulSoup(res, 'html5lib')
    for tr in soup.find_all("tr"):
        if "bgcolor" in tr.attrs.keys():
            if tr["bgcolor"] == "#ffffff" or tr["bgcolor"] == "#eeeeee":
                train_no = re.findall('<a href="/huoche/checi_(.*?)">', str(tr))[0].split("/")[0]
                tds = tr.find_all("td")
                train_list.append({"train_no": train_no,
                                   "type": tds[2].string,
                                   "start_time": tds[3].string,
                                   "end_time": tds[4].string,
                                   "time": tds[5].string,
                                   "mileage": tds[6].string})
    return train_list


def get_rails(rail_id: str) -> tuple:
    """从网站获取铁路线路数据

    Args:
        :param rail_id: 网站使用的铁路id

    Returns:
        :return: Rail, list<int> 数据获取失败返回None, None
    """
    r = requests.get("http://cnrail.geogv.org/api/v1/rail/%s?locale=zhcn" % rail_id)
    result = json.loads(r.text, encoding="utf-8")
    if result["success"]:
        rail = get_rail_model(rail_id, result["data"])
        # 部分线路上没有车站信息
        if result["data"]["diagram"] is None:
            return rail, []
        # 缺少里程时用None代替
        station_infos = [[station[3][0][1], station[1] if station[1] != "" else None]
                         for station in result["data"]["diagram"]["records"] if station[2] in ["MST", "SST"]]
        return rail, station_infos
    return None, None


def get_station(station_id: int, rail_id: int, mileage: int, no: int, station_list: list) -> tuple:
    """从网站获取站点以及站点-线路关联

    Args:
        :param station_id: 站点id
        :param rail_id: 线路id
        :param mileage: 线路里程
        :param no: 站点序号
        :param station_list: 车站信息列表（来自12306网站）

    Returns:
        :return: tuple(Station, RailStationRelation)
    """
    r = requests.get(
        "http://cnrail.geogv.org/api/v1/station/%s?locale=zhcn&query-override=&requestGeom=true" % station_id)
    result = json.loads(r.text, encoding="utf-8")

    excel_reader = ExcelReader("station_data.xlsx")
    if result["serviceClass"] != "":
        if result["teleCode"] is None:
            for s in station_list:
                if s.name == result["localName"]:
                    result["teleCode"] = s.tele_code.upper()
        if result["pinyinCode"] is None:
            for s in station_list:
                if s.name == result["localName"]:
                    result["pinyinCode"] = s.pinyin_code.upper()
        result["x"] = excel_reader.get_column_value(result["localName"], "WGS84_Lng")
        result["y"] = excel_reader.get_column_value(result["localName"], "WGS84_Lat")
    station = get_station_model(result) if result["serviceClass"] != "" else None
    rs_relation = get_rs_relation_model(rail_id, station_id, mileage, no)
    return station, rs_relation


def get_station_link(station_id: int) -> list:
    """
    从网站获取站点经过的线路
    :param station_id: 站点id
    :return: 线路id列表
    """
    r = requests.get("http://cnrail.geogv.org/api/v1/station-link/%s?locale=zhcn&query-override=" % station_id)
    result = json.loads(r.text, encoding="utf-8")
    if result["success"]:
        return [line["railId"] for line in result["data"]]
    else:
        return []
