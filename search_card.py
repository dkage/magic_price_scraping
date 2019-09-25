from bs4 import BeautifulSoup
import requests
import re
import urllib.parse


def card_url(card_name):
    parameter = {'card': card_name}
    parameter = urllib.parse.urlencode(parameter)
    url = "https://www.ligamagic.com.br/?view=cards/card&" + parameter
    return url


def get_card(card_name):
    search_url = card_url(card_name)
    request = requests.get(search_url)
    # print(search_url)
    return request.text


