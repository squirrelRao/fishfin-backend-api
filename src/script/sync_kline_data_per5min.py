# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.net_client import net_client
from model.huobi import HuobiTrade
from model.user import User
import datetime

#sync kline data

huobi = HuobiTrade()
host = "http://lab.lakewater.cn"
url = host +"/v1/trade/data/push"
period = "1min"

_list = net_client.get(host +"/v1/symbol/watch/list")
if _list["rc"] == 0:
    #sync 1min data
    for symbol in _list["data"]:
        print("sync kline data:" + symbol + " "+period)
        data = huobi.get_kline(symbol = symbol,period = period)
        print(data)
        net_client.post(url,data)

