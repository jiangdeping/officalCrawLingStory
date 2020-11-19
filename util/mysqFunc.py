# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/19 15:30
from mysql.mysqllist import DownLoadStoryContentUrlssql,stroryNoSql,alreadyDownLoadStoryContentUrlssql,storyIndexSql,storyUrlSql,storyNoSql
from mysql.mysqlConnect import MyPoolDB
from config.setting import INDEXNUM,DOWNLOADNUM
mysql=MyPoolDB()
def getStoryNo():
    storynos=[]
    urls=mysql.execute(stroryNoSql)
    for i in urls:
        storynos.append(i[0])
    return storynos
def getStoryUrls(storyno):
    downloadurls=[]
    urls=mysql.execute(DownLoadStoryContentUrlssql,(storyno,))
    for i in urls:
        downloadurls.append(i[0])
    return downloadurls
def getAlreadyStoryUrls(storyno):
    downloadurls=[]
    urls=mysql.execute(alreadyDownLoadStoryContentUrlssql,(storyno,))
    for i in urls:
        downloadurls.append(i[0])
    return downloadurls
def getStoryIndex():
    storyIndexs=[]
    Indexs=mysql.execute(storyIndexSql)
    for index in Indexs[0:INDEXNUM]:
        storyIndexs.append(index[0])
    return storyIndexs
def getStoryUrl():
    storyUrls=[]
    urls=mysql.execute(storyUrlSql)
    for url in urls[0:DOWNLOADNUM]:
        storyUrls.append(url[0])
    return storyUrls
def getdownloadStoryNo():
    storynos=[]
    nos=mysql.execute(storyNoSql)
    for no in nos:
        storynos.append(no[0])
    return storynos

