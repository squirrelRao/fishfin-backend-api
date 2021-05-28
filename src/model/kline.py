# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util

class Kline:

    def __init__(self):
        self.db = mongo_client.fishfin
        return
    
    def get_kline_strategy(self,user_id,period,_strategy="rsi"):
        data = []
        watch = list(self.db.user_quantization.find({"status":1,"user_id":user_id}))
        for item in watch:
            item["_id"] = str(item["_id"])
            symbol = item["symbol"]
            open_signal = item["open_signal"]
            strategy = self.db.user_strategy.find_one({"user_id":user_id,"strategy":_strategy,"period":period,"symbol":symbol})
            strategy["_id"] = str(strategy["_id"])
            signal = self.db.user_quantization_signal.find({"user_id":user_id,"strategy":_strategy,"symbol":symbol,"period":period}).sort("ktime",-1).limit(1)
            _signal = None
            for s in signal:
                _signal = s
                _signal["_id"] = str(_signal["_id"])
            line_name = "market."+symbol+".kline."+period
            kline = None
            if _signal is None or time.time() - _signal["ktime"] > 1000 * 60:
                klines = self.db.kline.find({"name":line_name}).sort("ktime",-1).limit(1)
                for k in klines:
                    kline = k
            else:
                kline = self.db.kline.find_one({"ktime":_signal["ktime"],"name":line_name})
            kline["_id"] = str(kline["_id"])
            _data = {"symbol":symbol,"period":period,"watch":item,"kline":kline,"signal":_signal,"strategy":strategy,"ktime":kline["ktime"]}
            data.append(_data)
        return data


    def get_price(self,symbol,period,_type = "latest"):
        line_name = "market."+symbol+".kline."+period
        res = self.db.kline.find({"name":line_name}).sort("ktime",-1).limit(1)
        price = None
        for item in res:
            price = item["close"]
        return price


    def get_ktime_range_data(self,symbol,period,start_ktime=time.time(),end_ktime=time.time(),page_size=None,page_no=None):
        data = list()
        #start_ktime = start_ktime - self.get_period_timestamp() * period_count
        res = None
        if page_size is None:
            res = self.db.kline.find({"name":"market."+symbol+".kline."+period,"ktime":{"$gte":start_ktime,"$lte":end_ktime}}).sort("ktime",1)
        else:
            skip = page_size * ( page_no - 1)
            res = self.db.kline.find({"name":"market."+symbol+".kline."+period,"ktime":{"$gte":start_ktime,"$lte":end_ktime}}).sort("ktime",1).limit(page_size).skip(skip)
        for item in res:
            item.pop("_id")
            data.append(item)
        return data

    def get_ktime_period_data(self,symbol,period,period_count=14,ktime=time.time()):
        data = list()
        res = self.db.kline.find({"name":"market."+symbol+".kline."+period,"ktime":{"$lte":ktime}}).sort("ktime",1).limit(period_count)
        for item in res:
            item.pop("_id")
            data.append(item)
        return data
    
    def get_data(self,symbol,period,page_size=20,page_no=1):
        skip = page_size * ( page_no - 1)
        name = "market."+symbol+".kline."+period
        query = {"name":name}
        total_count = self.db.kline.count(query)
        res = self.db.kline.find(query).sort("ktime",1).limit(page_size).skip(skip)
        data = []
        for item in res:
            item.pop("_id")
            data.append(item)
        return {"total":total_count,"lines":data}

