# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 14:21
import os
from fake_useragent import UserAgent

url = "http://m.xsqishu.com/newbook/"
#配置为False  全量下载
DOWNLOADNUM=3 # 每夜索引获取的故事数目
STORYNUM=5  #下载的故事个数 storynum=Fasle 全量下载
INDEXNUM=2 #小说索引的下载地址
stroypath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "story\story.txt")
urlpath = os.path.join(os.path.dirname(os.getcwd()), "story\\url.txt")
dbpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config\\db_config.ini")
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_PATH, 'log')

def user_Agent():
    ua = UserAgent()
    useragent = ua.chrome
    headers = {"User-Agent": useragent}
    return headers
