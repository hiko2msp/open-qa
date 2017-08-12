import os

import base64
import hmac
import hashlib

from flask import Flask, request, jsonify

app = Flask(__name__)

APP_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', 'dummy secret')

@app.route('/', methods=['GET'])
def crc():
    try:
        crc_token = request.args['crc_token']
        sha256_hash_digest = hmac.new(APP_CONSUMER_SECRET, msg=crc_token, digestmod=hashlib.sha256).digest()
        return jsonify(
            response_token='sha256=' + base64.b64encode(sha256_hash_digest)
        )
    except Exception as e:
        return 'error' + str(e)

if __name__ == '__main__':
    app.run()
