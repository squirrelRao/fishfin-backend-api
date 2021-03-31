# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util

class Backtest:

    def __init__(self):
        self.db = mongo_client.fishfin
        return

    def run(self):
        return
