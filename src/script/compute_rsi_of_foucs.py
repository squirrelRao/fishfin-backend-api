# -*- coding: utf-8 -*-
import sys
import time
import os
sys.path.append("..")
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"libs"))
from common.net_client import net_client
from common.mongo_client import mongo_client
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
    for user in users:
        focus = kline.get_kline_strategy(user_id,period,"rsi")
        symbol = focus["symbol"]
        period = focus["period"]
        ktime = focus["ktime"]
        user_id = focus["strategy"]["user_id"]
        base_currency = "usdt"
        quote_currency = symbol.replace("usdt","") 
        strategy.run(user_id,quote_currency,base_currency,period,ktime,5000,"rsi")


#compute_focus_rsi()
