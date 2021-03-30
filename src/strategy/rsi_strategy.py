# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from strategy import Strategy

class RsiStrategy(Strategy):

    def __init__(self):
        super(RsiStrategy,self).__init__()
        self.name = "rsi"
        return

   
   
