import os
import requests
import re
from bs4 import BeautifulSoup


def download_picture(direct, img_id, img_address):
    filename = 'dataset/' + direct + '/' + str(img_id).rjust(4, '0') + '.jpg'
    image = requests.get('https' + img_address, headers)
    if image.status_code:
        direct = open(filename, 'wb')
        direct.write(image.content)
        direct.close()


headers = {"User-Agent": "Mozilla/5.0"}
# os.mkdir('dataset')
# os.mkdir('dataset/tiger')
# os.mkdir('dataset/leopard')
URL = 'https://yandex.ru/images/search?text=tiger%20animal%20'
images = []
max_pages = 40
for page in range(0, max_pages + 1):
    cur_URL = URL + str(page)
    html_page = requests.get(cur_URL, headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    print(soup)
    break
    divs = soup.find_all('div', {"class": re.compile(r"serp-item serp-item_type_search serp-item_group_search serp-item_pos_\d+ serp-item_scale_yes justifier__item i-bem$")})
    for i in range(len(divs)):
        img = re.findall(r'"img_href":"([^"]+)"', str(divs[i]))
        images += img
print(len(images))
for i in range(len(images)):
    print(images[i])
    download_picture('tiger', i, images[i])
del images
images = []
URL = 'https://yandex.ru/images/search?text=leopard%20animal%20'
for page in range(1, max_pages + 1):
    cur_URL = URL + str(page)
    html_page = requests.get(cur_URL, headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    img = re.findall(r'"origin":\{"w":\w+,"h":\w+,"url":"([^"]+)"\}', str(divs[i]))
    divs = soup.find_all('div', {"class": re.compile(r"serp-item serp-item_type_search serp-item_group_search serp-item_pos_\d+ serp-item_scale_yes justifier__item i-bem$")})
    for i in range(len(divs)):
        img = re.findall(r'"origin":\{"w":\w+,"h":\w+,"url":"([^"]+)"\}', str(divs[i]))
        images.append(img[0])
for i in range(len(images)):
    download_picture('leopard', i, images[i])
del images
