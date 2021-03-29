# coding=UTF-8
import time
import sys
import urllib.request as req
import json
import datetime
import requests
    
class NetClient:

    def __init__(self):
        self.session = requests.Session()

    def get(self,url,res_type="json"):
        self.session = requests.Session()
        res = self.session.get(url)
        self.session.close()
        if res_type =="json":
            return res.json()
        elif res_type == "text":
            return res.text
        else:
            return res.content

    def post(self,url,data,header={'Content-Type':'application/json'},res_type="json"):
        data = json.dumps(data) 
        self.session = requests.Session()
        res = self.session.post(url,data = data,headers = header,timeout=60)
        self.session.close()
        if res_type == "json":
            return res.json()
        elif res_type == "text":
            return res.text
        else:
            return res.content


net_client = NetClient()
def main():
    x = NetClient()
    print(x.request("http://www.baidu.com",{"test":"a"},"GET"))

#main()
