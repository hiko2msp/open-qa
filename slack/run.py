import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import slackbot_settings
from slackbot.bot import Bot
import importlib

def main():
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
        importlib.reload(slackbot_settings)
        print(slackbot_settings.API_TOKEN)
        print(os.environ['API_TOKEN'])
        if not self.is_active():
            self.p = multiprocessing.Process(target=main)
            self.p.start()
            print(self.p.is_alive(), os.getpid(), self.p.pid)

    def stop(self):
        print('before terminate')
        print(self.p.is_alive(), self.p.exitcode, self.p.pid)
        print('try terminate')
        self.p.terminate()
        result = self.p.join(0.5)
        print(self.p.is_alive(), self.p.exitcode, self.p.pid, result)
        if self.p.exitcode is None:
            print('try terminate failed once')
            print('try terminate again')
            os.system('kill -9 {}'.format(self.p.pid))
            result = self.p.join(0.5)
            print(self.p.is_alive(), self.p.exitcode, self.p.pid, result)
            if self.p.exitcode is None:
                raise Exception('terminate process failed')
        if not self.p.is_alive():
            self.p = None

    def is_active(self):
        return self.p is not None

if __name__ == '__main__':
    main()
