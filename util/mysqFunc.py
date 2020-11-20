# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/19 15:30
from mysql.mysqllist import DownLoadStoryContentUrlssql,stroryNoSql,alreadyDownLoadStoryContentUrlssql,storyIndexSql,storyUrlSql,storyNoSql
from mysql.mysqlConnect import MyPoolDB
from config.setting import INDEXNUM,DOWNLOADNUM,STORYCONTENTNUM
mysql=MyPoolDB()
def queryStoryNo():
    storynos=[]
    urls=mysql.execute(stroryNoSql)
    for i in urls:
        storynos.append(i[0])
    return storynos
def queryStoryUrls(storyno):
    downloadurls=[]
    urls=mysql.execute(DownLoadStoryContentUrlssql,(storyno,))
    num=STORYCONTENTNUM
    if STORYCONTENTNUM==False:
        num=len(urls)
    for i in urls[0:num]:
        downloadurls.append(i[0])
    return downloadurls
def queryAlreadyStoryUrls(storyno):
    downloadurls=[]
    urls=mysql.execute(alreadyDownLoadStoryContentUrlssql,(storyno,))
    for i in urls:
        downloadurls.append(i[0])
    return downloadurls
def queryStoryIndex():
    storyIndexs=[]
    Indexs=mysql.execute(storyIndexSql)
    for index in Indexs[0:INDEXNUM]:
        storyIndexs.append(index[0])
    return storyIndexs
def queryStoryUrl():
    storyUrls=[]
    urls=mysql.execute(storyUrlSql)
    for url in urls[0:DOWNLOADNUM]:
        storyUrls.append((url[0],url[1]))
    return storyUrls
def querydownloadStoryNo():
    storynos=[]
    nos=mysql.execute(storyNoSql)
    for no in nos:
        storynos.append(no[0])
    return storynos
