# -*- coding:utf-8 -*-
from .train.models import *
from .train.data import get_station_list, get_rails, get_station, get_station_link


def import_rails():
    """使用网络数据与本地文件初始化数据库

    从 http://cnrail.geogv.org 抓取铁路线路数据并结合12306网站数据和本地数据，写入数据库
    warming: 每一个站点的数据不能保证非Null
    """
    # 从12306获取车站数据列表，用于补充电报码与拼音码
    station_list = get_station_list()
    # 线路的id列表
    rail_ids = ['48317']
    # 位置游标，游标前是已抓取线路，之后是未抓取线路
    rail_ids_pos = 0
    # 站点id列表，避免重复抓取站点基本信息
    all_station_ids = []

    while rail_ids_pos != len(rail_ids):
        rail, station_infos = get_rails(rail_ids[rail_ids_pos])
        print("Current Line: %s, %s" % (rail.id, rail.name))
        rail.save(force_insert=True)
        order_num = 1  # 记录当前站点序号
        for station_info in station_infos:
            # station_info格式: [id, 里程数]
            station_id = station_info[0]
            station = Station.get_or_none(id=station_id)
            # 如果站点已经存在
            if station is not None:
                # 从数据库中获取经过站点的线路
                lines = [relation.rid for relation
                         in RailStationRelation.select().where(RailStationRelation.sid == station_id)]
            else:
                # 从网站抓取站点数据
                station, rs_relation = get_station(station_id, rail.id, station_info[1], order_num, station_list)
                # 排除非客运站点
                if station is None:
                    continue
                rs_relation.save()
                order_num += 1
                # 如果站点未被保存，则写入数据库
                if station_id not in all_station_ids:
                    station.save(force_insert=True)
                    print(station.name)
                lines = get_station_link(station_id)

            # lines为经过当前车站的线路列表
            if len(lines) > 1:
                # 说明不止一条线路经过，之后可能还会抓到，需要保存id以免重复抓取
                all_station_ids.append(station_id)
            else:
                continue

            for line_id in lines:
                # 将不在线路列表里的线路加入列表
                if line_id not in rail_ids:
                    print("New Line:", line_id)
                    rail_ids.append(line_id)
        rail_ids_pos += 1


if __name__ == "__main__":
    import_rails()
