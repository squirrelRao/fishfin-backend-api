# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from trade import Trade

class HuobiTrade(Trade):

    def __init__(self):
        super(HuobiTrade, self).__init__()
        self.name = "simulation" 
        return

    #submit market transaction: buy-market, sell-market
    def submit_market_transaction(self,symbol,amount,price,_type=None):
        if _type is None:
            return
