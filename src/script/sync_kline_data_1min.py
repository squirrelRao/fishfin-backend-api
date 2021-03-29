# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.net_client import net_client
from model.huobi import HuobiTrade
from model.user import User

#sync basic info

huobi = HuobiTrade()

_list = net_client.get("http://lab.lakewater.cn/v1/symbol/watch/list")
if _list["rc"] != 0:
    return
period = "1min"

for symbol in _list["data"]:
    print("sync kline data:" + symbol + " "+period)
    data = huobi.get_kline(symbol = symbol,period = period)
    print(data)
    net_client.post(url,data)

