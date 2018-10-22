# coding=utf-8
import sqlite3


class DataService(object):
    """
    数据层接口，不同数据库可分别实现
    """

    def save_rail(self, rail):
        pass

    def save_station(self, station):
        pass

    def save_relation(self, rs_relation):
        pass


class SqlliteDataImpl(DataService):

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    @staticmethod
    def insert_sql(obj, table_name):
        """
        返回插入语句及参数
        :param obj: 待插入对象
        :param table_name: 表名
        :return: (str, tuple) sql语句, 参数
        """
        attrs = [x for x in dir(obj) if x[0] != '_']
        sql = "INSERT INTO " + table_name + "(" + ",".join(attrs) + ")" + " VALUES (" + ",".join(
            ['?'] * len(attrs)) + ");"
        params = tuple((getattr(obj, x) for x in attrs))
        return sql, params

    def save_rail(self, rail):
        c = self.conn.cursor()
        sql, params = self.insert_sql(rail, "rail")
        c.execute(sql, params)
        self.conn.commit()

    def save_station(self, station):
        c = self.conn.cursor()
        sql, params = self.insert_sql(station, "station")
        c.execute(sql, params)
        self.conn.commit()

    def save_relation(self, rs_relation):
        c = self.conn.cursor()
        sql, params = self.insert_sql(rs_relation, "rs_relation")
        c.execute(sql, params)
        self.conn.commit()

