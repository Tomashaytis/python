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


def copy_file(file_path: str, path_to_copy: str, new_file_name: str) -> None:
    """
    Копирует файл, с местоположением file_path, в папку, с местоположением path_to_copy.
    Переименовывает файл (Новое имя - new_file_name).

    :param file_path: Путь до файла.
    :param path_to_copy: Путь до директории, в которую необходимо скопировать файл.
    :param new_file_name: Новое имя файла.
    :return: Нет возвращаемого значения.
    """
    cur_dir = os.getcwd()
    try:
        shutil.copy(file_path, path_to_copy)
        os.chdir(path_to_copy)
        os.rename(os.path.split(file_path)[1], new_file_name)
        os.chdir(cur_dir)
    except OSError as err:
        os.chdir(cur_dir)
        raise err


def copy_dataset(dataset: str, path_to_copy: str) -> None:
    """
        Копирует экземпляры класса из папки dataset по пути path_to_copy.
        Каждый экземпляр получит префикс перед номером: class_.
        При работе опирается на аннотацию в папке dataset.

        :param dataset: Путь к датасету с экземплярами класса.
        :param path_to_copy: Путь до папки в которую нужно скопировать датасет.
        :return: Нет возвращаемого значения.
        """
    if not os.path.exists(path_to_copy):
        create_directory(path_to_copy)
    dataset_an = Annotation(dataset)
    exemplars = dataset_an.read()
    copy_an = Annotation(path_to_copy)
    for exemplar in exemplars:
        old_file_name = os.path.split(exemplar[1])[1]
        new_file_name = f'{exemplar[2]}_{old_file_name}'
        try:
            copy_file(exemplar[0], path_to_copy, new_file_name)
            copy_an.add(exemplar[2], new_file_name)
        except OSError as err:
            logging.warning(f' При попытке копирования файла {old_file_name} в папку '
                            f'{path_to_copy} произошла ошибка:\n{err}.')
    copy_an.create()


if __name__ == "__main__":
    for i in CLASSES:
        copy_dataset(os.path.join('dataset', i), 'dataset1')
