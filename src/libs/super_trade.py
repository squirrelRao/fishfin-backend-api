# -*- coding: utf-8 -*-
import sys,os
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

    #new order
    def create_order(self,user_id,amount,price,symbol,trans_fee,currency,strategy):
        order = self.db.simulation_trade_order
        if self.name not in ["simulation",""]:
            order = self.db.real_trade_order
        info = {"name":"trade","user_id":user_id,"amount":amount,"price":price,"strategy":strategy,"symbol":symbol,"trans_fee":trans_fee,"currency":currency,"status":0,"update_time":time.time()}
        res = order.insert_one(info)
        return str(res.inserted_id)

    #update order
    def finish_order(self,order_id):
        order = self.db.simulation_trade_order
        if self.name not in ["simulation",""]:
            order = self.db.read_trade_order
        order.update({"_id":ObjectId(order_id)},{"$set":{"status":3}})

    #log trade
    def log(self,user_id,order_id,amount,price,period,symbol,currency,trans_fee,base_currency_balance,quote_currency_balance,ktime,strategy,action="new",log_id=None,rsi=0):
        log = self.db.simulation_trade_log
        if self.name not in ["simulation",""]:
            log = self.db.real_trade_log
        info = {"name":"trade","rsi":rsi,"strategy":strategy,"period":period,"user_id":user_id,"order_id":order_id,"trade_amount":amount,"price":price,"base_currency_balance":base_currency_balance,"quote_currency_balance":quote_currency_balance,"ktime":ktime,"symbol":symbol,"trans_fee":trans_fee,"currency":currency,"action":action,"update_time":time.time()}
        #print(info)
        if log_id is None:
            info["log_id"] = ""
            res = log.insert_one(info)
            return str(res.inserted_id)
        else:
            info["log_id"] = log_id
            res = log.insert_one(info)
            return str(res.inserted_id)

    #submit market transaction: buy-market, sell-market
    def submit_market_transaction(self,symbol,amount,price,ktime,strategy=None,_type=None,rsi=0):
        if _type is None:
            return
