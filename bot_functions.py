from api_key import TOKEN
import json
import requests
import urllib.parse
# import time

url_base = "https://api.telegram.org/bot{}/".format(TOKEN)

# Bot info
# print(http_request(url_base + 'getme'))


# Makes the http request to Telegram API and returns response from server
def http_request(url):
    data_from_get = requests.get(url)
    data_unicode = data_from_get.text
    return data_unicode


# Transforms response data into a json object, making it possible to work with it as a dict using indexes
def gen_json(url):
    data = http_request(url)
    json_data = json.loads(data)
    return json_data


# Request updates from server | grabs new messages
def get_updates(offset=None):
    url = url_base + "getUpdates"
    content = gen_json(url)
    print(content['result'])


def send_message(message_text, chat_id):
    parsed_message = urllib.parse.quote_plus(message_text)
    url = url_base + "sendMessage?text={}&chat_id={}".format(parsed_message, chat_id)
    http_request(url)

# get_updates()
send_message('testing', 15746192)