# -*- coding: utf-8 -*-
# Author:jiang
# 2020/11/9 17:23
import requests
from config.setting import user_Agent
from util.log import logger as logging
def requestOverwrite(url):
    requests.adapters.DEFAULT_RETRIES = 5
    res= requests.session()
    res.keep_alive = False
    flag = True
    while flag:
        try:
            user_agent = user_Agent()
            res = res.get(url, headers=user_agent)
            flag = False
            # print(res.headers["User-Agent"])
            # log.info(res.headers["User-Agent"])
        except Exception as e:
            logging.info("- - 连接失败,正在重连- ")
            logging.error(e)
            continue
    return res
