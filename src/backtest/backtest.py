# -*- coding: utf-8 -*-
import sys,os
import time
sys.path.append("..")
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"libs"))
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from common.common_util import common_util
from model.kline import Kline
from libs.rsi_strategy import RsiStrategy

class Backtest:

    def __init__(self):
        self.db = mongo_client.fishfin
        return

    def run(self,user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time):
        
        st = None
        if strategy == "rsi":
            st = RsiStrategy()
        
        kline = Kline()
        symbol = quote_currency + base_currency
        lines = kline.get_ktime_range_data(symbol,period,start_time,end_time)
        
        #execute strategy
        for line in lines:
            st.run(user_id,quote_currency,base_currency,period,line["ktime"],limit_trade_count,trade_name="simulation")

        #compute rate of return
        logs = self.db.simulation_trade_log.find({"symbol":symbol,"strategy":strategy,"user_id":user_id,"peroid":peroid,"action":"finish","ktime":{"$gte":start_time,"$lte":end_time}}).sort("ktime",-1)
        rates = list()
        for index,log in enumerate(logs[1:]):
            pre = logs[index-1]
            current = log
            pre_value = pre["price"] * pre["quote_currency_balance"] + pre["base_currency_balance"]
            current_value = current["price"] * current["quote_currency_balance"] + current["base_currency_balance"]
            ror = round(float(current_value - pre_value)/pre_value * 100,2)
            self.db.backtest.update({"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":current["ktime"]},{"$set":{"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":current["ktime"],"ror":ror,"trade_log_id":current["log_id"]}},upsert=True)
        return

    def query_result(self,user_id,strategy,quote_currency,base_currency,period,start_time,end_time):
        symbol = quote_currency + base_currency
        lines = kline.get_ktime_range_data(symbol,period,start_time,end_time)
        test_results = list()
        res = self.db.backtest.find({"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":{"$lte":start_time,"$gte":end_time}})
        for item in res:
            item.pop("_id")
            test_results.append(item)
        st = self.db.user_strategy.find_one({"user_id":user_id,"strateg":strategy})
        st.pop("_id")
        
        res = self.db.user_quantization_signal.find({"user_id":user_id,"strategy":strategy,"symbol":symbol,"peroid":period,"ktime":{"$lte":start_time,"$gte":end_time}})
        signals = []
        for item in res:
            item.pop("_id")
            signals.append(item)

        data = {"user_id":user_id,"quote_currency":quote_curreny,"base_currency":base_currency,"period":period,"start_time":start_time,"end_time":end_time,"strategy":strategy,"ror":test_results,"kline":lines,"signal":signals}
        return data


def main():
    test = Backtest()
    #user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time
    user_id = "60607bd63a7c1d3802e86243"
    strategy = "rsi"
    quote_currency = "btc"
    base_currency = "usdt"
    period = "1min"
    limit_trade_count = 1000
    start_time = common_util.string_to_timestamp("2021-03-29 20:00:00")
    end_time = common_util.string_to_timestamp("2021-03-30 00:00:00")
    print("start backtest")
    test.run(user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time)
    print("backtest end ")
