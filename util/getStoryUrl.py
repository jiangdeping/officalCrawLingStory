# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 16:00
import re,requests
from config.setting import createtime,updatetime,user_Agent
from util.log import logger as logging
from mysql.mysqllist import isExistStorySql,inrertStoryUrlSql
from mysql.mysqlConnect import MyPoolDB
from util.resquestOverwrite import requestOverwrite
from util.mysqFunc import getStoryNo
mysql=MyPoolDB()
def getStoryUrl(url):
    stroyurls = {}
    inertStoryUrls=[]
    res=requestOverwrite(url)
    url_reg = re.compile(r'<a href="/txt/(\d+).html">')
    allstorynos = url_reg.findall(res.text)
    storynos=[]#当前需要下载的小说ID
    for i in allstorynos:
        storynos.append(i)
    alreadyStoryNos=getStoryNo()#已下载的小说ID
    downloadStoryNos=list(set(storynos).difference(set(alreadyStoryNos))) #下载的小说ID
    if downloadStoryNos:
        for i in downloadStoryNos:
            story_url = "http://m.xsqishu.com/txt/" + i + ".html"
            stroyurls[i]=story_url
        for num,compileurl in stroyurls.items():
            res=requestOverwrite(compileurl)
            res.encoding = "gbk"
            reg = re.compile(r'<a href="/book/(.+).html" class="bdbtn greenBtn">')
            url = reg.findall(res.text)
            story_title_reg = re.compile(r'<h1 class="title">(.+)</h1>')
            title = story_title_reg.findall(res.text)[0]
            download_url = "http://m.xsqishu.com/book/" + url[0] + ".html"
            inertStoryUrls.append((num,title,download_url,createtime))
            msg="- - - -:新增小说<"+title+">入库"
            logging.info(msg)
        mysql.insertmany(inrertStoryUrlSql,inertStoryUrls)
    else:
        msg="- - - -:目前无新增小说"
        logging.warning(msg)
# url="http://m.xsqishu.com/newbook/index.html"
# getStoryUrl(url)