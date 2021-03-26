from flask import Flask
import logging

app = Flask(__name__)
logger = app.logger

@app.route('/')
def hello():
    logger.info("test from logger")
    print("test")  
    return 'hello water laker'


if __name__ != '__main__':
    gun_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gun_logger.handlers
    app.logger.setLevel(gun_logger.level)

if __name__ == '__main__':
    app.run(debug=True)
