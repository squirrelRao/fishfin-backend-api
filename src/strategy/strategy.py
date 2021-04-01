# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util

class Strategy:

    def __init__(self):
        self.db = mongo_client.fishfin
        self.name = ""
        self.data = list()
        return

    def get_period_timestamp(self,period):
        if "min" in period:
            return int(period.replace("min")) * 60 * 1000
        elif "hour" in period:
            return int(period.replace("hour")) * 60 * 60 * 1000
        elif "week" in period:
            return int(period.replace("week")) * 60 * 60 * 100 * 24 * 7
        elif "mon" in period:
            return int(period.replace("week")) * 60 * 60 * 100 * 24 * 7 * 30
        return 0
    
    def get_max_action_amount(self,user_id,currency,price,trans_fee,account_type="simulation"):
        tb = None
        if account_type == "simulation":
            tb = self.db.user_simulation_currency
        else:
            tb = None
        info = tb.find_one({"user_id":user_id,"currency":currency})
        balance = info["balance"]
        max_amount = round(float(balance)/price * ( 1 - trans_fee),6)
        return max_amount

    def run(self,symbol,period,start_ktime,end_ktime):
        return

    def get_price_list(self,name="close"):
        prices = list()
        for item in self.data:
            if name in item:
                prices.append(item[name])
        return prices

    #release quantization signal: buy, sell, keep
    def signal(self,user_id,symbol,period,strategy,ktime,data,signal):
        self.db.user_quantization_signal.update({"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":ktime},{"$set":{"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":ktime,"data":data,"singal":signal}},upsert=True)
        return

    #quantization log
    def log(self,info):
        info["update_time"] = time.time()
        _id = self.db.strategy_log.insert_one(info)
        return _id
