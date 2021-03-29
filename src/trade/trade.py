# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util

class Trade:

    def __init__(self):
        self.db = mongo_client.fishfin
        self.name = ""
        return

    #submit market transaction: buy-market, sell-market
    def submit_market_transaction(self,symbol,amount,price,_type=None):
        if _type is None:
            return
