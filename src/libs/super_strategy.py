# -*- coding: utf-8 -*-
import os,sys
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
    
    def get_strategy(self,user_id,symbol,period):
        db = mongo_client.fishfin
        strategy = db.user_strategy.find_one({"user_id":user_id,"symbol":symbol,"period":period})
        return strategy

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
        print({"user_id":user_id,"currency":currency})
        info = tb.find_one({"user_id":user_id,"currency":currency})
        balance = info["balance"]
        max_amount = round(float(balance)/price * ( 1 - trans_fee),10)
        print(max_amount)
        return max_amount

    def run(self,symbol,period,start_ktime,end_ktime):
        return

    def get_price_list(self,name="close"):
        prices = list()
        for item in self.data:
            if name in item:
                prices.append(float(item[name]))
        return prices

    #release quantization signal: buy, sell, keep
    def signal(self,user_id,symbol,period,strategy,ktime,data,trade_amount,signal):
        self.db.user_quantization_signal.update({"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":ktime},{"$set":{"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"trade_amount":trade_amount,"ktime":ktime,"data":data,"singal":signal}},upsert=True)
        return

    #quantization log
    def log(self,info):
        log = info.copy()
        log["update_time"] = time.time()
        #print(log)
        res = self.db.strategy_log.insert_one(log)
        return str(res.inserted_id)
