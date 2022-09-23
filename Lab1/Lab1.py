import os
import requests
import re
from bs4 import BeautifulSoup
import cv2

URL = 'https://yandex.ru/images/'+'search?text=' + 'tiger'
max_pages = 10
for page in range(1, max_pages):
    cur_URL = URL + str(page)
    html_page = requests.get(cur_URL).text
    soup = BeautifulSoup(html_page, 'lxml')
    a = soup.find_all('div')
    print(a)
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
'''img = []
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
