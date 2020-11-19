# -*- coding: utf-8 -*-
#Author:jiang
#2020/11/19 17:24
from util import downLoadStoryContentTxt,getStoryContentUrl,getStoryIndexUrl,getStoryUrl,mysqFunc
#第一步：检查索引更新
getStoryIndexUrl.getStoryIndexUrl()
#第二步：根据索引获取小说ID及标题
downloadurls=mysqFunc.getStoryIndex()
for downloadurl in downloadurls:
    getStoryUrl.getStoryUrl(downloadurl)
#第三步：获取小说内容的下载地址

storycontneturls=mysqFunc.getStoryUrl()
for storycontneturl in storycontneturls:
    getStoryContentUrl.getStoryContentUrl(storycontneturl)

#第四步：下载小说
storynos=mysqFunc.getdownloadStoryNo()

for storyno in storynos:
    downLoadStoryContentTxt.downLoadStoryContent(storyno)