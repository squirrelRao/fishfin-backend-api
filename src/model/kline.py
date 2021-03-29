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
