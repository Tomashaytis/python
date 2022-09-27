import os
import requests
from bs4 import BeautifulSoup


def download_picture(direct, img_id, img_address):
    filename = f'dataset/{direct}/{str(img_id).rjust(4, "0")}.jpg'
    picture = requests.get(f'https:{img_address}', headers)
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
URL = 'https://yandex.ru/images/'
name = 'tiger'
images = []
page = 0
while len(images) <= 1000:
    html_page = requests.get(f'{URL}search?p={page}&text={name}&lr=51&rpt=image', headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    page_img = soup.find_all('img')
    for image in page_img:
        if len(image['src']) and image['src'][0] == '/':
            images.append(image['src'])
            print(len(images))
    page += 1
for i in range(len(images)):
    download_picture(name, i, images[i])
del images
name = 'leopard'
images = []
page = 0
while len(images) <= 1000:
    html_page = requests.get(f'{URL}search?p={page}&text={name}&lr=51&rpt=image', headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    page_img = soup.find_all('img')
    for image in page_img:
        if len(image['src']) and image['src'][0] == '/':
            images.append(image['src'])
            print(len(images))
    page += 1
for i in range(len(images)):
    download_picture(name, i, images[i])
del images

if __name__ == '__main__':
    directory_manager()
    download_picture()
