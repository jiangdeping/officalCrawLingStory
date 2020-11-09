# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 17:08
import re
import requests, re,time
# from mysql.storyMysql import insertStory
from util.log import logger as logging
from config.setting import user_Agent,createtime,updatetime
from util.resquestOverwrite import requestOverwrite
from mysql.mysqlConnect import MyPoolDB
from mysql.mysqllist import DownLoadStoryContentUrlssql,inserStoryTxtsql
mysql=MyPoolDB()
def getStoryUrls(storyno):

    downloadurls=[]
    urls=mysql.execute(DownLoadStoryContentUrlssql,(storyno,))
    for i in urls:
        downloadurls.append(i[0])
    return downloadurls
def downLoadStory(urls):
    insertstorytxts=[]
    for url in urls:
        res=requestOverwrite(url)
        res.encoding = "gbk"  #指定res.encoding
        reg=re.compile(r'http://m.xsqishu.com(.+)/(\d+)/(\d)+.html')
        identical=reg.findall(url)[0]  #同一小说相同的部分
        # print(identical)## /book/45/83253
        title_identical=identical[0]+"/"+identical[1]+".html"
        storyno=identical[1]
        chapternum=identical[2]
        chapter="第"+chapternum+"章"
        new_chapter_num=storyno+str(chapternum.zfill(5))
        # storytitle_reg=re.compile(r'</span><a href="%s">(.+)</a></div>'%(title_identical)) #获取小说url
        # storytitle=storytitle_reg.findall(res.text)[0]
        text_reg = re.compile(r'<div class="articlecon font-large"><p>(.+)<br/><br/></p></div>')
        # strorytitle=
        result = text_reg.findall(res.text)
        new_result = result[0].replace("<br/>", "")
        new_result.lstrip("")
        new_result = re.sub(' +', '\n  ', new_result)
        insertstorytxts.append((chapter,url,new_result,new_chapter_num,storyno,0,createtime,updatetime))
    # inserStoryTxtsql="INSERT INTO story(chapter,url,text,chapter_num,story_no,state,createtime,updatetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    mysql.insertmany(inserStoryTxtsql,insertstorytxts)

urls=getStoryUrls("83026")

print(urls)
downLoadStory(urls)