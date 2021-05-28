#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import os
sys.path.append("..")
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"libs"))
from common.net_client import net_client
from common.mongo_client import mongo_client
from common.common_util import CommonUtil
from common.mail_client import MailClient
from model.user import User
from libs.ias import IaS

from model.kline import Kline
import datetime
from datetime import date

#signal monitor
def signal_monitor_remind():
    db = mongo_client.fishfin
    users = db.user.find({"status":1})
    ias = IaS()
    mailClient = MailClient()
    for user in users:
        user_id = str(user["_id"])
        watch = list(db.user_quantization.find({"status":1,"user_id":user_id}))
        for item in watch:
            data = ias.symbol_remind(user_id,item["symbol"],"rsi")
            print(user["mail"]+":"+item["symbol"]+":"+str(data))
            if data["is_remind"] == 0:
                continue
            else:
                mailClient.sendSignalRemind(user["mail"],item["symbol"])



signal_monitor_remind()
