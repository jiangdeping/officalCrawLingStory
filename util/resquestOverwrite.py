# -*- coding: utf-8 -*-
# Author:jiang
# 2020/11/9 17:23
import requests,time
from config.setting import user_Agent
from util.log import logger as logging
def requestOverwrite(url):
    requests.adapters.DEFAULT_RETRIES = 5
    res= requests.session()
    res.encoding = "gbk"
    res.keep_alive = False
    flag = True
    while flag:
        try:
            user_agent = user_Agent()
            res = res.get(url, headers=user_agent)
            if res.status_code ==200:
                flag = False
            # else:
            #     msg="GET页面<"+url+">失败，重新请求- - -"
            #     time.sleep(2)
            #     logging.info(msg)
        except Exception as e:
            logging.info("- - 连接失败,正在重连- - ")
            logging.error(e)
    return res
