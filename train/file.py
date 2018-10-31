# -*- coding:utf-8 -*-
"""
train.file
==========

This module read file data
"""
import pandas as pd


class ExcelReader(object):
    """读取Excel文件，获取其中的值

    Attributes:
        data: pd.DataFrame
    """
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path, encoding="utf-8")

    def get_column_value(self, station_name: str, column_name: str):
        """ 获取数据框中某站点记录的字段值

            SELECT column_name FROM data WHERE 站名=station_name

            Args:
                :param station_name: 站点名
                :param column_name: 列名

            Returns:
                :return: 返回值，不存在则返回None
            """
        result = self.data.loc[self.data['站名'] == station_name][column_name].values
        return result
