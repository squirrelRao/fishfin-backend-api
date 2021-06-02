# -*- coding: utf-8 -*-
import sys,os
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from model.kline import Kline
from simulation_trade import SimulationTrade
from super_strategy import Strategy
import pandas as pd
import numpy as np
import talib as ta

class RsiStrategy(Strategy):

    def __init__(self):
        super(RsiStrategy,self).__init__()
        self.name = "rsi"
        self.period_count = 14
        self.min_sell_rsi = 30
        self.max_buy_rsi = 70
        return

    #trade_count_type : limit
    def run(self,user_id,quote_currency,base_currency,period,ktime,limit_trade_count,trade_name="simulation"):
        
        symbol = quote_currency + base_currency
        kline = Kline()
        log_info = {"quote_currency":quote_currency,"base_currency":base_currency,"symbol":symbol,"period":period,"ktime":ktime,"strategy":self.name,"limit_trade_count":limit_trade_count,"trade_name":trade_name,"period_count":self.period_count,"min_sell_rsi":self.min_sell_rsi,"max_buy_rsi":self.max_buy_rsi,"user_id":user_id}
        _log_id = self.log(log_info)
        log_info["log_id"] = _log_id
        #load data
        self.data = kline.get_ktime_period_data(symbol,period,self.period_count+1,ktime)
        prices = self.get_price_list("close")
        log_info["data"] = prices
        log_info["data_type"] = "price"
        self.log(log_info)

        #compute index
        rsi = ta.RSI(np.array(prices),self.period_count)
        rsi = round(rsi[len(rsi)-1],6)
        print("rsi:"+str(rsi))
        
        log_info["data"] = rsi
        log_info["data_type"] = "rsi"
        self.log(log_info)

        trade = None
        if trade_name == "simulation":
            trade = SimulationTrade()
        else:
            trade = None
            
        strategy = self.get_strategy(user_id,symbol,period)
        if strategy is not None:
            self.min_sell_rsi = float(strategy["max_sell_rsi"])
            self.max_buy_rsi = float(strategy["min_buy_rsi"])
        #execute transaction action
        action = "keep"
        if rsi <= self.min_sell_rsi:
            action = "sell"
        elif rsi >= self.max_buy_rsi:
            action = "buy"
        amount = 0
        cur_price = prices[-1]
        trans_fee = 0.002
        if  trade is None:
            self.signal(user_id,symbol,period,self.name,ktime,rsi,-1,action)
            log_info["data"] = -1
        else:
            if action in ["buy","sell"]:
                #submit action
                max_trade_count = self.get_max_action_amount(user_id,quote_currency,cur_price,trans_fee,trade_name)
                if max_trade_count < limit_trade_count:
                    amount = max_trade_count
                else:
                    amount = limit_trade_count
                self.signal(user_id,symbol,period,self.name,ktime,rsi,amount,action)
                trade.submit_market_transaction(user_id,period,symbol,amount,cur_price,quote_currency,trans_fee,ktime,self.name,action)
            else:
                self.signal(user_id,symbol,period,self.name,ktime,rsi,0,action)
                quote_currency_balance = self.db.user_simulation_currency.find_one({"user_id":user_id,"currency":quote_currency})["balance"]
                base_currency_balance = self.db.user_simulation_currency.find_one({"user_id":user_id,"currency":base_currency})["balance"]
                trade.log(user_id,"keep_log",0,cur_price,period,symbol,quote_currency,trans_fee,base_currency_balance,quote_currency_balance,ktime,self.name,action="finish",log_id="")
            log_info["data"] = amount
        log_info["data_type"] = action
        log_info["price"] = cur_price 
        self.log(log_info)
        return
