# -*- coding:utf-8 -*-
"""
train.models
================

This module contains basic objects used in package
"""
from peewee import *
db = SqliteDatabase('train.db')  # 配置数据库连接


class BaseModel(Model):
    """
    peewee 模型使用的基类
    """
    class Meta:
        database = db


class RailStationRelation(BaseModel):
    """
    线路-站点 关系模型
    """
    rid = IntegerField()
    sid = IntegerField()
    mileage = IntegerField()
    no = IntegerField()

    class Meta:
        table_name = "rs_relation"


class Rail(BaseModel):
    """
    线路模型
    """
    id = IntegerField(primary_key=True)
    name = TextField()
    lineNum = TextField()
    speed = TextField()
    elec = TextField()
    service = TextField()
    type = TextField()


class Station(BaseModel):
    """
    车站模型
    """
    id = IntegerField(primary_key=True)
    name = TextField()
    teleCode = TextField()
    pinyinCode = TextField()
    location = TextField()
    bureau = TextField()
    service = TextField()
    x = DoubleField()
    y = DoubleField()
