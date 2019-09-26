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
        print(http_return['ok'])

        if http_return['ok']:
            return True
        else:
            return False
