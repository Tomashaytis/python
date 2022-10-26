import os
import logging
from random import randint
from annotation import Annotation, CLASSES
from dataset_replication import create_directory, copy_file


def random_dataset(dataset: str, path_to_copy: str) -> None:
    """
    Копирует экземпляры класса из папки dataset по пути path_to_copy.
    Каждый экземпляр получит случайный номер от 0000 до 9999.

    :param dataset: Путь к датасету с экземплярами класса.
    :param path_to_copy: Путь до папки в которую нужно скопировать датасет.
    :return: Нет возвращаемого значения.
    """
    if not os.path.exists(path_to_copy):
        create_directory(path_to_copy)
    dataset_an = Annotation(dataset)
    instances = dataset_an.read()
    copy_an = Annotation(path_to_copy)
    for instance in instances:
        old_filename = os.path.split(instance[1])[1]
        new_filename = f'{randint(0, 9999):04d}.jpg'
        while True:
            try:
                copy_file(instance[1], path_to_copy, new_filename)
                copy_an.add(instance[2], new_filename)
                break
            except FileExistsError:
                new_filename = f'{randint(0, 9999):04d}.jpg'
            except OSError as err:
                logging.warning(f' При попытке копирования файла {old_filename} в папку '
                                f'{path_to_copy} произошла ошибка:\n{err}.')
                return
    copy_an.create()


if __name__ == "__main__":
    for i in CLASSES:
        random_dataset(os.path.join('dataset', i), 'who')
