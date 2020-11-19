# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 15:34
import re
from config import  setting
from util.log import logger as logging
from mysql.mysqlConnect import MyPoolDB
from mysql.mysqllist import storyIndexCountSql,insertindexsql
from config.setting import createtime,updatetime
from util.resquestOverwrite import requestOverwrite
def getStoryIndexUrl():  #获取小说的索引地址
    mysql=MyPoolDB()
    downLoadIndexCount=int(mysql.execute(storyIndexCountSql)[0][0])
    url=setting.url
    res=requestOverwrite(url)
    max_index_reg = re.compile(r'<a id="pt_mulu">\d+/(\d+)</a>')
    max_index = max_index_reg.findall(res.text)[0]
    page_urls=[]
    if downLoadIndexCount==0:
        logging.info("---索引下载中，请等待---")

        for i in range(1, int(max_index)+1):
            if i == 1:
                page_url = "http://m.xsqishu.com/newbook/index.html"
            else:
                page_url = "http://m.xsqishu.com/newbook/index_" + str(i) + ".html"
            page_urls.append((i,page_url,createtime,updatetime))
            msg="下载第"+str(i)+"页"
            logging.info(msg)
    elif downLoadIndexCount==int(max_index):
        logging.info("----当前已是最新索引,无需更新----")
    else:
        logging.info("----索引更新中,请等待----")
        for i in range(downLoadIndexCount+1, int(max_index)+1):
            page_url = "http://m.xsqishu.com/newbook/index_" + str(i) + ".html"
            # sql=inertStoryPageIndexSql(i,page_url)
            # mysql.insert(sql)
            msg="更新第"+str(i)+"页"
            logging.info(msg)
            page_urls.append((i,page_url,createtime,updatetime))
    mysql.insertmany(insertindexsql,page_urls)
getStoryIndexUrl()