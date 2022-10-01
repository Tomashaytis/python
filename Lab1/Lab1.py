import os
import requests
from bs4 import BeautifulSoup
import logging
from tqdm import tqdm
HEADERS = {"User-Agent": "Mozilla/5.0"}

logger = logging.getLogger()
logger.setLevel('INFO')


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
    except OSError as err:
        logging.warning(f' При попытке загрузки изображения произошла ошибка:\n{err}')


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
        logging.info(f' Папка {folder[1]} успешно создана.')
    except OSError as err:
        logging.info(f' При попытке создания папки {folder[1]} произошла ошибка:\n{err}.')


def download_quantity_of_photos(search_name, quantity, directory, url='https://yandex.ru/images/', min_page_photos=5):
    """
    Получает html код страницы https://yandex.ru/images для выбранного поискового запроса.
    Находит в этом коде выбранное количество картинок, соответствующих запросу.
    Сохраняет картинки в выбранную директорию.

    :param search_name: поисковый запрос.
    :param quantity: количество соответствующих запросу картинок, подлежащих скачиванию.
    :param directory: путь к директории, куда будут скачиваться картинки.
    :param url: адрес страницы, с которой будет осуществляться поиск.
    :param min_page_photos: Минимальное количество картинок на странице сайта.
    :return: Нет возвращаемого значения.
    """
    no_repeat = 0
    repeaters = 0
    page = 0
    images = []
    bar = tqdm(total=quantity, desc='Процесс поиска изображений: ', ncols=120)
    while len(images) <= quantity:
        html_page = requests.get(f'{url}search?p={page}&text={search_name}&lr=51&rpt=image', HEADERS)
        if html_page.status_code != 200:
            del bar
            logging.warning(f' Запрос не был выполнен. Код ответа сайта: {html_page.status_code}')
            return
        html_page = html_page.text
        soup = BeautifulSoup(html_page, 'lxml')
        page_img = soup.find_all('img')
        if len(page_img) < min_page_photos:
            del bar
            logging.warning(' На страницах результатов нет картинок.')
            return
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
        page += 1
    del bar
    for i in tqdm(range(len(images)), desc='Процесс скачивания изображений: ', ncols=120):
        filename = os.path.join(directory, f'{str(i).rjust(4, "0")}.jpg')
        download_picture(filename, images[i])
    del images


if __name__ == '__main__':
    tiger_path = os.path.join('dataset', 'tiger')
    leopard_path = os.path.join('dataset', 'leopard')
    directory_manager(tiger_path)
    directory_manager(leopard_path)
    download_quantity_of_photos('tiger', 1000, tiger_path)
    download_quantity_of_photos('leopard', 1000, leopard_path)
