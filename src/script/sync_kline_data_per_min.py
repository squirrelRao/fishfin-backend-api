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

now_min = datetime.datetime.now().minute

def sync_data(symbols,period):
    for symbol in _list["data"]:
        print("sync kline data:" + symbol + " "+period) 
        data = huobi.get_kline(symbol = symbol,period = period)
        print(data)
        net_client.post(url,data)


_list = net_client.get(host +"/v1/symbol/watch/list")
if _list["rc"] == 0:
    symbols = _list["data"]
    #sync hour data
    sync_data(symbols,"1min")
    
    #sync 5min data
    if now_min%5 == 0:
        sync_data(symbols,"5min")

    #sync 15min data
    if now_min%15 == 0:
        sync_data(symbols,"15min")

    #sync 30min data
    if now_min%30 == 0:
        sync_data(symbols,"30min")
