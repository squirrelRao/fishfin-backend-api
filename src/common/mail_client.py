# coding=UTF-8
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bson.objectid import ObjectId
import urllib2
import json
import datetime
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
DEFAULT_SMTP = "smtp.exmail.qq.com"
DEFAULT_PORT = 465

class MailClient:

    def __init__(self,email,pwd,smtp=DEFAULT_SMTP,port=DEFAULT_PORT):
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
            print "no login"
            return False
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = ",".join(to_addr)
        msg['Cc'] = ",".join(cc_addr)
        msg['Subject'] = subject
        msg.attach(MIMEText(body,body_type,'utf-8'))
        self.server.sendmail(self.from_addr, to_addr + cc_addr,msg.as_string())
        print "send complete"

def main():

    client = MailClient("raopingping@caiyunapp.com","rpp085620")
    client.login()
    subject ="test"
    content = '<html><head><meta charset="utf-8"><title>菜鸟教程(runoob.com)</title></head><body><h1>我的第一个标题</h1><p>我的第一个段落。</p></body></html>'
    client.sendMail(subject,content,["hqraop@163.com"])

#main()
