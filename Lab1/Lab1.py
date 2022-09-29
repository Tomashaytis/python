import os
import requests
from bs4 import BeautifulSoup


def download_picture(direct, img_id, img_address):
    """
    Качает картинку и сохраняет её в выбранную директорию.
    Имя скаченной картинки формируется на основе её идентификатора.

    :param direct: путь к директории.
    :param img_id: идентификатор картинки.
    :param img_address: сетевой адрес картинки.
    :return: успешно или неуспешно прошла операция загрузки.
    """
    filename = f'dataset/{direct}/{str(img_id).rjust(4, "0")}.jpg'
    picture = requests.get(f'https:{img_address}', headers)
    if picture.status_code:
        direct = open(filename, 'wb')
        direct.write(picture.content)
        direct.close()
        return True
    return False


def directory_manager(direct):
    """
    Создаёт новую директорию с выбранным именем, а также все промежуточные директории, если их нет.
    Если директория уже создана, пересоздаёт её.

    :param direct: имя новой директории (может содержать и промежуточные директории).
    :return: нет возвращаемого значения.
    """
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
    if not download_picture(name, i, images[i]):
        print(f'Ошибка загрузки изображения. Его id: {i}')
del images

if __name__ == '__main__':
    directory_manager()
    download_picture()
