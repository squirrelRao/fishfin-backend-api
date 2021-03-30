# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from trade import Trade

class SimulationTrade(Trade):

    def __init__(self):
        super(SimulationTrade, self).__init__()
        self.name = "simulation" 
        return

    #submit market transaction: buy/sell
    def submit_market_transaction(self,user_id,symbol,amount,price,currency,trans_fee,ktime,_type="buy"):
        order_id = self.create_order(user_id,amount,price,symbol,trans_fee,currency)
        quote_currency = symbol.replace(currency,"")

        quote_currency_balance = self.db.user_simulation_currency.find_one({"user_id":user_id,"currency":quote_currency})
        base_currency_balance = self.db.user_simulation_currency.find_one({"user_id":user_id,"currency":currency})

        log_id = self.log(user_id,order_id,amount,price,symbol,currency,trans_fee,base_currency_balance,quote_currency_balance,ktime,action="new")
        base_change = 0 # symbol is btcusdt, base currency is btc , quote currency is usdt
        quote_change = 0
    
        if _type == "buy":
            base_change = amount
            quote_change = 0 - amount * price - amount * price * trans_fee
        elif _type == "sell":
            base_change = 0 - amount
            quote_change = amount * price - amount * price * trans_fee
        
        db.user_simulation_currency.update({"user_id":user_id,"currency":currency},{"$inc":{"balance":base_change}})
        db.user_simulation_currency.update({"user_id":user_id,"currency":quote_currency},{"$inc":{"balance":quote_change}})
        self.finish_order(order_id)
        self.log(user_id,order_id,amount,price,symbol,currency,trans_fee,base_currency_balance,quote_currency_balance,ktime,action="finish",log_id=log_id)
        return True
