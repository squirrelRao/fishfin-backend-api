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

    def get_price(self,symbol,_type = "latest"):
        line_name = "market."+symbol+".kline.1min"
        res = self.db.kline.find({"name":line_name}).sort("ktime":-1).limit(1)
        price = None
        for item in res:
            price = item["close"]
        return price


    def get_ktime_range_data(self,symbol,period,start_ktime=time.time(),end_ktime=time.time()):
        data = list()
        #start_ktime = start_ktime - self.get_period_timestamp() * period_count
        res = self.db.kline.find({"name":"market."+symbol+".kline."+period,"ktime":{"$gte":start_ktime,"$lte":end_ktime}}).sort("ktime",-1))
        for item in res:
            item.pop("_id")
            data.append(item)
        return data

    def get_ktime_period_data(self,symbol,peroid,period_count=14,ktime=time.time()):
        data = list()
        res = self.db.kline.find({"name":"market."+symbol+".kline."+period,"ktime":{"$lte":ktime}}).sort("ktime",-1).limit(period_count)
        for item in res:
            item.pop("_id")
            data.append(item)
        return data
    
    def get_data(self,symbol,period,page_size=20,page_no=1):
        skip = page_size * ( page_no - 1)
        name = "market."+symbol+".kline."+period
        query = {"name":name}
        total_count = self.db.kline.count(query)
        res = self.db.kline.find(query).sort("ktime",-1).limit(page_size).skip(skip)
        data = []
        for item in res:
            item.pop("_id")
            data.append(item)
        return {"total":total_count,"lines":data}
