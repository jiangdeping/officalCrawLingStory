# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 14:19

####MySQLdb连接方法1：
import MySQLdb
from util.log import logger as logging
from config import setting
import configparser as cparser
# def connect():
#     filpath = setting.dbpath
#     cf = cparser.ConfigParser()
#     cf.read(filpath)
#     conn= MySQLdb.Connect(
#         host=cf.get("mysqlconf", "host"),
#         db=cf.get("mysqlconf", "db_name"),
#         user=cf.get("mysqlconf", "user"),
#         password=cf.get("mysqlconf", "password"),
#         port=int(cf.get("mysqlconf", "port")),
#         charset="utf8",
#         use_unicode=True,
#     )
#     return conn
#
# ####MySQLdb连接方法2：
# import MySQLdb
# from config import setting
# DBConfigInformation=setting.MySqlConfig
# def connect():
#     conn=MySQLdb.Connect(**DBConfigInformation)
#     return conn
#
#
# ###MYSQL封装：
# import MySQLdb
# from config import setting
# DBConfigInformation=setting.MySqlConfig
# class MySQL(object):
#     def __init__(self):
#         self.conn=None
#         self.cur=None
#     def connect(self):
#         self.conn=MySQLdb.Connect(**DBConfigInformation)
#         self.cur=self.conn.cursor()
#         return self.conn
#     def close(self):
#         self.conn.commit()
#         self.cur.close()
#         self.conn.close()

###PooledDB连接
import MySQLdb
from dbutils.pooled_db import PooledDB
DBConfigInformation=setting.MySqlConfig
class MyPoolDB(object):
    pool=None
    def __init__(self):
        self.conn=self.Connect()
        self.cursor=self.conn.cursor()
    def Connect(self):
        if MyPoolDB.pool==None:
            pool=PooledDB(MySQLdb,**DBConfigInformation)
        return pool.connection()
    def execute(self, sql, args=None):
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()
    def insertmany(self,sql,args=None):
        try:
            self.cursor.executemany(sql,args)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()  # 事务回滚
            print('SQL执行有误,原因:', e)
    def insert(self,sql,args=None):
        try:
            self.cursor.execute(sql,args)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()  # 事务回滚
            print('SQL执行有误,原因:', e)
    def __del__(self):
        self.cursor.close()
        self.conn.close()
