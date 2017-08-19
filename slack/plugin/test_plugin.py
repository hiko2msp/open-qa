from slackbot.bot import respond_to, listen_to, default_reply
import os

@respond_to('ping')
def ping(message):
    message.reply('Thank you for your ping from {}'.format(os.uname()[1]))
#    message.react('+1')

import json

def load_dictionary(filename):
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    with open(filename) as f:
        return json.load(f)

patern_dictionary = load_dictionary('../../data/pattern.json')

@default_reply
def patern_match(message):
    text = message.body['text']
    match_result = patern_dictionary.get(text)
    if match_result is not None:
        message.send(match_result['reply_text'])
    else:
        message.send('？')
