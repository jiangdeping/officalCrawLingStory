# -*- coding: utf-8 -*-
# Author:jiang
# 2020/11/5 20:44
import threading
import time
import queue
import requests
# from mysql.SQL_LIST import insertStory
# from mysql.db_PooledDB import pool,Connect
from  config.setting import user_Agent
from util.log import logger as logging
import re
from threading import Thread
download_urls=[]
storyListIndexQueue = queue.Queue()
sotryUrlQueue = queue.Queue()
sotryUrlQueue2 = queue.Queue()
storyContentUrlQueue = queue.Queue()

def get_index_url():  # 获取小说的索引地址
    url = "http://m.xsqishu.com/newbook/"
    requests.adapters.DEFAULT_RETRIES = 5
    urls = []
    s = requests.session()
    s.keep_alive = False
    flag = True
    while flag:
        try:
            user_agent = user_Agent()
            res = requests.get(url, headers=user_agent)
            flag = False
            # res.request.headers  获取设置的user_agent
        except Exception as e:
            logging.error(e)
            continue
    max_index_reg = re.compile(r'<a id="pt_mulu">\d+/(\d+)</a>')
    max_index = max_index_reg.findall(res.text)[0]
    for i in range(1, int(max_index) + 1):
        if i == 1:
            page_url = "http://m.xsqishu.com/newbook/index.html"
        else:
            page_url = "http://m.xsqishu.com/newbook/index_" + str(i) + ".html"
        urls.append(page_url)
    for i in urls[0:2]:
        storyListIndexQueue.put(i)
def get_story_url1():  # 获取每部小说的下载地址
    while True:
        url = storyListIndexQueue.get()
        print("get_story_url", url)
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        flag = True
        while flag:
            try:
                user_agent = user_Agent()
                res = requests.get(url, headers=user_agent)
                flag = False
                # res.request.headers  获取设置的user_agent
            except Exception as e:
                logging.error(e)
                continue
        url_reg = re.compile(r'<a href="/txt/(\d+).html">')
        allUrl = url_reg.findall(res.text)
        for i in allUrl[0:5]:
            story_url = "http://m.xsqishu.com/txt/" + i + ".html"
            sotryUrlQueue.put(story_url)
        storyListIndexQueue.task_done()
def get_story_url2():
    while True:
        url=sotryUrlQueue.get()
        print("get_story_url2",url)
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        flag = True
        while flag:
            try:
                user_agent = user_Agent()
                res = requests.get(url, headers=user_agent)
                res.encoding = "gbk"
                flag = False
                # res.request.headers  获取设置的user_agent
            except Exception as e:
                logging.error(e)
                continue
        reg = re.compile(r'<a href="/book/(.+).html" class="bdbtn greenBtn">')
        url = reg.findall(res.text)
        download_url = "http://m.xsqishu.com/book/" + url[0] + ".html"
        sotryUrlQueue2.put(download_url)
        sotryUrlQueue.task_done()
def getStoryContentTxt():
    while True:
        url=sotryUrlQueue2.get(sotryUrlQueue2)
        storyContentNum=5
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        flag = True
        # logging.info(url)
        while flag:
            try:
                user_agent = user_Agent()
                res = requests.get(url, headers=user_agent)
                flag = False
                # res.request.headers  获取设置的user_agent
            except Exception as e:
                logging.error(e)
                continue
        reg=re.compile(r'http://m.xsqishu.com(.+).html')
        identical=reg.findall(url)[0]  #同一小说相同的部分
        storyurlreg = re.compile(r'<a href=(%s/\d+).html><li>'%(identical)) #获取小说url
        storyUrls = storyurlreg.findall(res.text)
        newstoryUrls=[]
        if storyContentNum==False:
            storyContentNum=len(storyUrls)
        for i in storyUrls[0:storyContentNum-1]:
            url="http://m.xsqishu.com"+i+".html"
            newstoryUrls.append(url)
        for i in newstoryUrls[0:5]:
            storyContentUrlQueue.put(i)
        sotryUrlQueue2.task_done()
def downLoadStory():
    s1=[]
    while True:
        requests.adapters.DEFAULT_RETRIES = 5
        url=storyContentUrlQueue.get()
        print("storyContentUrlQueue",url)
        s = requests.session()
        s.keep_alive = False
        flag = True
        while flag:
            try:
                user_agent = user_Agent()
                res = s.get(url, headers=user_agent)
                flag = False
                # print(res.headers["User-Agent"])
                # log.info(res.headers["User-Agent"])
            except Exception as e:
                logging.info("- - 连接失败,正在重连- ")
                logging.error(e)
                continue
        reg=re.compile(r'http://m.xsqishu.com(.+)/(\d+)/(\d)+.html')
        identical=reg.findall(url)[0]  #同一小说相同的部分
        # print(identical)## /book/45/83253
        title_identical=identical[0]+"/"+identical[1]+".html"
        storyno=identical[1]
        chapternum=identical[2]
        # new_chapter_num=storyno+str(chapternum.zfill(5))
        storytitle_reg=re.compile(r'</span><a href="%s">(.+)</a></div>'%(title_identical)) #获取小说url
        storytitle=storytitle_reg.findall(res.text)[0]
        text_reg = re.compile(r'<div class="articlecon font-large"><p>(.+)<br/><br/></p></div>')
        # strorytitle=
        result = text_reg.findall(res.text)
        new_result = result[0].replace("<br/>", "")
        new_result.lstrip("")
        new_result = re.sub(' +', '\n  ', new_result)
        # sql=insertStory(storyno,chapternum,url,new_result)
        # mysql=Connect(pool)
        # mysql.insert(sql)
        s1.append((storyno,chapternum,url,new_result))
        storyContentUrlQueue.task_done()
    return s

def run():
    list=[]
    get_index_url()
    for i in range(10):
        t=threading.Thread(target=get_story_url1)
        list.append(t)
    for i in range(10):
        t= threading.Thread(target=get_story_url2)
        list.append(t)
    for i in range(50):
        t = threading.Thread(target=getStoryContentTxt)
        list.append(t)
    for i in range(50):
        t = threading.Thread(target=downLoadStory)
        list.append(t)
    for i in list:
        i.setDaemon(True)
        i.start()
    for q in[storyListIndexQueue,sotryUrlQueue ,sotryUrlQueue2,storyContentUrlQueue]:
        q.join()
run()