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


def get_card_info(search_words):

    # Creates empty dictionary that will contain all card info
    card_data = dict()

    # Capture Search Word and append to dictionary
    card_data["search_words"] = search_words
    card_data["url_liga"] = card_url(search_words)

    # Gets text through LigaMagic web request
    soup = BeautifulSoup(get_card(search_words), "lxml")

    # Card frame div
    card_frame = soup.find("div", {"class": "card"})

    # Grabs card name pt and eng
    # noinspection PyBroadException
    try:
        name_pt = card_frame.find("h3", {"class": "titulo-card b"}).text
    except AttributeError:
        return 'Card not found!'
    try:
        name_us = card_frame.find("p", {"class": "subtitulo-card"}).text
    except AttributeError:
        return 'Card not found!'
    card_data["name_pt"] = name_pt  # Add portuguese card name to dictionary
    card_data["name_us"] = name_us  # Add original card name to dictionary

    # Grabs card img
    image = card_frame.find("span", {"id": "omoImage"})
    image = [x['src'] for x in image.find_all('img')]
    card_data["img"] = image  # Add the default img to dictionary (last edition print)

    # Card details frame div to extract data
    card_details_frame = soup.find("div", {"class": "card-detalhes"}).find("div")
    card_details = card_details_frame.text
    card_details = card_details.split('Edições')[0]  # Selects only string part before the 'Edições' section
    card_info = card_details.split('\n')
    for info in card_info:
        info_no_spaces = info.replace(' ', '')
        if info_no_spaces:
            if ':' in info_no_spaces:
                info_no_spaces = info_no_spaces.split(':')
                card_data[info_no_spaces[0]] = info_no_spaces[1]

    # TODO create a treatment for card mana symbols images

    # Grabs the html table that contains the name of each edition and it's prices
    card_eds = soup.find("div", {"class": "card-detalhes"}).find("table")
    prices_string = card_eds.text

    # Grabs name of each edition that the card has been issued
    eds_html_string = ''
    for lines in card_eds:
        eds_html_string = eds_html_string + str(lines)
    eds_names = re.findall(' title="(.*?)"', eds_html_string)
    items = []
    for item in eds_names:  # Creates a new list with each "variacao de preco" appearing in eds_names list
        if item.startswith('Variação de preço'):
            items.append(item)
    eds = [x for x in eds_names if x not in items]  # New list with only elements from eds_name not in items list

    # Grabs prices from each edition and creates a list containing the 3 values
    # those being lowest price, middle price and highest price
    prices_string = prices_string.split('\n\n\n')  # Removes the reoccurring 3 blank lines from extracted string
    prices_list = []
    for elements in prices_string:
        prices = elements.split('\n')  # Separates the string in a list by each line break
        prices = list(filter(None, prices))  # This function removes blank elements in each price list
        if prices:  # If list is not empty adds it's 3 values to the prices_list (removes blank lists)
            prices_list.append(prices)

    eds_with_prices = []
    for price, edition in zip(prices_list, eds):  # Iterates through both lists as a tuple for each index
        values_string = ''
        aux = 0  # Auxiliary that works as a switch/case operation
        for value in price:  # This iteration creates a string that separates the 3 values between ";"
            if aux == 0:
                values_string = value[:-1]
            elif aux == 1:
                values_string = values_string + ";" + value[:-1]
            else:
                values_string = values_string + ";" + value[:-1]
                eds_with_prices.append(edition + '@' + values_string)  # Then finally concatenates edition w/ 3 prices
            aux += 1
    card_data["prices"] = eds_with_prices  # Adds price list to dictionary

    return card_data


# Generates a string containing all information to be printed
def message_layout(card_data):
    message = ''
    message += '*Nome:* _' + card_data['name_pt'] + '_\n'
    message += '*Nome US:* _' + card_data['name_us'] + '_\n'
    message += '*Raridade:* _' + card_data['Raridade'] + '_\n'
    message += '*Cor:* _' + card_data['Cor'] + '_\n'
    message += '*Tipo:* _' + card_data['Tipo'] + '_\n'
    if 'CMC' in card_data:
        message += '*CMC:* _' + str(card_data['CMC']) + '_\n'
    message += '*Formatos válidos:* _' + card_data['FormatosVálidos'].replace(',', ', ') + '_\n'
    message += '```\n======================' + '\n'
    message += 'Edição \n Mínimo | Médio | Máximo' + '\n'
    message += '---------------------------' + '\n'
    for price in card_data['prices']:
        # Ed = Edition | Min = values[0] | Med = values[1] | Max = values[2]
        ed = price.split('@')[0]
        values = price.split('@')[1].split(';')
        message += ed + '\n' + values[0] + ' | ' + values[1] + ' | ' + values[2] + '\n'
        message += '---------------------------' + '\n'

    message += '```'
    message += 'Link da imagem: ' + card_data['img'][0] + '\n'
    message += 'Link na LigaMagic: ' + card_data['url_liga']
    message += '\n\n``` search words used: ' + card_data['search_words'] + '```\n'
    message += '*Artista:* _' + card_data['Artista'] + '_\n'

    return message
