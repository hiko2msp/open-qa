from slackbot.bot import respond_to, listen_to
import os

@respond_to('hi')
def hi(message):
    message.reply('I can understand hi or HI from {}'.format(os.uname()[1]))
    message.react('+1')
