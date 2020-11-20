# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 15:18
from  datetime import datetime
storyIndexSql="SELECT storyindexUrl FROM STORY_INDEX"
storyUrlSql="SELECT storytitle,storyurl FROM STORY_url"
storyNoSql="select DISTINCT storyno from story_content_url"
stroryNoSql="SELECT storyno,storyurl FROM story_url"
storyIndexCountSql="SELECT count(*) FROM STORY_INDEX"
insertindexsql="INSERT INTO story_index(storyindexID,storyindexUrl,createtime,updatetime) VALUES (%s,%s,%s,%s)"
inrertStoryUrlSql="INSERT INTO story_url(storyno,storytitle,storyurl,createtime) VALUES (%s,%s,%s,%s)"
insertStoryContentUrlSql="INSERT INTO story_content_url(storyno,chapter_num,chapter_num_url,createtime) VALUES (%s,%s,%s,%s)"
isExistStorySql="SELECT * FROM story_url where STORYNO=%s"
DownLoadStoryContentUrlssql="SELECT chapter_num_url FROM story_content_url where STORYNO=%s ORDER BY chapter_num"
alreadyDownLoadStoryContentUrlssql="SELECT url FROM story where STORY_NO=%s"
inserStoryTxtsql="INSERT INTO story(chapter,url,text,chapter_num,story_no,state,createtime,updatetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
def getStoryIndexUrlSql(num):
    sql="SELECT storyindexurl FROM STORY_INDEX limit %s"%num
    return sql
def inertStoryPageIndexSql(storyindexID, storyindexUrl):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO story_index(storyindexID,storyindexUrl,createtime,updatetime) VALUES ('{}','{}','{}','{}')".format(storyindexID, storyindexUrl, createtime, updatetime)
    return sql
# def isExistStorySql(storyno):
#     sql="SELECT * FROM story_url where STORYNO=%s" % storyno
#     return sql
# def InertStoryUrlSql(storyNo, storyTitle, storyUrl):
#     createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     sql = "INSERT INTO story_url(storyno,storytitle,storyurl,createtime) VALUES ('{}','{}','{}','{}')".format(storyNo, storyTitle,storyUrl,createtime)
#     return sql
def insetStoryContentUrl(storyno,new_chapter_num,url):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO story_content_url(storyno,chapter_num,chapter_num_url,createtime) VALUES ('{}','{}','{}','{}')".format(
            storyno, new_chapter_num, url,createtime)
    return sql
def insertStory(storyno,chapter_num,url,text):
    createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updatetime= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_chapter_num = str(storyno) + chapter_num.zfill(5)
    chapter = "第" + str(chapter_num) + "章"
    sql = "INSERT INTO story(chapter,url,text,chapter_num,story_no,state,createtime,updatetime) VALUES ('{}','{}','{}','{}',{},{},'{}','{}')".format(
        chapter, url, text, new_chapter_num, storyno, 0,createtime,updatetime)
    return sql