from bs4 import BeautifulSoup
import requests
import re


def card_url(card_name):
    url = "https://www.ligamagic.com.br/?view=cards%2Fsearch&btSubmit=btSubmit&card=" + card_name
    return url


def get_card(card_name):
    search_url = card_url(card_name)
    request = requests.get(search_url)
    return request.text

# Creates empty dictionary
card_data = {}

# Capture Search Word and append to dictionary
search_words = "mirari's wake"
card_data["search_words"] = search_words
card_data["url_liga"] = "LigaMagic:" + card_url(search_words)


# ------CARD FOUND ------
# ------CARD FOUND ------
# ------CARD FOUND ------

# ------CARD-------
# ------CARD-------
# ------CARD-------

# Gets text through LigaMagic web request
soup = BeautifulSoup(get_card(search_words), "lxml")

# Card frame div
card_frame = soup.find("div", {"class": "card"})

# Grabs card name pt and eng
name_pt = card_frame.find("h3", {"class": "titulo-card b"}).text
name_us = card_frame.find("p", {"class": "subtitulo-card"}).text
card_data["name_pt"] = name_pt
card_data["name_us"] = name_us

# Grabs card img
image = card_frame.find("span", {"id": "omoImage"})
image = [x['src'] for x in image.find_all('img')]
card_data["img"] = image

# -----CARD DETAILS-----
# -----CARD DETAILS-----
# -----CARD DETAILS-----

# Card details frame div
card_details_frame = soup.find("div", {"class": "card-detalhes"}).find("div")

card_details = card_details_frame.findAll("p")
# imagecost = [x['src'] for x in card_details.findAll('img')]

# Grabs price for each edition

# print (card_details_frame.text)
for lines in card_details:
    print(lines)
    print("\n\n\n")
# print (card_data)
