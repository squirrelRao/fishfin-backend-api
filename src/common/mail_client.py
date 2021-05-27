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

def main():
    (MailClient()).sendLoginCode("hqraop@163.com","1234")


#main()
