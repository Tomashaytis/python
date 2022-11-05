import os
import logging
from random import randint, shuffle
from annotation import Annotation, CLASSES
from dataset_replication import copy_dataset


def random_dataset(dataset_path: str) -> None:
    """
    Переименовывает экземпляры класса в папке по пути dataset_path.
    Каждый экземпляр получит случайный номер от 0000 до 9999.

    :param dataset_path: Путь до папки в которой будет происходить рандомизация датасета.
    :return: Нет возвращаемого значения.
    """
    an = Annotation(dataset_path)
    instances = an.read()
    random_numbers = set()
    while len(random_numbers) != len(instances):
        random_numbers.add(randint(0, 9999))
    random_numbers = list(random_numbers)
    shuffle(random_numbers)
    for inst, rand in zip(instances, random_numbers):
        new_filename = f'{rand:04d}.jpg'
        new_filename_path = os.path.join(os.path.split(inst[1])[0], new_filename)
        old_filename_path = inst[1]
        try:
            os.rename(old_filename_path, new_filename_path)
            an.add(inst[2], new_filename)
        except OSError as err:
            logging.warning(f' При попытке переименования файла по пути {old_filename_path} в папке '
                            f'{dataset_path} произошла ошибка:\n{err}.')
    an.create()


if __name__ == "__main__":
    for i in CLASSES:
        copy_dataset(os.path.join('dataset', i), 'who')
    random_dataset('who')
