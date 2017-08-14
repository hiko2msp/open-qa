from slackbot.bot import respond_to, listen_to

@respond_to('hi')
def hi(message):
    message.reply('I can understand hi or HI')
    message.react('+1')
