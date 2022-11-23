import json
import re

import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

import utils

base_url = 'https://nj.lianjia.com/ershoufang/aoti3'


def parse_page(item):
    follow_info = item.find('div', {'class': 'followInfo'}).text.strip()
    tokens = follow_info.split(' / ')
    num_followers = int(re.match(r'^\d+', tokens[0].strip()).group())
    days_past = tokens[1].strip()[:-2]

    house_info = item.find('div', {'class': 'houseInfo'}).text.strip()
    tokens = [t.strip() for t in house_info.split(' | ')]

    try:
        num_rooms = int(re.match(r'\d+(?=室)', tokens[0]).group())
    except AttributeError:
        num_rooms = tokens[0]

    try:
        num_living_rooms = int(re.match(r'\d+(?=厅)', tokens[0]).group())
    except AttributeError:
        num_living_rooms = tokens[0]

    size = float(tokens[1].replace('平米', ''))
    direction = tokens[2].split()
    furnishing = tokens[3]
    height = tokens[4]
    house_type = tokens[5]

    price = utils.convert_unit_value(item.find('div', {'class': 'totalPrice'}).text.strip())

    return {
        'href': item.find('a')['href'],
        'housecode': item.find('a')['data-housecode'],
        'title': re.sub(r'\s+', ' ', item.find('div', {'class': 'title'}).text.strip()),
        'position': item.find('div', {'class': 'positionInfo'}).text.split('-')[0].strip(),
        'price': price,
        'num_rooms': num_rooms,
        'num_living_rooms': num_living_rooms,
        'size': size,
        'direction': direction,
        'furnishing': furnishing,
        'height': height,
        'house_type': house_type,
        'num_followers': num_followers,
        'days_past': days_past,
    }


def scrap_page(page_no):
    url = f'{base_url}/pg{page_no}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode(), 'html.parser')
    items = soup.find('ul', {'class': 'sellListContent'}).find_all('li')
    res = []
    for item in items:
        try:
            parsed_item = parse_page(item)
            res.append(parsed_item)
        except:
            pass
    return res


def scrap_num_pages():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content.decode(), 'html.parser')
    page_data = soup.find('div', {'class': 'house-lst-page-box'})['page-data']
    total_pages = json.loads(page_data)['totalPage']
    return total_pages


if __name__ == '__main__':
    db = TinyDB('nanjing-aoti.json')
    for page_no in range(80, scrap_num_pages() + 1):
        houses = scrap_page(page_no)
        for house in houses:
            if not db.search(Query().housecode == house['housecode']):
                print(f'INSERT {house["title"]} ({house["housecode"]})')
                db.insert(house)
