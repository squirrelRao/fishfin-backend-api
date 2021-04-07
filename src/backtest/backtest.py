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
from model.task import Task
from libs.rsi_strategy import RsiStrategy

class Backtest:

    def __init__(self):
        self.db = mongo_client.fishfin
        return

    def run_task(self):
        task = Task()
        task = task.get_waiting_task()
        if task is None:
            return
        task.update_status(task["task_id"],1)
        self.run(task["user_id"],task["strategy"],task["quote_currency"],task["base_currency"],task["period"],task["limit_trade_count"],task["start_time"],task["end_time"])
        task.update_status(task["task_id"],2)

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
        logs = self.db.simulation_trade_log.find({"symbol":symbol,"strategy":strategy,"user_id":user_id,"action":"finish","ktime":{"$gte":start_time,"$lte":end_time}}).sort("ktime",1)
        rates = list()
        logs = list(logs)
        for index,log in enumerate(logs[1:]):
            pre = logs[index-1]
            current = log
            pre_value = pre["price"] * pre["quote_currency_balance"] + pre["base_currency_balance"]
            current_value = current["price"] * current["quote_currency_balance"] + current["base_currency_balance"]
            ror = round((float(current_value - pre_value)/pre_value * 100),2)
            quote_currency_balance = log["quote_currency_balance"]
            base_currency_balance = log["base_currency_balance"]
            self.db.backtest.update({"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":current["ktime"]},{"$set":{"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":current["ktime"],"ror":ror,"quote_currency":quote_currency,"quote_currency_balance":quote_currency_balance,"base_currency":base_currency,"base_currency_balance":base_currency_balance,"trade_log_id":current["log_id"]}},upsert=True)
        return

    def query_result(self,user_id,strategy,quote_currency,base_currency,period,start_time,end_time,action,page_size,page_no):
        symbol = quote_currency + base_currency
        lines = Kline().get_ktime_range_data(symbol,period,start_time,end_time)
        ror  = dict()
        res = self.db.backtest.find({"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"ktime":{"$lte":end_time,"$gte":start_time}})
        for item in res:
            item.pop("_id")
            ror[item["ktime"]] = item
        st = self.db.user_strategy.find_one({"user_id":user_id,"strategy":strategy})
        st.pop("_id")
        res = self.db.user_quantization_signal.find({"user_id":user_id,"strategy":strategy,"symbol":symbol,"period":period,"ktime":{"$lte":end_time,"$gte":start_time}})
        signals = dict()
        for item in res:
            item.pop("_id")
            signals[item["ktime"]] = item

        for line in lines:
            _time = line["ktime"]
            if _time in ror:
                line["rate_of_return"] = ror[_time]["ror"]
                line["trade_log_id"] = ror[_time]["trade_log_id"]
                line["quote_currency"] = ror[_time]["quote_currency"]
                line["quote_currency_balance"] = ror[_time]["quote_currency_balance"]
                line["base_currency"] = ror[_time]["base_currency"]
                line["base_currency_balance"] = ror[_time]["base_currency_balance"]
            if _time in signals:
                line["advice"] = signals[_time]["singal"]
                line["advice_trade_amount"] = signals[_time]["trade_amount"]
                line["rsi"] = signals[_time]["data"]
        _lines = list()
        for _line in lines:
            if _line["advice"] in action:
                _lines.append(_line)
        lines = _lines
        if len(lines) >= page_size * page_no:
            lines = lines[page_size * ( page_no - 1) : page_size * page_no]
        data = {"user_id":user_id,"quote_currency":quote_currency,"base_currency":base_currency,"period":period,"start_time":start_time,"end_time":end_time,"strategy":strategy,"back_result":lines,"strategy_detail":st}
        return data

def clear_data():
    db = mongo_client.fishfin
    db.strategy_log.delete_many({})
    db.user_quantization_signal.delete_many({})
    db.simulation_trade_order.delete_many({})
    db.simulation_trade_log.delete_many({})
    db.backtest.delete_many({})
    db.user_simulation_currency.update_one({"currency":"usdt"},{"$set":{"balance":1000}})
    db.user_simulation_currency.update_one({"currency":"btc"},{"$set":{"balance":0}})




def main():
    #clear_data()
    test = Backtest()
    #user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time
    user_id = "60607bd63a7c1d3802e86243"
    strategy = "rsi"
    quote_currency = "btc"
    base_currency = "usdt"
    period = "1min"#1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon, 1week, 1year
    limit_trade_count = 1000
    start_time = common_util.string_to_timestamp("2021-03-28 00:00:00")
    end_time = common_util.string_to_timestamp("2021-04-02 23:59:00")
    print("start backtest")
    test.run(user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time)
    print("backtest end ")

#main()

#clear_data()
