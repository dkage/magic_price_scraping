import requests
from api_key import TELEGRAM_KEY
import json


class Telegram:

    def __init__(self):
        self.url = "https://api.telegram.org/bot{}/".format(TELEGRAM_KEY)

        self.offset = ''
        self.name = ''

    def get_me(self):
        get_me = self.url + 'getme'

        http_return = requests.get(get_me).json()

        if http_return['ok']:
            return True
        else:
            return False

    def send_message(self):
        # TODO scope
        return True


    def get_updates(self):
        #TODO scope
        return True
