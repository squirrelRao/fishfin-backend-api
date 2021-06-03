# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from common.common_util import common_util
from bson import ObjectId 
from bson import json_util

class Task:

    def __init__(self):
        self.db = mongo_client.fishfin
        return


    def new_task(self,user_id,strategy,quote_currency,base_currency,period,init_amount,limit_trade_count,buy_rsi,sell_rsi,start_time,end_time):
        task = {"user_id":user_id,"strategy":strategy,"quote_currency":quote_currency,"base_currency":base_currency,"period":period,"init_amount":init_amount,"limit_trade_count":limit_trade_count,"buy_rsi":buy_rsi,"sell_rsi":sell_rsi,"start_time":start_time,"end_time":end_time}
        task["status"] = 0
        task["create_time"] = time.time()
        self.db.test_task.insert(task)

    def query_task(self,user_id,page_size,page_no):
        skip = page_size * ( page_no - 1)
        count = self.db.test_task.count({"status":{"$ne":-1}})
        
        res = self.db.test_task.find({"user_id":user_id,"status":{"$ne":-1}}).sort("create_time",-1).limit(page_size).skip(skip)
        x = []
        for item in res:
            item["_id"] = str(item["_id"])
            item["create_time_str"] = common_util.timestamp_to_string(item["create_time"])
            item["start_time"] = item["start_time"][:10]
            item["end_time"] = item["end_time"][:10]
            if "last_current_value" not in item:
                item["last_current_value"] = 0
            item["last_current_value"] = round(item["last_current_value"],6) 
            x.append(item)
            
        data = {"count":count,"data":x}
        return data
    
    def get_running_task_count(self):
        count = self.db.test_task.count({"status":1})
        return count

    def get_waiting_task(self):
        task = None
        res = self.db.test_task.find({"status":0}).sort("create_time",-1).limit(1)
        for item in res:
            task = item
        return task

    #get task 
    def get_task(self,task_id):
        task = self.db.test_task.find_one({"_id":ObjectId(task_id)})
        task["start_time_origin"] = task["start_time"]
        task["end_time_origin"] = task["end_time"]
        task["start_time"] = task["start_time"][:10]
        task["end_time"] = task["end_time"][:10]
        
        task["create_time_str"] = common_util.timestamp_to_string(task["create_time"])
        if "last_current_value" not in task:
            task["last_current_value"] = 0
        task["last_current_value"] = round(task["last_current_value"],6)
        task["task_id"] = str(task["_id"])
        return task
    
    def update_task_ror(self,task_id,avg_ror,total_ror,last_current_value):
        self.db.test_task.update({"_id":ObjectId(task_id)},{"$set":{"last_current_value":last_current_value,"avg_ror":avg_ror,"total_ror":total_ror,"update_time":time.time()}})

    #todo 0, doing 1 done 2 cancel -1
    def update_task_status(self,task_id,status):
        self.db.test_task.update({"_id":ObjectId(task_id)},{"$set":{"status":status,"update_time":time.time()}})
