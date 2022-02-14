# coding=UTF-8
import time
import sys
import urllib.request as req
import json
import datetime
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import random

class SmsClient:

    def __init__(self):
        self.access_key = ""
        self.access_token = ""
        self.sign = "阿里云"
        self.region = "cn-hangzhou"
        self.client = AcsClient(self.access_key,self.access_token,self.region)
        return

    def getSmsCode(self,_type):
        if _type == "login":
            return "SMS_122310183"
        elif _type == "remind":
            return "1001"
        else:
            return ""

    def genCode(self,length=6):
        code = ""
        for i in range(length):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            code += ch
        return code


    def sendSms(self,phone,msg,_type,action="SendSms"):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') 
        request.set_version('2017-05-25')
        request.set_action_name(action)
        request.add_query_param('RegionId',self.region)
        request.add_query_param('PhoneNumbers',phone)
        request.add_query_param('SignName',self.sign)
        request.add_query_param('TemplateCode',self.getSmsCode(_type))
        response = self.client.do_action(request)
        return response

def main():
    sms = SmsClient()
    res = sms.sendSms("","","login")
    print(res)
main()
