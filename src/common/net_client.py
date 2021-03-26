# coding=UTF-8
import time
import sys
import urllib
import json
import datetime

    
class NetClient:

    #request third-service api
    def postThirdService(self,url,data,methods="POST",headers={'Content-Type':'application/json'}):
        print("TEST")
