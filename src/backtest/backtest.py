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
        _task = Task()
        task = _task.get_waiting_task()
        if task is None:
            return
        task["_id"] = str(task["_id"])
        _task.update_task_status(task["_id"],1)
        start_time = common_util.string_to_timestamp(task["start_time"])
        end_time = common_util.string_to_timestamp(task["end_time"])
        self.run(task["_id"],task["user_id"],task["strategy"],task["quote_currency"],task["base_currency"],task["period"],task["limit_trade_count"],start_time,end_time)
        _task.update_task_status(task["_id"],2)

    def run(self,task_id,user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time):
        st = None
        if strategy == "rsi":
            st = RsiStrategy()
        
        self.db.user_simulation_currency.update({"currency":quote_currency},{"$set":{"balance":0}})
        self.db.user_simulation_currency.update({"currency":base_currency},{"$set":{"balance":5000}})


        kline = Kline()
        symbol = quote_currency + base_currency
        lines = kline.get_ktime_range_data(symbol,period,start_time,end_time)
        #execute strategy
        for line in lines:
            st.run(user_id,quote_currency,base_currency,period,line["ktime"],limit_trade_count,trade_name="simulation")
        
        #compute rate of return
        logs = self.db.simulation_trade_log.find({"period":period,"symbol":symbol,"strategy":strategy,"user_id":user_id,"action":"finish","ktime":{"$gte":start_time,"$lte":end_time}}).sort("ktime",1)
        rates = list()
        logs = list(logs)
        step = 0
        if period == "1min":
            step = 60 * 24
        elif period == "5min":
            step = 12 * 24
        elif period == "30min":
            step =  2 * 24
        elif period == "60min":
            step = 24
        total_ror = 0
        avg_ror = 0
        _i = 0
        last_current_value = 0
        for index,log in enumerate(logs[0:]):
            if index % ( step - 1 ) != 0:
                continue 
            pre = logs[index]
            end_index = -1
            if index + step >= len(logs):
                end_index = -1
            else:
                end_index = index+step-1
            current = logs[end_index]
            pre_value = pre["price"] * pre["quote_currency_balance"] + pre["base_currency_balance"]
            current_value = current["price"] * current["quote_currency_balance"] + current["base_currency_balance"]
            ror = round((float(current_value - pre_value)/pre_value * 100),2)
            total_ror += ror
            _i += 1
            quote_currency_balance = current["quote_currency_balance"]
            base_currency_balance = current["base_currency_balance"]
            last_current_value = current_value
            self.db.backtest.update({"task_id":task_id,"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy,"start_ktime":pre["ktime"],"end_ktime":current["ktime"]},{"$set":{"task_id":task_id,"user_id":user_id,"symbol":symbol,"pre_quote_currency_balance":pre["quote_currency_balance"],"pre_base_currency_balance":pre["base_currency_balance"],"period":period,"strategy":strategy,"start_price":pre["price"],"end_price":current["price"],"start_value":pre_value,"end_value":current_value,"start_index":index,"end_index":end_index,"start_ktime":pre["ktime"],"end_ktime":current["ktime"],"ror":ror,"ror_period":"24hour","quote_currency":quote_currency,"current_quote_currency_balance":quote_currency_balance,"base_currency":base_currency,"current_base_currency_balance":base_currency_balance,"trade_log_id":current["log_id"]}},upsert=True)
        if _i != 0:
            avg_ror = round(total_ror/_i,2)
        task =  Task()
        task.update_task_ror(task_id,avg_ror,total_ror,last_current_value)
        task.update_task_status(task_id,2) #2 means complete
        return

    def query_result_by_task(self,task):
        
        print(task)
        data = self.query_result(task)
        return data

    def query_result(self,task):
        ror  = list()
        res = self.db.backtest.find({"task_id":str(task["_id"])})
        last_total_ror = 0
        for item in res:
            item.pop("_id")
            item["start_ktime_str"] = common_util.timestamp_to_string(item["start_ktime"])
            item["end_ktime_str"] = common_util.timestamp_to_string(item["end_ktime"])
            item["ror"] = round(item["ror"],2)
            item["end_value"] = str(item["end_value"])
            item["start_value"] = str(item["start_value"])
            last_total_ror += item["ror"]
            item["total_ror"] = round(last_total_ror,2)
            ror.append(item)
        st = self.db.user_strategy.find_one({"user_id":task["user_id"],"strategy":"rsi"})
        st.pop("_id")
        data = {"back_result":ror,"strategy_detail":st}
        return data

def clear_data():
    db = mongo_client.fishfin
    db.strategy_log.delete_many({})
    db.user_quantization_signal.delete_many({})
    db.simulation_trade_order.delete_many({})
    db.simulation_trade_log.delete_many({})




def main():
    clear_data()
    test = Backtest()
    #user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time
    user_id = "60607bd63a7c1d3802e86243"
    strategy = "rsi"
    quote_currency = "shib"
    base_currency = "usdt"
    period = "1min"#1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon, 1week, 1year
    limit_trade_count = 1000
    start_time = common_util.string_to_timestamp("2021-05-26 00:00:00")
    end_time = common_util.string_to_timestamp("2021-06-02 00:00:00")
    db = mongo_client.fishfin
    db.user_simulation_currency.update({"currency":quote_currency},{"$set":{"balance":0}})
    db.user_simulation_currency.update({"currency":"usdt"},{"$set":{"balance":5000}})
    task_id = "60b6fe55c113f6e0e9b853ff" 
    print("start backtest")
    test.run(task_id,user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time)
    print("backtest end ")


#task = (Task()).get_task("60b6fe55c113f6e0e9b853ff")
#(Backtest()).query_result_by_task(task)
#clear_data()
#main()
#query(se_currency_balance"])
