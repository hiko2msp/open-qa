import os
import json
import base64
import hmac
import hashlib
from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    render_template,
    redirect,
    url_for,
)
import html
from slack.run import BotManager
from reply_pattern import ReplyPatternGspread
bot_manager = BotManager()
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT', 'dummy service account')
reply_pattern = ReplyPatternGspread(json.loads(SERVICE_ACCOUNT))


app = Flask(__name__)


@app.route('/')
def index():
    render_object = {
        'reply_pattern_dict': reply_pattern.get_pattern(),
        'current_api_token': os.environ['API_TOKEN'],
    }
    return render_template('index.html', **render_object)

@app.route('/add', methods=['POST'])
def add():
    print('add start')
    match_pattern = html.escape(request.form['match_pattern'])
    print(match_pattern)
    value = html.escape(request.form['reply_text'])
    print(value)
    reply_pattern.add_pattern(match_pattern, value)
    return jsonify({'status': 200}), 200

@app.route('/delete', methods=['POST'])
def delete():
    print('delete start')
    match_pattern = request.form['match_pattern']
    print(match_pattern)
    reply_pattern.delete_pattern(match_pattern)
    return jsonify({'status': 200}), 200

@app.route('/register_token', methods=['POST'])
def register_token():
    print('register_token')
    api_token = request.form['slack_api_token']
    os.environ['API_TOKEN'] = api_token
    return jsonify({'status': 200}), 200

@app.route('/content')
def content():
    render_object = {
        'reply_pattern_dict': reply_pattern.get_pattern(),
        'current_api_token': os.environ['API_TOKEN'],
    }
    return render_template('pattern_list.html', **render_object), 200

@app.route('/reload', methods=['GET'])
def reload():
    reply_pattern.load()
    return '', 200

@app.route('/save', methods=['GET'])
def save():
    reply_pattern.save()
    print('save finished')
    render_object = {
        'reply_pattern_dict': reply_pattern.get_pattern(),
        'current_api_token': os.environ['API_TOKEN'],
    }
    return render_template('pattern_list.html', **render_object), 200

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('images', 'favicon.png')

@app.route('/trigger', methods=['POST'])
def trigger_bot():
    if bot_manager.is_active():
        try:
            bot_manager.stop()
        except Exception as e:
            print(e)
            return jsonify({'status': 500}), 500
    else:
        bot_manager.start()
    return jsonify({'status': 200}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9006')
