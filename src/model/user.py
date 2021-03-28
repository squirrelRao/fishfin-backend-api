# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client

class User:

    def __init__(self):
        self.db = mongo_client.fishfin
        return

    
    def update(self,name,avatar=""):
        db.user.update({"name":name},{"$set":{"name":name,"avatar":avatar,"update_time":time.time()}},upsert=True)
        return


    def update_quantization(self,user_id,name,symbol,status=1,open_signal=1,open_trade=0):
        db.user_quantization.update({"user_id":user_id,"symbol":symbol},{"$set":{"user_id":user_id,"name":name,"symbol":symbol,"status":status,"open_signal":open_signal,"open_trade":open_trade}},upsert=True)
        return

    def get_quantization_symbols(self,user_id=None):
        symbols = []
        query = {"status":1}
        if user_is is not None:
            query["user_id"] = user_id
        res = db.user_quantization.find(query)
        for item in symbols:
            if item["symbol"] not in symbols:
                symbols.append(item["symbol"])
        return symbols
