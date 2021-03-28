# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.net_client import net_client
from mondel.huobi import HuobiTrade

#sync basic info

huobi = HuobiTrade()

print("sync kline data")
data = huobi.get_kline()
net_client.post(url,data)

