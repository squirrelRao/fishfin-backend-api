# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.net_client import net_client
from model.huobi import HuobiTrade
from model.user import User

#sync basic info

huobi = HuobiTrade()
host = "http://lab.lakewater.cn"
_list = net_client.get(host +"/v1/symbol/watch/list")
period = "1min"
if _list["rc"] == 0:
    for symbol in _list["data"]:
        print("sync kline data:" + symbol + " "+period)
        data = huobi.get_kline(symbol = symbol,period = period)
        print(data)
        url = host +"/v1/trade/data/push"
        net_client.post(url,data)

