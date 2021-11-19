from flask import Flask
from flask import request
import logging

logging.basicConfig(filename='flask.log',level=logging.DEBUG)
logger = logging.getLogger('flask_server')

app = Flask(__name__)

@app.before_request
def log_request_info():
    logger.info(request.get_data())

app.run(port='80', debug=True, host="0.0.0.0")
