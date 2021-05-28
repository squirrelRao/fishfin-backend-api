# -*- coding: utf-8 -*-
import sys,os
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from bson import ObjectId 
from bson import json_util
from model.kline import Kline

class IaS():

    def __init__(self):
        return

    def symbol_remind(self,user_id,symbol,strategy="rsi"):
        _1min = self.strategy_auto_remind(user_id,symbol,"1min","rsi")
        _5min = self.strategy_auto_remind(user_id,symbol,"5min","rsi")
        _30min = self.strategy_auto_remind(user_id,symbol,"30min","rsi")
        _60min = self.strategy_auto_remind(user_id,symbol,"60min","rsi")
        is_remind = 0
        if _1min["is_remind"] == 1 or _5min["is_remind"] == 1 or _30min["is_remind"] == 1 or _60min["is_remind"] == 1:
            is_remind == 1
        if is_remind == 0:
            return {"is_remind":0}
        return {"is_remind":1,"quote_currency":symbol.replace("usdt",""),"user_id":user_id,"data":{"1min":_1min,"5min":_5min,"30min":_30min,"60min":_60min}}


    def strategy_auto_remind(self,user_id,symbol,period,strategy="rsi"):
        db = mongo_client.fishfin
        watch_size = 15
        signals = db.user_quantization_signal.find({"user_id":user_id,"symbol":symbol,"period":period,"strategy":strategy}).sort("ktime",-1).limit(watch_size)
        signals = list(signals)
        if len(signals) < watch_size or signals[0]["singal"] == "keep":
            return {"is_remind":0}
        else:
            if period == "1min":
                return self.remind_1min(signals)
            elif period == "5min":
                return self.remind_5min(signals)
            elif period == "30min":
                return self.remind_30min(signals)
            elif period == "60min":
                return self.remind_60min(signals)
            else:
                return {"is_remind":0}

    def remind_1min(self,signals):
        latest = signals[0]["singal"]
        desc = "买入"
        if latest == "sell":
            desc = "卖出"
        count = 0
        for signal in signals:
            if signal["singal"] == latest:
                count += 1
        percent = round(float(count)*100/len(signals),2)
        if percent > 50:
            return {"is_remind":1,"signal":signal,"desc":desc}
        return {"is_remind":0}


    def remind_5min(self,signals):
        latest = signals[0]["singal"]
        count = 0
        desc = "买入"
        if latest == "sell":
            desc = "卖出"
        for signal in signals[:10]:
            if signal["singal"] == latest:
                count += 1
        percent = round(float(count)*100/len(signals),2)
        if percent > 50:
            return {"is_remind":1,"signal":signal,"desc":desc}
        return {"is_remind":0}


    def remind_30min(self,signals):
        latest = signals[0]["singal"]
        count = 0
        desc = "买入"
        if latest == "sell":
            desc = "卖出"
        for signal in signals[:8]:
            if signal["singal"] == latest:
                count += 1
        percent = round(float(count)*100/len(signals),2)
        if percent > 50:
            return {"is_remind":1,"signal":signal,"desc":desc}
        else:
            count = 0
            for signal in signals[0:4]:
                if signal["singal"] == latest:
                    count += 1
            percent = round(float(count)*100/len(signals),2)
            if percent >= 50:
                return {"is_remind":1,"signal":signal,"desc":desc}
        return {"is_remind":0}


    def remind_60min(self,signals):
        latest = signals[0]["singal"]
        count = 0
        desc = "买入"
        if latest == "sell":
            desc = "卖出"
        for signal in signals[:4]:
            if signal["singal"] == latest:
                count += 1
        percent = round(float(count)*100/len(signals),2)
        if percent > 50:
            return {"is_remind":1,"signal":signal,"desc":desc}
        else:
            if latest == signals[1]["singal"]:
                return {"is_remind":1,"signal":signal,"desc":desc}
        return {"is_remind":0}
