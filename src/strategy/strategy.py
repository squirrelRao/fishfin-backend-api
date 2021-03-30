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

    def get_price_list(self,name="close"):
        prices = list()
        for item in self.data:
            if name in item:
                prices.append(item[name])
        return prices

    def load_kline_range_data(self,symbol,period,period_count=14,start_ktime=time.time(),end_ktime=time.time()):
        self.data = list()
        start_ktime = start_ktime - self.get_period_timestamp() * period_count
        res = self.db.kline.find({"name":"market."+symbol+".kline."+period,"ktime":{"$gte":start_ktime,"$lte":end_ktime}}).sort("ktime",-1))
        for item in res:
            item.pop("_id")
            self.data.append(item)
        return self.data

    def load_kline_data(self,symbol,peroid,period_count=14,ktime=time.time()):
        self.data = list()
        res = self.db.kline.find({"name":"market."+symbol+".kline."+period,"ktime":{"$lte":ktime}}).sort("ktime",-1).limit(period_count)
        for item in res:
            item.pop("_id")
            self.data.append(item)
        return self.data

    #quantization log
    def log(self):
        info = {}
        _id = self.db.quantization_log.insert_one(info)
        return _id
