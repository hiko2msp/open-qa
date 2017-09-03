#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
from slackbot.bot import respond_to, listen_to, default_reply
from main import reply_pattern

@respond_to('ping')
def ping(message):
    message.reply('Thank you for your ping from {}'.format(os.uname()[1]))


def load_dictionary(filename):
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    with open(filename) as f:
        return json.load(f)


@default_reply
def patern_match(message):
    text = message.body['text']
    match_result = reply_pattern.get_reply_messages(text)
    if match_result:
        message.send(match_result[0]['reply_text'])
    else:
        message.send('？')
