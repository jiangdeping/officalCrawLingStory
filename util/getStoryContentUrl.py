# -*- coding: utf-8 -*-
# Author:jiang
# 2020/11/9 16:34
import re
from config.setting import  STORYCONTENTNUM,createtime
from util.log import logger as logging
from mysql.mysqlConnect import MyPoolDB
from util.resquestOverwrite import requestOverwrite
from mysql.mysqllist import insertStoryContentUrlSql
from util.mysqFunc import queryStoryUrls
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
    urls=[]
    for i in storyUrls[0:storyContentNum]:
        url = "http://m.xsqishu.com" + i + ".html"
        urls.append(url)
    alreadyDownLoadurls=queryStoryUrls(storyno)
    downloadUrls=list(set(urls).difference(set(alreadyDownLoadurls)))
    if downloadUrls:
        for url in downloadUrls:
            reg=re.compile(r'%s/(\d+)'%(identical))
            if reg.findall(url):
                chapter_num=reg.findall(url)[0]
                new_chapter_num=storyno+str(chapter_num.zfill(5))
                msg="更新下载链接地址："+url
                logging.info(msg)
                insertStoyrContentUrls.append((storyno,new_chapter_num,url,createtime))
        mysql.insertmany(insertStoryContentUrlSql,insertStoyrContentUrls)
# url = "http://m.xsqishu.com/book/78/83877.html"
# getStoryContentUrl(url)
