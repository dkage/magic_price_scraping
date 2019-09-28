import requests
from api_key import TELEGRAM_KEY
import json


class Telegram:

    def __init__(self):
        self.url = "https://api.telegram.org/bot{}/".format(TELEGRAM_KEY)

        self.offset = ''
        self.name = ''
        self.bot_id = ''
        self.updates_json = '0'

    def get_me(self):
        get_me = self.url + 'getme'

        http_return = requests.get(get_me).json()

        self.name = http_return['result']['username']
        self.bot_id = http_return['result']['id']

        if http_return['ok']:
            return True
        else:
            return False

    def send_message(self):
        return True

    def get_updates(self):
        update_url = self.url + 'getUpdates?timeout=100'

        # If offset is already set, concatenates it to tell API last ID already received
        if self.offset:
            update_url += "&offset={}".format(self.offset)
        http_response = requests.get(update_url)
        json_response = http_response.json()
        self.updates_json = json_response['result']

        # Set variable offset to tell API url, the last update ID already received
        print(json_response)
        self.offset = int(json_response['result'][-1]['update_id']) + 1

        if json_response['ok']:
            return json_response['result']
        else:
            return False
