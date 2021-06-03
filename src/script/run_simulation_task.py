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
from model.user import User
from model.task import Task
from backtest.backtest import Backtest
from libs.rsi_strategy import RsiStrategy
from model.kline import Kline
import datetime
from datetime import date


def simulate_task():
    db = mongo_client.fishfin
    task = (Task()).get_waiting_task()
    if task is None:
        print("no task waiting to go")
        return
    max_running_count = 1
    running_count = (Task()).get_running_task_count()
    if running_count >= max_running_count:
        print("running task count is up to max limit,waiting...")
        return

    backtest = Backtest()
    start = time.time()
    print("start backtest",str(task["_id"]),"-",task["user_id"])
    #(task_id,user_id,strategy,quote_currency,base_currency,period,limit_trade_count,start_time,end_time)
    backtest.run(str(task["_id"]),task["user_id"],task["strategy"],task["quote_currency"],task["base_currency"],task["period"],task["limit_trade_count"],task["start_time"],task["end_time"])
    print("end backtest",str(task["_id"]),"-",task["user_id"],"-","spent:",(time.time() - start))


simulate_task()
