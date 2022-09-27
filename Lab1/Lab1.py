import os
import requests
from bs4 import BeautifulSoup


def download_picture(direct, img_id, img_address):
    filename = f'dataset/{direct}/{str(img_id).rjust(4, "0")}.jpg'
    picture = requests.get(f'https{img_address}', headers)
    if picture.status_code:
        direct = open(filename, 'wb')
        direct.write(picture.content)
        direct.close()


def directory_manager(direct):
    while True:
        try:
            os.makedirs(direct)
            break
        except OSError:
            os.removedirs(direct)


directory_manager('dataset/tiger')
directory_manager('dataset/leopard')
headers = {"User-Agent": "Mozilla/5.0"}
name = 'tiger'
URL = 'https://yandex.ru/images/'
images = []
page = 0
while len(images) <= 1000:
    html_page = requests.get(f'{URL}search?p={page}&text={name}&lr=51&rpt=image', headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    page_img = soup.find_all('img')
    for image in page_img:
        s = str(image['src'])
        if len(s) and s[0] == '/':
            images.append(image['src'])
            print(len(images))
    page += 1
print(images)
print(len(images))
for i in range(len(images)):
    print(images[i])
    download_picture(name, i, images[i])
del images
'''
max_pages = 40
for page in range(0, max_pages + 1):
    cur_URL = URL + str(page)
    html_page = requests.get(cur_URL, headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    divs = soup.find_all('div', {"class": re.compile(r"serp-item serp-item_type_search serp-item_group_search serp-item_pos_\d+ serp-item_scale_yes justifier__item i-bem$")})
    for i in range(len(divs)):
        img = re.findall(r'"img_href":"([^"]+)"', str(divs[i]))
        images += img
print(len(images))
for i in range(len(images)):
    print(images[i])
    download_picture(tiger, i, images[i])
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
    download_picture(leopard, i, images[i])
del images'''
