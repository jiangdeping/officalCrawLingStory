# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/9 16:00
import re,requests
from config.setting import createtime,updatetime,user_Agent
from util.log import logger as logging
from mysql.mysqllist import isExistStorySql,inrertStoryUrlSql
from mysql.mysqlConnect import MyPoolDB
from util.resquestOverwrite import requestOverwrite
mysql=MyPoolDB()
def getStoryUrl(url):
    stroyurls = {}
    inertStoryUrls=[]
    res=requestOverwrite(url)
    url_reg = re.compile(r'<a href="/txt/(\d+).html">')
    allUrl = url_reg.findall(res.text)
    for i in allUrl:
        story_url = "http://m.xsqishu.com/txt/" + i + ".html"
        stroyurls[i]=story_url
    for num,compileurl in stroyurls.items():
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        flag = True
        while flag:
            try:
                user_agent = user_Agent()
                res = requests.get(compileurl, headers=user_agent)
                res.encoding = "gbk"
                flag = False
                # res.request.headers  获取设置的user_agent
            except Exception as e:
                logging.error(e)
                continue
        reg = re.compile(r'<a href="/book/(.+).html" class="bdbtn greenBtn">')
        url = reg.findall(res.text)
        story_title_reg = re.compile(r'<h1 class="title">(.+)</h1>')
        title = story_title_reg.findall(res.text)[0]
        download_url = "http://m.xsqishu.com/book/" + url[0] + ".html"
        flag=mysql.execute(isExistStorySql,(num,))
        if flag:
            msg="小说"+title+"已入库，无需重复添加"
            logging.info(msg)
        else:
            inertStoryUrls.append((num,title,download_url,createtime))
            msg="新增小说"+title+"入库"
            logging.info(msg)
    mysql.insertmany(inrertStoryUrlSql,inertStoryUrls)
url="http://m.xsqishu.com/newbook/index.html"
getStoryUrl(url)