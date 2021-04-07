# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util

class Task:

    def __init__(self):
        self.db = mongo_client.fishfin
        return


    def new_task(self,user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time):
        task = {"user_id":user_id,"strategy":strategy,"quote_currency":quote_currency,"base_currency":base_currency,"period":period,"limit_trade_count":limit_trade_count,"start_time":start_time,"end_time":end_time}
        task["status"] = 0
        task["create_time"] = time.time()
        self.db.test_task.insert(taks)


    def get_waiting_task(self):
        task = None
        res = self.db.test_task.find({"status":0}).sort("create_time",-1).limit(1)
        for item in res:
            task = item
        return task

    #get task 
    def get_task(self,task_id):
        task = self.db.test_task.find_one({"_id":ObjectId(task_id)})
        task["task_id"] = str(task["_id"])
        return task

    #todo 0, doing 1 done 2 cancel -1
    def update_task_status(self,task_id,status):
        self.db.test_task.update({"_id":ObjectId(task_id)},{"$set":{"status":status,"update_time":time.time()}})
