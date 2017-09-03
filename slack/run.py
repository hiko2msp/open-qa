import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import slackbot_settings
from slackbot import settings
from slackbot.bot import Bot
import importlib

def start_bot():
    importlib.reload(slackbot_settings)
    importlib.reload(settings)
    bot = Bot()
    bot.run()

import logging
import multiprocessing
multiprocessing.log_to_stderr(logging.DEBUG)
sys.path.append('./slack')

class BotManager():
    def __init__(self):
        self.p = None

    def start(self):
        if not self.is_active():
            self.p = multiprocessing.Process(target=start_bot)
            self.p.start()
            print(self.p.is_alive(), os.getpid(), self.p.pid)

    def stop(self):
        if not self.p.is_alive():
            return

        print('before termination')
        print(self.p.is_alive(), self.p.exitcode, self.p.pid)
        print('try to terminate')
        self.p.terminate()
        result = self.p.join(0.5)
        print(self.p.is_alive(), self.p.exitcode, self.p.pid, result)
        if self.p.exitcode is None:
            print('Termination failed once')
            print('try to terminate again')
            os.system('kill -9 {}'.format(self.p.pid))
            result = self.p.join(0.5)
            print(self.p.is_alive(), self.p.exitcode, self.p.pid, result)
            if self.p.exitcode is None:
                raise Exception('Termination process failed')
        if not self.p.is_alive():
            self.p = None

    def is_active(self):
        return self.p is not None

if __name__ == '__main__':
    start_bot()
