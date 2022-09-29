import os
import requests
from bs4 import BeautifulSoup


def download_picture(directory, img_id, img_address):
    """
    Качает картинку и сохраняет её в выбранную директорию.
    Имя скаченной картинки формируется на основе её идентификатора.

    :param directory: путь к директории, куда будут скачиваться картинки.
    :param img_id: идентификатор картинки.
    :param img_address: сетевой адрес картинки.
    :return: Успешно или неуспешно прошла операция загрузки.
    """
    filename = f'{directory}/{str(img_id).rjust(4, "0")}.jpg'
    picture = requests.get(f'https:{img_address}', HEADERS)
    if picture.status_code:
        direct = open(filename, 'wb')
        direct.write(picture.content)
        direct.close()
        return True
    return False


def directory_manager(directory):
    """
    Создаёт новую директорию с выбранным именем, а также все промежуточные директории, если их нет.
    Если директория уже создана, пересоздаёт её.

    :param directory: имя новой директории (может содержать и промежуточные директории).
    :return: Нет возвращаемого значения.
    """
    while True:
        try:
            os.makedirs(directory)
            break
        except OSError:
            os.removedirs(directory)


def download_quantity_of_photos(search_name, quantity, directory):
    """
    Получает html код страницы https://yandex.ru/images для выбранного поискового запроса.
    Находит в этом коде выбранное количество картинок, соответствующих запросу.
    Сохраняет картинки в выбранную директорию.

    :param search_name: поисковый запрос.
    :param quantity: количество соответствующих запросу картинок, подлежащих скачиванию.
    :param directory: путь к директории, куда будут скачиваться картинки.
    :return: Нет возвращаемого значения.
    """
    url = 'https://yandex.ru/images/'
    images = []
    page = 0
    while len(images) <= quantity:
        html_page = requests.get(f'{url}search?p={page}&text={search_name}&lr=51&rpt=image', HEADERS).text
        soup = BeautifulSoup(html_page, 'lxml')
        page_img = soup.find_all('img')
        for image in page_img:
            if len(image['src']) and image['src'][0] == '/':
                images.append(image['src'])
                print(len(images))
        page += 1
    for i in range(len(images)):
        if not download_picture(directory, i, images[i]):
            print(f'Ошибка загрузки изображения. Его id: {i}')
    del images


HEADERS = {"User-Agent": "Mozilla/5.0"}
directory_manager('dataset/tiger')
directory_manager('dataset/leopard')
download_quantity_of_photos('tiger', 1100, 'dataset/tiger')
download_quantity_of_photos('leopard', 1100, 'dataset/leopard')

if __name__ == '__main__':
    directory_manager()
    download_picture()
    download_quantity_of_photos()
