# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from strategy import Strategy
from model.kline import Kline
from trade.simulation_trade import SimulationTrade
import pandas as pd
import numpy as np
import talib as ta

class RsiStrategy(Strategy):

    def __init__(self):
        super(RsiStrategy,self).__init__()
        self.name = "rsi"
        self.period_count = 14
        self.min_sell_rsi = 70
        self.max_buy_rsi = 30
        return

    #trade_count_type : limit
    def run(self,user_id,quote_currency,base_currency,period,ktime,limit_trade_count,trade_name="simulation"):
        
        symbol = quote_currency + base_currency
        kline = Kline()
        #load data
        self.data = kline.get_ktime_period_data(symbol,peroid,self.period_count,ktime)
        prices = self.get_price_list("close")
        print(prices)

        #compute index
        rsi = ta.RSI(prices,period_count)
        print("rsi:"+str(rsi))
        
        trade = None
        if trade_name == "simulation":
            trade = SimulationTrade()
        else:
            trade = None

        #execute transaction action
        action = None
        if rsi >= min_sell_rsi:
            action = "sell"
        elif rsi <= max_bug_rsi:
            action = "buy"
        
        #submit action
        cur_price = prices[0]
        trans_fee = 0.002
        max_trade_count = self.get_max_action_amount(user_id,quote_currency,cur_price,trans_fee,trade_name)
        amount = 0
        if max_trade_count < limit_trade_count:
            amount = max_trade_count
        else:
            amount = limit_trade_count
        trade.submit_market_transaction(user_id,symbol,amount,cur_price,quote_currency,trans_fee,ktime,action)
        return
