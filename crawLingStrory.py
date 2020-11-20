# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/19 17:24
from util import downLoadStoryContentTxt,getStoryContentUrl,getStoryIndexUrl,getStoryUrl,mysqFunc
from util.log import logger as logging
from util.getStoryUrl import getStoryUrl
import threading
#第一步：检查索引更新
# logging.info("- - - -更新小说索引- - - -")
# getStoryIndexUrl.getStoryIndexUrl()
# #第二步：根据索引获取小说ID及标题
# logging.info("- - - -更新小说下载地址- - - -")
# downloadurls=mysqFunc.queryStoryIndex()
# downloadurlthreads=[]
# for downloadurl in downloadurls:
#     getStoryUrl(downloadurl)
# threads=[]
# for i in downloadurls:
#     t=threading.Thread(target=getStoryUrl,args=(i,))
#     t.start()
#     threads.append(t)
# for i in threads:
#     i.join()

#第三步：获取小说内容的下载地址
storycontneturls=mysqFunc.queryStoryUrl()
for storycontneturl in storycontneturls:
    msg="检查小说- - -<"+storycontneturl[0]+">- - -是否更新"
    logging.info(msg)
    getStoryContentUrl.getStoryContentUrl(storycontneturl[1])
#第四步：下载小说
storynos=mysqFunc.querydownloadStoryNo()
print(storynos)
logging.info("- - - -小说下载- - - -")
for storyno in storynos:
    downLoadStoryContentTxt.downLoadStoryContent(storyno)
