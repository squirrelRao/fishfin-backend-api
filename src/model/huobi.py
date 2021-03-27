# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from common.mongo_client import mongo_client
from common.net_client import net_client

class HuobiTrade:

    def __init__(self):
        self.host = "https://api-aws.huobi.pro" 
        self.host = "https://api.huobi.pro"
        self.access_key = "00f2bf63-703e6631-dbye2sf5t7-7f94b"
        self.secret_key = "795f1d60-25eee502-07545a80-1c76f"

    def get_kline(self,symbol,period = "1min",size=10): #period in 1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1mon, 1week, 1year
        url = self.host + "/market/history/kline?symbol="+symbol+"&period="+period+"&size="+str(size)
        print(url)
        res = net_client.get(url)
        if res["status"] == "ok":
            data = {"type":"kline","name":res["ch"],"data":res["data"]}
            return data
        return None

    def save_data(self,data):
        db = mongo_client.fishfin
        if data["type"] == "kline":
            for item in data["data"]:
                item["ktime"] = item["id"]
                item.pop("id")
                db.kline.update({"name":data["name"],"ktime":item["id"]},{"$set":item},upsert=True)
        return 
    

            
def main():
    x = HuobiTrade()
    x.get_kline("btcusdt")

#main()
