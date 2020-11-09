# -*- coding: utf-8 -*-
# Author:jiang
# 2020/11/9 16:34
import requests, re
from config.setting import user_Agent, STORYCONTENTNUM,createtime
from util.log import logger as logging
from mysql.mysqlConnect import MyPoolDB
from util.resquestOverwrite import requestOverwrite
from mysql.mysqllist import insertStoryContentUrlSql
mysql=MyPoolDB()
def getStoryContentUrl(url):
    storyContentNum = STORYCONTENTNUM
    res=requestOverwrite(url)
    identical_reg=re.compile(r'http://m.xsqishu.com(.+)/(\d+).html')
    result=identical_reg.findall(url)
    storyno=result[0][1] #小说id
    identical=result[0][0]+"/"+storyno #url相同部分
    storyurlreg = re.compile(r'<a href=(%s/\d+).html><li>' % (identical))  # 获取小说url
    storyUrls = storyurlreg.findall(res.text)
    insertStoyrContentUrls=[]
    if storyContentNum == False:
        storyContentNum = len(storyUrls)
    for i in storyUrls[0:storyContentNum]:
        reg=re.compile(r'%s/(\d+)'%(identical))
        chapter_num=reg.findall(i)[0]
        new_chapter_num=storyno+str(chapter_num.zfill(5))
        url = "http://m.xsqishu.com" + i + ".html"
        insertStoyrContentUrls.append((storyno,new_chapter_num,url,createtime))
    mysql.insertmany(insertStoryContentUrlSql,insertStoyrContentUrls)
url = "http://m.xsqishu.com/book/40/83026.html"
getStoryContentUrl(url)
