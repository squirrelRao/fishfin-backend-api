# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.net_client import net_client
from model.huobi import HuobiTrade
from model.user import User
import datetime
from datetime import date

#sync kline data

huobi = HuobiTrade()
host = "http://lab.lakewater.cn"
url = host +"/v1/trade/data/push"

now_hour = datetime.datetime.now().hour
now_day =  datetime.datetime.now().day
now_month =  datetime.datetime.now().month
isoweekday =  datetime.datetime.now().isoweekday()


def sync_data(symbols,period):
    for symbol in _list["data"]:
        print("sync kline data:" + symbol + " "+period) 
        data = huobi.get_kline(symbol = symbol,period = period)
        print(data)
        net_client.post(url,data)


_list = net_client.get(host +"/v1/symbol/watch/list")
if _list["rc"] == 0:
    symbols = _list["data"]
    #sync day data
    sync_data(symbols,"1day")
    
    #sync 1week
    if isoweekday == 1:
        sync_data(symbols,"1week")

    #sync 1month
    if now_day == 1:
        sync_data(symbols,"1mon")

    #sync 1year
    if now_month == 1 and now_day == 1:
        sync_data(symbols,"1year")
