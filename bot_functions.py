from api_key import TOKEN
import json
import requests
import urllib.parse
import time

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
# Offset id argument is sent to ask for updates STARTING FROM this id
def get_updates(offset=None):
    url = url_base + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    content = gen_json(url)
    return content


# This function checks if the parsed message has more than UTF-8 4096 characters (Telegram max size)
# If it is bigger it splits the message in a list
def max_size_checker(parsed_message):
    list_of_messages = []
    if len(parsed_message) > 4096:
        for i in range(4096, 0, -1):
            if (parsed_message[i] == 'A') and (parsed_message[i - 1] == '0') and (parsed_message[i - 2] == '%'):
                list_of_messages.append(parsed_message[0:i-2])
                new = parsed_message[i+1:]
                if len(new) > 4096:
                    list_of_messages = list_of_messages + max_size_checker(new)
                else:
                    list_of_messages.append(new)
                break
    if list_of_messages:
        return list_of_messages
    return parsed_message


# Sends message | receives as parameter the text to be sent and the chat_id | also parses text to url format
def send_message(message_text, chat_id):
    response = None
    parsed_message = urllib.parse.quote_plus(message_text)
    checked_message = max_size_checker(parsed_message)
    if type(checked_message) is list:
        for element in checked_message:
            url = url_base + "sendMessage?text={}&chat_id={}&parse_mode={}".format(element, chat_id, 'Markdown')
            response = http_request(url)
            time.sleep(0.5)
    else:
        url = url_base + "sendMessage?text={}&chat_id={}&parse_mode={}".format(checked_message, chat_id, 'Markdown')
        response = http_request(url)
    return response


# Returns the highest id number, so it can be sent as offset later in get_updates() function
# that way we can tell telegram servers that we already read the updates till that last one
def get_last_id(json_results):
    list_update_ids = []
    for result in json_results['result']:
        list_update_ids.append(int(result['update_id']))
    return max(list_update_ids)


def get_chat_info(json_single_result):
    message = json_single_result['message']['text']
    chat_id = json_single_result['message']['from']['id']
    return message, chat_id
