import os

import base64
import hmac
import hashlib

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    render_template
)

app = Flask(__name__)

APP_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', 'dummy secret').encode()

@app.route('/crc', methods=['GET'])
def crc():
    crc_token = request.args['crc_token'].encode()
    print(crc_token)
    sha256_hash_digest = hmac.new(APP_CONSUMER_SECRET, msg=crc_token, digestmod=hashlib.sha256).digest()
    print(sha256_hash_digest)
    return jsonify(
        response_token=(b'sha256=' + base64.b64encode(sha256_hash_digest)).decode()
    )

from reply_pattern import ReplyPattern
reply_pattern = ReplyPattern()

@app.route('/')
def index():
    render_object = {
        'message': 'テストメッセージ',
        'reply_pattern_dict': reply_pattern.get_pattern()
    }
    return render_template('index.html', **render_object)

@app.route('/add', methods=['POST'])
def add():
    render_object = {
        'message': 'テストメッセージ',
        'reply_pattern_dict': reply_pattern.get_pattern()
    }
    return render_template('index.html', **render_object)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == '__main__':
    app.run()
