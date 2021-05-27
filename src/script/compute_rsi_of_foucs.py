#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import os
sys.path.append("..")
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"libs"))
from common.net_client import net_client
from common.mongo_client import mongo_client
from common.common_util import CommonUtil
from model.user import User
from libs.rsi_strategy import RsiStrategy
from model.kline import Kline
import datetime
from datetime import date


#compute rsi strategy of focus
def compute_focus_rsi():
    strategy = RsiStrategy()
    db = mongo_client.fishfin
    users = db.user.find({"status":1})
    kline = Kline()
    common_util = CommonUtil()
    periods = ["1min","5min","30min","60min"]
    for user in users:
        user_id = str(user["_id"])
        for period in periods:
            watch = list(db.user_quantization.find({"status":1,"user_id":user_id}))
            for item in watch:
                symbol = item["symbol"]
                line_name = "market."+symbol+".kline."+period
                klines = db.kline.find({"name":line_name}).sort("ktime",-1).limit(1)
                kline = None
                for k in klines:
                    kline = k
                if kline is None:
                    continue
                ktime = kline["ktime"]
                print(user_id+":"+period+":"+symbol+":"+common_util.timestamp_to_string(kline["ktime"]))
                base_currency = "usdt"
                quote_currency = symbol.replace("usdt","") 
                strategy.run(user_id,quote_currency,base_currency,period,ktime,5000,"rsi")


compute_focus_rsi()
