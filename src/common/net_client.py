# coding=UTF-8
import time
import sys
import urllib.request as req
import json
import datetime

    
class NetClient:

    #request network url
    def request(self,url,data={},method="POST",header={'Content-Type':'application/json'},coding='utf-8'):
        data = json.dumps(data).encode(coding) 
        request = req.Request(url,data = data,headers = header,method = method)
        response = req.urlopen(request)
        rs = response.read().decode(coding)
        return rs



net_client = NetClient()
def main():
    x = NetClient()
    print(x.request("http://www.baidu.com",{"test":"a"},"GET"))

#main()
