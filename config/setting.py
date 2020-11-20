# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 14:32

import os
from fake_useragent import UserAgent
from datetime import datetime
createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
updatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

url = "http://m.xsqishu.com/newbook/"
#配置为False  全量下载
DOWNLOADNUM=100 #下载的故事个数
STORYCONTENTNUM=10 #每个故事的下载章节数 storynum=Fasle 全量下载
INDEXNUM=50 #小说索引数
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

MySqlConfig={
    "host":"47.96.162.123",
    "port":3306,
    'user':"cqdev",
    'password':"cqdev",
    "db":"test",
    "charset":"utf8",# 数据库连接编码
}