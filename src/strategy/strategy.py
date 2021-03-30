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
        return


    #quantization log
    def log(self):
        info = {}
        _id = self.db.quantization_log.insert_one(info)
        return _id
