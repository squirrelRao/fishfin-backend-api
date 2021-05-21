from flask import Flask
from flask import request
import os,sys
import json
from bson import json_util
import logging
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"src/libs"))
from model.huobi import HuobiTrade
from model.user import User
from model.kline import Kline
from common.mongo_client import mongo_client
from backtest.backtest import Backtest
from common.common_util import common_util
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},supports_credentials=True)
logger = app.logger


@app.route('/')
def hello():
    logger.info("test from logger")
    return 'hello water laker'


@app.route('/v1/regist',methods=['POST'])
def regist():
    data = request.get_data()
    data = json.loads(data)
    phone = data.get("phone","")
    name = data.get("name","")
    invite_code = data.get("invite_code","")
    db = mongo_client.fishfin
    _codes = [""]
    _user = db.user.find_one({"phone":phone})
    if _user is not None:
        return {"rc":-1,"msg":"registed"}
    elif invite_code not in _codes:
        return {"rc":-2,"msg":"invite_code is invalid"}
    else:
        db.user.insert({"phone":phone,"name":name,"invite_code":invite_code,"update_time":time.time()})
        return {"rc":0}

@app.route('/v1/login',methods=['POST'])
def login():
    data = request.get_data()
    data = json.loads(data)
    phone = data.get("phone","")
    code = data.get("code","")
    db = mongo_client.fishfin
    _user = db.user.find_one({"phone":phone})
    if _user is None:
        return {"rc":-1,"data":{"msg":"user is not found"}}
    _name = _user["name"]
    if _name is None or _name == "":
        _name = _user["phone"][0:3]+"****"+_user["phone"][-4:]
    else:
        _name = _user["name"]
    if _user is not None and code is not None:
        return {"rc":0,"data":{"user_id":str(_user["_id"]),"name":_name}}
    return {"rc":-1}

@app.route('/v1/logout',methods=['POST'])
def logout():
    data = request.get_data()
    data = json.loads(data)
    phone = data.get("phone","")
    return {"rc":0}


@app.route('/v1/backtest/query',methods=['POST'])
def get_backtest_result():
    data = request.get_data()
    data = json.loads(data)
    backtest = Backtest()
    #strategy,quote_currency,base_currency,period,start_time,end_time
    user_id = data.get("user_id","")
    quote_currency = data.get("quote_currency","")
    base_currency = data.get("base_currency","")
    period = data.get("period","")
    start_time = data.get("start_time","")
    end_time = data.get("end_time","")
    strategy = data.get("strategy","rsi")
    page_size = data.get("page_size",30)
    page_no = data.get("page_no",1)
    action = data.get("action",["keep","buy","sell"])
    start_time = common_util.string_to_timestamp(start_time)
    end_time = common_util.string_to_timestamp(end_time)
    data = backtest.query_result(user_id,strategy,quote_currency,base_currency,period,start_time,end_time,action,page_size,page_no)
    return {"rc":0,"data":data}


@app.route('/v1/symbol/query',methods=['POST'])
def get_currencys():
    data = request.get_data()
    data = json.loads(data)
    db = mongo_client.fishfin
    key = data.get("key","")
    user_id = data.get("user_id","")
    query = {"base-currency":{"$regex":".*"+key+".*"},"quote-currency":"usdt"}
    res = list(db.symbol.find(query))
    data = []
    for item in res:
        _item =  {"currency":item["base-currency"],"is_watch":0}
        watch = db.user_quantization.find_one({"user_id":user_id,"symbol":item["base-currency"]+"usdt"})
        if watch is not None:
            _item["is_watch"] = 1
        data.append(_item)
    rs = {"rc":0,"data":data}
    return json.loads(json_util.dumps(rs))


@app.route('/v1/kline/query',methods=['POST'])
def get_kline():
    data = request.get_data()
    data = json.loads(data)
    kline = Kline()
    logger.info(data)
    res = kline.get_data(data["symbol"],data["period"],data["page_size"],data["page_no"])
    return {"rc":0,"data":res}

@app.route('/v1/trade/data/basic',methods=['GET'])
def get_trade_basic_info():
    db = mongo_client.fishfin
    currency = list(db.currency.find({}))
    symbol = list(db.symbol.find({}))
    market_status = list(db.market_status.find({}))
    
    rs = {"rc":0,"data":{"market_status":market_status,"currency_count":len(currency),"symbol_count":len(symbol)}}
    return json.loads(json_util.dumps(rs))

@app.route('/v1/symbol/watch/list',methods=['GET'])
def get_symbol_watch_list():
    user = User()
    symbols = user.get_quantization_symbols()
    return {"rc":0,"data":symbols}

@app.route('/v1/trade/data/push',methods=['POST'])
def save_data():
    logger.info("save data")
    data = request.get_data()
    data = json.loads(data)
    ht = HuobiTrade()
    ht.save_data(data)
    return {"rc":0}

@app.route('/v1/user/quantization/update',methods=['POST'])
def update_user_quantization():
    data = request.get_data()
    data = json.loads(data)
    user = User()
    _user = user.get_user(data["user_id"])
    if _user is None:
        return {"rc":-1,"msg":"user not found"}
    user.update_quantization(data["user_id"],_user["name"],data["symbol"],status = data["status"])
    return {"rc":0}


if __name__ != '__main__':
    gun_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gun_logger.handlers
    app.logger.setLevel(gun_logger.level)

if __name__ == '__main__':
    app.run(debug=True)

