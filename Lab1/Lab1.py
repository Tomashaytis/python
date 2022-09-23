import os
import requests
import re
from bs4 import BeautifulSoup
import cv2
from fake_useragent import UserAgent


def download_picture(direct, img_id, img_address):
    filename = 'dataset/' + direct + '/' + '0' * (4 - len(str(img_id))) + str(img_id) + '.jpg'
    image = requests.get(img_address)
    print(image)
    direct = open(filename, 'wb')
    direct.write(image.content)
    direct.close()


# os.mkdir('dataset')
# os.mkdir('dataset/tiger')
# os.mkdir('dataset/leopard')
URL = 'https://yandex.ru/images/search?text=animal,tiger'
headers = {"User-Agent": UserAgent().chrome}
# download_picture('tiger', 0, 'https://www.fonstola.ru/images/201509/fonstola.ru_202497.jpg')
images = []
max_pages = 10
for page in range(1, max_pages + 1):
    cur_URL = URL + str(page)
    html_page = requests.get(cur_URL, headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    divs = soup.find_all('div', {"class": re.compile(r"serp-item serp-item_type_search serp-item_group_search serp-item_pos_\d+ serp-item_scale_yes justifier__item i-bem$")})
    for i in range(len(divs)):
        img = re.findall(r'"origin":\{"w":\w+,"h":\w+,"url":"([^"]+)"\}', str(divs[i]))
        images += img
print(len(images))
# html_page = requests.get(URL+'search?text=' + 'tiger', headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84 (Edition Yx 05)"})
# soup = BeautifulSoup(html_page.text, 'lxml')
# a = soup.find_all('div', class_="serp-item serp-item_type_search serp-item_group_search ")
# print(soup)
# print('\n', a)
# os.mkdir('dataset')
# os.mkdir('dataset/tiger')
# os.mkdir('dataset/leopard')
# cv2.imwrite('python/dataset/tiger', img[0])
# за каждую итерацию загружается > 100 фотографий
'''
filename = 'dataset/tiger/0000.jpg'
image = requests.get('https://www.fonstola.ru/images/201509/fonstola.ru_202497.jpg')
print(image)
directory = open(filename, 'wb')
directory.write(image.content)
directory.close()

img = []
max_pages = 9
for i in range(max_pages):
    a = re.findall(r'"origin":\{"w":\w+,"h":\w+,"url":"([^"]+)"\}', html_page.text)
    img = img + a
    next_page = re.findall(r'href="/images/([^"]+)"[^E]+Ещё картинки', html_page.text)
    # print(next_page)
    if len(next_page) == 0:
        break
    html_page = requests.get(URL + next_page[0])
print(len(img))'''
