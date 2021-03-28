from flask import Flask
from flask import request
import json
import logging
from model.huobi import HuobiTrade
from model.user import User

app = Flask(__name__)
logger = app.logger

@app.route('/')
def hello():
    logger.info("test from logger")
    return 'hello water laker'


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
