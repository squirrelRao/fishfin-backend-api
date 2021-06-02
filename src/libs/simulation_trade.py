# -*- coding: utf-8 -*-
import sys,os
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from super_trade import Trade

class SimulationTrade(Trade):

    def __init__(self):
        super(SimulationTrade, self).__init__()
        self.name = "simulation" 
        return

    #submit market transaction: buy/sell
    def submit_market_transaction(self,user_id,period,symbol,amount,price,currency,trans_fee=0.002,ktime=time.time(),strategy=None,_type="buy"):
        order_id = self.create_order(user_id,amount,price,symbol,trans_fee,currency,strategy)
        print(currency)
        quote_currency = currency
        currency = "usdt"
        print("quote_currency:",quote_currency,"currency:",currency)
        quote_currency_balance = self.db.user_simulation_currency.find_one({"user_id":user_id,"currency":quote_currency})
        base_currency_balance = self.db.user_simulation_currency.find_one({"user_id":user_id,"currency":currency})

        quote_currency_balance = quote_currency_balance["balance"]
        base_currency_balance = base_currency_balance["balance"]

        log_id = self.log(user_id,order_id,amount,price,period,symbol,currency,trans_fee,base_currency_balance,quote_currency_balance,ktime,strategy,action="new")
        base_change = 0 # symbol is btcusdt, base currency is btc , quote currency is usdt
        quote_change = 0
        # y = x/p * (1-F)
        # x = yp/(1-F)
        # when buy amount is x, is base currency,when sell amount is y, is quote currency
        if _type == "buy":#use usdt buy btc
            if amount > base_currency_balance:
                amount = base_currency_balance
            base_change = float(0) - amount
            quote_change = float(amount / price) *  float( 1 - trans_fee)
            print("amount:",amount,"base_currency_balance:",base_currency_balance,"quote_currency_balance:",quote_currency_balance,_type,"base_change:",base_change,"quote_change:",quote_change)
        elif _type == "sell":#sell btc get usdt
            if amount > quote_currency_balance:
                amount = quote_currency_balance
            base_change = float(amount * price) * float( 1 - trans_fee)
            quote_change = float(0) - float(amount)
            print("amount:",amount,"base_currency_balance:",base_currency_balance,"quote_currency_balance:",quote_currency_balance,_type,"base_change:",base_change,"quote_change:",quote_change)
        else:
            print(amount,_type)
            amount = 0
        base_currency_balance = base_currency_balance + base_change
        quote_currency_balance = quote_currency_balance + quote_change

        self.db.user_simulation_currency.update({"user_id":user_id,"currency":currency},{"$set":{"balance":base_currency_balance}})
        self.db.user_simulation_currency.update({"user_id":user_id,"currency":quote_currency},{"$set":{"balance":quote_currency_balance}})
        
        self.finish_order(order_id)
        self.log(user_id,order_id,amount,price,period,symbol,currency,trans_fee,base_currency_balance,quote_currency_balance,ktime,strategy,action="finish",log_id=log_id)
        return True
