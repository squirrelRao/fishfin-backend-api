from flask import Flask
from flask import request
import json
import logging
from model.huobi import HuobiTrade

app = Flask(__name__)
logger = app.logger

@app.route('/')
def hello():
    logger.info("test from logger")
    print("test")  
    return 'hello water laker'


@app.route('/v1/trade/data/push',methods=['POST'])
def save_data():
    logger.info("save data")
    data = request.get_data()
    data = json.loads(data)
    ht = HuobiTrade()
    ht.save_data(data)
    return {"rc":0}


if __name__ != '__main__':
    gun_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gun_logger.handlers
    app.logger.setLevel(gun_logger.level)

if __name__ == '__main__':
    app.run(debug=True)
