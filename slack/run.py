import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from slackbot_settings import API_TOKEN
from slackbot.bot import Bot

def main():
    bot = Bot()
    bot.run()

if __name__ == '__main__':
    main()
