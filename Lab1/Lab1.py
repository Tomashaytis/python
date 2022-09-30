import os
import requests
from bs4 import BeautifulSoup
from logging import warning
from tqdm import tqdm
HEADERS = {"User-Agent": "Mozilla/5.0"}


def download_picture(filename, img_address):
    """
    Качает картинку и сохраняет её в выбранную директорию.
    Имя скаченной картинки формируется на основе её идентификатора.

    :param filename: будущее имя скаченного изображения (может содержать и путь до него).
    :param img_address: сетевой адрес картинки.
    :return: Нет возвращаемого значения.
    """
    try:
        picture = requests.get(img_address, HEADERS)
        direct = open(filename, 'wb')
        direct.write(picture.content)
        direct.close()
    except OSError:
        warning(f' Загрузка изображения не удалась.')


def directory_manager(directory):
    """
    Создаёт новую директорию с выбранным именем, а также все промежуточные директории, если их нет.
    Если директория уже создана, оповестит об этом.

    :param directory: имя новой директории (может содержать и промежуточные директории).
    :return: Нет возвращаемого значения.
    """
    folder = os.path.split(directory)
    try:
        os.makedirs(directory)
        print(f'Папка {folder[1]} успешно создана.')
    except OSError:
        print(f'Папка {folder[1]} уже существует.')


def download_quantity_of_photos(search_name, quantity, directory, url='https://yandex.ru/images/'):
    """
    Получает html код страницы https://yandex.ru/images для выбранного поискового запроса.
    Находит в этом коде выбранное количество картинок, соответствующих запросу.
    Сохраняет картинки в выбранную директорию.

    :param search_name: поисковый запрос.
    :param quantity: количество соответствующих запросу картинок, подлежащих скачиванию.
    :param directory: путь к директории, куда будут скачиваться картинки.
    :param url: адрес страницы, с которой будет осуществляться поиск.
    :return: Нет возвращаемого значения.
    """
    checker = 0
    images = []
    page = 0
    no_repeat = 0
    repeaters = 0
    bar = tqdm(total=quantity, desc='Процесс поиска изображений: ', ncols=120)
    while len(images) <= quantity:
        html_page = requests.get(f'{url}search?p={page}&text={search_name}&lr=51&rpt=image', HEADERS)
        if html_page.status_code != 200:
            warning(f' Запрос не был выполнен. Код ответа сайта: {html_page.status_code}')
            return
        if checker > 10:
            warning(' На страницах результатов нет картинок.')
            return
        html_page = html_page.text
        soup = BeautifulSoup(html_page, 'lxml')
        page_img = soup.find_all('img')
        for image in page_img:
            if len(image['src']) and image['src'][0] == '/':
                if no_repeat == 30:
                    no_repeat = 0
                    repeaters = 13
                if repeaters == 0:
                    images.append(f"https:{image['src']}")
                    no_repeat += 1
                    bar.update(1)
                else:
                    repeaters -= 1
                checker = 0
        checker += 1
        page += 1
    del bar
    for i in tqdm(range(len(images)), desc='Процесс скачивания изображений: ', ncols=120):
        filename = os.path.join(directory, f'{str(i).rjust(4, "0")}.jpg')
        download_picture(filename, images[i])
    del images


if __name__ == '__main__':
    tiger_path = os.path.join('dataset', 'tiger1')
    leopard_path = os.path.join('dataset', 'leopard1')
    directory_manager(tiger_path)
    directory_manager(leopard_path)
    download_quantity_of_photos('tiger', 100, tiger_path)
    download_quantity_of_photos('leopard', 100, leopard_path)
