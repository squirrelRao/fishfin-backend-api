# coding=UTF-8
import time
import sys
from bson.objectid import ObjectId
import json
import datetime
import smtplib
import email
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
DEFAULT_SMTP = "smtp.163.com"
DEFAULT_PORT = 465
DEFAULT_MAIL = "hqraop@163.com"
DEFAULT_PWD = "TJBXMTEIFYSEPUIJ"

class MailClient:

    def __init__(self,email=DEFAULT_MAIL,pwd=DEFAULT_PWD,smtp=DEFAULT_SMTP,port=DEFAULT_PORT):
        self.from_addr = email
        self.pwd = pwd
        self.smtp = smtp
        self.port = port
        self.server = None

    def login(self):
        if self.server is not None:
            self.logout()
        self.server = smtplib.SMTP_SSL(self.smtp,self.port)
        self.server.login(self.from_addr,self.pwd)

    def logout(self):
        self.server.close() if self.server is not None else None

    def sendMail(self,subject,body,to_addr,cc_addr=[],body_type="html"):
        if self.server is None:
            print("no login")
            return False
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = ",".join(to_addr)
        msg['Cc'] = ",".join(cc_addr)
        msg['Subject'] = subject
        msg.attach(MIMEText(body,body_type,'utf-8'))
        self.server.sendmail(self.from_addr, to_addr + cc_addr,msg.as_string())
        print("send complete")
        
    def sendLoginCode(self,mail_to,code):
        self.login()
        subject = "【鱼鳍】您的登录验证码"
        content = '<html><head><meta charset="utf-8"><title>您的登录验证码</head><body><h5>您的登录验证码是:'+code+'</h5></body></html>'
        self.sendMail(subject,content,[mail_to])
   
    def sendSignalRemind(self,mail_to,data):
        if "desc" not in data["data"]["1min"]:
            data["data"]["1min"]["desc"] = "持有"
        if "desc" not in data["data"]["5min"]:
            data["data"]["5min"]["desc"] = "持有"
        if "desc" not in data["data"]["30min"]:
            data["data"]["30min"]["desc"] = "持有"
        if "desc" not in data["data"]["60min"]:
            data["data"]["60min"]["desc"] = "持有"
        subject = "【鱼鳍】你关注的"+data["quoto_currency"]+" 发现显著的买卖信号请查看"
        content = '<html><head></head><body><p>'+data["quote_currency"]+'的买卖信号如下，请及时决策:</p>'
        content += '<p>1min频率上:'+data["data"]["1min"]["desc"]+'</p>'
        content += '<p>5min频率上:'+data["data"]["5min"]["desc"]+'</p>'
        content += '<p>30min频率上:'+data["data"]["30min"]["desc"]+'</p>'
        content += '<p>60min频率上:'+data["data"]["60min"]["desc"]+'</p>'
        content += '</body></html>'
        self.sendMail(subject,content,[mail_to])

def main():
    (MailClient()).sendLoginCode("hqraop@163.com","1234")


#main()
