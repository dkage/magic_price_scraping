import requests
from api_key import TELEGRAM_KEY


class Telegram:

    def __init__(self):
        self.url = "https://api.telegram.org/bot{}/".format(TELEGRAM_KEY)

        self.offset = ''
        self.name = ''

