# coding=UTF-8
import time
import sys
import urllib.request as req
import json
import datetime
import requests


class CommonUtil:


    def timestamp_to_string(self,timestamp,_format = "%Y-%m-%d %H:%M:%S"):
        return time.strftime(_format, time.localtime(timestamp))


    def string_to_timestamp(self,dt,_format = "%Y-%m-%d %H:%M:%S"):
        timeArray = time.strptime(dt,_format)
        timestamp = time.mktime(timeArray)
        return timestamp


common_util = CommonUtil()
