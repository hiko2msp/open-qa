import os

import base64
import hmac
import hashlib
from slack.run import main
from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    render_template,
    redirect,
    url_for,
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
    print('add start')
    match_pattern = request.form['match_pattern']
    print(match_pattern)
    value = request.form['reply_text']
    print(value)
    reply_pattern.add_pattern(match_pattern, value)
    reply_pattern.save()
    print('save finished')
    return jsonify({'status': 200}), 200

@app.route('/delete', methods=['POST'])
def delete():
    print('delete start')
    match_pattern = request.form['match_pattern']
    print(match_pattern)
    reply_pattern.delete_pattern(match_pattern)
    reply_pattern.save()
    print('save finished')
    return jsonify({'status': 200}), 200

@app.route('/content')
def content():
    render_object = {
        'reply_pattern_dict': reply_pattern.get_pattern()
    }
    return render_template('pattern_list.html', **render_object), 200

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/favicon.ico')
def send_image(path):
    return send_from_directory('images', 'favicon.png')

import sys
import logging
import multiprocessing
multiprocessing.log_to_stderr(logging.DEBUG)
sys.path.append('./slack')
from slackbot_settings import API_TOKEN

class BotManager():
    def __init__(self):
        self.p = None


    def start(self):
        if self.p is None:
            self.p = multiprocessing.Process(target=main, daemon=True)
            self.p.start() 

    def stop(self):
        self.p.terminate()
        self.p.join()
        self.p = None

    def is_active(self):
        return self.p is not None

bot_manager = BotManager()

@app.route('/trigger', methods=['POST'])
def trigger_bot():
    if bot_manager.is_active():
        bot_manager.stop()
    else:
        bot_manager.start()
    return jsonify({'status': 200}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9006')
