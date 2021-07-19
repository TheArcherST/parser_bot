import requests
from bs4 import BeautifulSoup
from typing import Union
from .types import DataPrice, DataShorts, DataOptionsChain, DataHistory
import pandas as pd
from datetime import datetime, date


def to_float(data: Union[str, int]):
    if isinstance(data, str):
        result = ''
        data = data.replace(',', '.')

    return float(data)


def get_soup(url):
    responce = requests.get(url)
    html = responce.text
    soup = BeautifulSoup(html, features="html.parser")

    return soup


def get_price_data() -> DataPrice:
    soup = get_soup('https://www.marketbeat.com/stocks/NYSE/SPCE/')
    price_block = soup.find(class_="price")
    content = price_block.text
    content = content.split(' ')
    raw_cost = content[0]

    if not raw_cost[0].isnumeric():
        raw_cost = raw_cost[1:]

    cost = float(raw_cost)


    all_price_data_tags = soup.find_all(class_='price-data')

    volume = all_price_data_tags[3].text.split(' ')[0][6:]
    average_volume = all_price_data_tags[4].text.split(' ')[1][6:]
    volume, average_volume = to_float(volume), to_float(average_volume)
    volume *= 10 ** 6
    average_volume *= 10 ** 6
    volume, average_volume = int(volume), int(average_volume)

    result = DataPrice(cost, volume, average_volume)

    return result


def get_shorts_data() -> DataShorts:
    soup = get_soup('https://www.marketbeat.com/stocks/NYSE/SPCE/short-interest/')
    all_sections_data = soup.find(class_='mt-2 mb-3').find_all('td')
    current_short_volume = all_sections_data[0].text.split(' ')[0]
    previous_short_volume = all_sections_data[1].text.split(' ')[0]
    current_short_volume, previous_short_volume = current_short_volume.replace(',', ''), previous_short_volume.replace(',', '')
    current_short_volume, previous_short_volume = map(int, [current_short_volume, previous_short_volume])

    result = DataShorts(current_short_volume, previous_short_volume)

    return result


def get_options_chain() -> DataOptionsChain:
    soup = get_soup('https://www.marketbeat.com/stocks/NYSE/SPCE/options/')

    all_lines = soup.find('table').find('tbody').find_all('tr')

    expires = list()
    strike_price = list()
    put_or_call = list()
    volume = list()

    for line in all_lines:
        sections = line.find_all('td')
        if len(sections) == 1:
            continue
        spl = sections[0].text.split('/')
        month = int(spl[0])
        day = int(spl[1])
        year = int(spl[2])
        exemplar_expires = date(year=year, month=month, day=day)
        expires.append(exemplar_expires)

        exemplar_strike_price = to_float(sections[1].text[1:])
        strike_price.append(exemplar_strike_price)

        exemplar_put_or_call = str(sections[3].text.lower())
        put_or_call.append(exemplar_put_or_call)

        exemplar_volume =  to_float(sections[4].text)
        volume.append(exemplar_volume)

    return DataOptionsChain(expires, strike_price, put_or_call, volume)


def get_history() -> DataHistory:
    soup = get_soup('https://www.marketbeat.com/stocks/NYSE/SPCE/price-history/')

    all_lines = soup.find('table').find('tbody').find_all('tr')

    date_ = list()
    opening_price = list()
    closing_price = list()
    volume = list()

    for line in all_lines:
        sections = line.find_all('td')
        if len(sections) == 1:
            continue
        spl = sections[0].text.split('/')
        month = int(spl[0])
        day = int(spl[1])
        year = int(spl[2])
        exemplar_date = date(year=year, month=month, day=day)
        date_.append(exemplar_date)

        exemplar_opening_price = to_float(sections[1]['data-sort-value'])
        opening_price.append(exemplar_opening_price)

        exemplar_closing_price = to_float(sections[2]['data-sort-value'])
        closing_price.append(exemplar_closing_price)

        exemplar_volume =  to_float(sections[5]['data-sort-value'])
        volume.append(exemplar_volume)

    return DataHistory(date_, opening_price, closing_price, volume)
