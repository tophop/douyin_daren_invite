# -*- coding:utf-8 -*-
import datetime

import pymysql
import json


class MysqlUtil:
    def __init__(self):
        self.con = self.connect()

    @classmethod
    def connect(cls):
        con = pymysql.connect(
            host='',
            port=0,
            user='',
            password='',
            db='',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        return con

    @classmethod
    def dict_to_str(cls, kwargs):
        a = ''
        kwargs.pop('create_time')
        for k, v in kwargs.items():
            a += f'{k}="{v}",'
        return a.rstrip(',')

    @classmethod
    def insert_author_data(cls, con, **kwargs):
        try:
            sql = "INSERT INTO `author_info` (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (
            ','.join([i for i in kwargs.keys()]), (str([str(i) for i in kwargs.values()]).strip('[').strip(']')),
            cls.dict_to_str(kwargs)
            )
            cursor = con.cursor()
            cursor.execute(sql)
            # # print(sql)
            con.commit()
            print(f'insert successed {kwargs.get("nickname")}')
        except Exception as e:
            print(e)

    @classmethod
    def insert_invited_author_data(cls, con, **kwargs):
        try:
            sql = "INSERT INTO `invited_author_info` (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (
                ','.join([i for i in kwargs.keys()]), (str([str(i) for i in kwargs.values()]).strip('[').strip(']')),
                cls.dict_to_str(kwargs))
            cursor = con.cursor()
            cursor.execute(sql)
            # # print(sql)
            con.commit()
            print(f'insert successed {kwargs.get("nickname")}')
        except Exception as e:
            print(e)

    @classmethod
    def query_uninvited(self, conn2):
        # self.conn2.ping(reconnect=True)
        sql = "SELECT * FROM `author_info` "
        cursor = conn2.cursor()
        cursor.execute(sql)
        conn2.commit()
        kwargs = cursor.fetchall()

        return json.dumps({'result': kwargs}, cls=DateEncoder)

    @classmethod
    def query_invited(self, conn2):
        # self.conn2.ping(reconnect=True)
        sql = "SELECT * FROM `invited_author_info` "
        cursor = conn2.cursor()
        cursor.execute(sql)
        conn2.commit()
        kwargs = cursor.fetchall()

        return json.dumps({'result': kwargs}, cls=DateEncoder)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    my = MysqlUtil()
