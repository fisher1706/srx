from flask import Flask
from flask import request
import logging

app = Flask(__name__)
import ilx_base_mocks

logging.basicConfig(filename='flask.log',level=logging.DEBUG)
logger = logging.getLogger('flask_server')

@app.before_request
def log_request_info():
    logger.info(request.get_data())

app.run(port='8080', debug=True, host="0.0.0.0")
