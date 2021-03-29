# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.net_client import net_client
from model.huobi import HuobiTrade

#sync basic info

host = "http://lab.lakewater.cn"
url = host + "/v1/trade/data/push"
huobi = HuobiTrade()

print("sync market status")
market_status = huobi.get_market_status()
print(market_status)
net_client.post(url,market_status)

print("sync symbols")
symbols = huobi.get_symbols()
print("post symbols:"+url)
net_client.post(url,symbols)

print("sync currencys")
currencys = huobi.get_currencys()
net_client.post(url,currencys)

print("sync market status")
market_status = huobi.get_market_status()
print(market_status)
net_client.post(url,market_status)

