# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client
from common.common_util import common_util as cu
class HuobiTrade:

    def __init__(self):
        self.host = "https://api-aws.huobi.pro" 
        self.host = "https://api.huobi.pro"
        self.access_key = "00f2bf63-703e6631-dbye2sf5t7-7f94b"
        self.secret_key = "795f1d60-25eee502-07545a80-1c76f"

    #get market status
    def get_market_status(self):
        url = self.host + "/v2/market-status"
        res = net_client.get(url)
        if res["code"] ==200:
            data = {"type":"market_status","data":res["data"]}
            return data
        return None

    #get all symbols
    def get_symbols(self):
        url = self.host + "/v1/common/symbols"
        res = net_client.get(url)
        if res["status"] == "ok":
            data = {"type":"symbol","data":res["data"]}
            return data
        return None

    #get all currencys
    def get_currencys(self):
        url = self.host + "/v1/common/currencys"
        res = net_client.get(url)
        if res["status"] == "ok":
            data = {"type":"currency","data":res["data"]}
            return data
        return None

    #get kline data
    def get_kline(self,symbol,period = "1min",size=1): #period in 1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon, 1week, 1year
        url = self.host + "/market/history/kline?symbol="+symbol+"&period="+period+"&size="+str(size)
        print(url)
        res = net_client.get(url)
        if res["status"] == "ok":
            data = {"type":"kline","name":res["ch"],"data":res["data"]}
            return data
        return None

    def save_data(self,data):
        db = mongo_client.fishfin
        data_type = data["type"]
        if data_type == "kline":
            for item in data["data"]:
                print(item)
                item["ktime"] = item["id"]
                item["ktime_str"] = cu.timestamp_to_string(item["ktime"])
                item["update_time"] = time.time()
                item.pop("id")
                db.kline.update({"name":data["name"],"ktime":item["ktime"]},{"$set":item},upsert=True)
        elif data_type == "currency":
            for item in data["data"]:
                db.currency.update({"name":item},{"$set":{"name":item,"update_time":time.time()}},upsert=True)
        elif data_type == "symbol":
            for item in data["data"]:
                item["update_time"] = time.time()
                db.symbol.update({"symbol":item["symbol"]},{"$set":item},upsert=True)
        elif data_type in ["market_status"]:
            db.market_status.update({"name":data_type},{"$set":{"name":data_type,"data":data,"update_time":time.time()}},upsert=True)
        return 
    

            
def main():
    x = HuobiTrade()
    x.get_kline("btcusdt")

#main()
