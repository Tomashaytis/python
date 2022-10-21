import os
import logging
import shutil
from annotation import Annotation

logger = logging.getLogger()
logger.setLevel('INFO')
CLASSES = ["tiger", "leopard"]


def create_directory(path):
    """
    Создаёт новую директорию с выбранным именем, а также все промежуточные директории, если их нет.
    Если директория уже создана, оповестит об этом.
    :param path: Путь до новой директории.
    :return: Нет возвращаемого значения.
    """
    folder = os.path.split(path)
    try:
        os.makedirs(path)
        logging.info(f' Папка {folder[1]} успешно создана.')
    except OSError as err:
        logging.info(f' При попытке создания папки {folder[1]} произошла ошибка:\n{err}.')


def copy_img(img_path: str, path_to_copy: str, old_img_name: str, new_img_name: str) -> None:
    cur_dir = os.getcwd()
    try:
        shutil.copy(img_path, path_to_copy)
        os.chdir(path_to_copy)
        os.rename(old_img_name, new_img_name)
        os.chdir(cur_dir)
    except OSError as err:
        os.chdir(cur_dir)
        raise err


def copy_dataset(dataset: str, path_to_copy: str) -> None:
    if not os.path.exists(path_to_copy):
        create_directory(path_to_copy)
    dataset_an = Annotation(dataset)
    exemplars = dataset_an.read()
    copy_an = Annotation(path_to_copy)
    for exemplar in exemplars:
        old_img_name = os.path.split(exemplar[1])[1]
        new_img_name = f'{exemplar[2]}_{old_img_name}'
        try:
            copy_img(exemplar[0], path_to_copy, old_img_name, new_img_name)
            copy_an.add(exemplar[2], new_img_name)
        except OSError as err:
            logging.warning(f' При попытке копирования файла {old_img_name} в папку '
                            f'{path_to_copy} произошла ошибка:\n{err}.')
    copy_an.create()


if __name__ == "__main__":
    for i in CLASSES:
        copy_dataset(os.path.join('dataset', i), 'dataset1')
