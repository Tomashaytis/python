import os
import logging
from random import randint
from annotation import Annotation
from dataset_replication import copy_dataset


def random_dataset(dataset: str, path_to_copy: str) -> None:
    """
    Копирует экземпляры класса из папки dataset по пути path_to_copy.
    Каждый экземпляр получит случайный номер от 0000 до 9999.

    :param dataset: Путь к датасету с экземплярами класса.
    :param path_to_copy: Путь до папки в которую нужно скопировать датасет.
    :return: Нет возвращаемого значения.
    """
    copy_dataset(dataset, path_to_copy)
    copy_an = Annotation(path_to_copy)
    instances = copy_an.read()
    random_numbers = set()
    while len(random_numbers) != len(instances):
        random_numbers.add(randint(0, 9999))
    random_numbers = list(random_numbers)
    for inst in range(len(instances)):
        new_filename = f'{random_numbers[inst]:04d}.jpg'
        new_filename_path = os.path.join(os.path.split(instances[inst][1])[0], new_filename)
        old_filename_path = instances[inst][1]
        try:
            os.rename(old_filename_path, new_filename_path)
            copy_an.add(instances[inst][2], new_filename)
        except OSError as err:
            logging.warning(f' При попытке переименования файла по пути {old_filename_path} в папке '
                            f'{path_to_copy} произошла ошибка:\n{err}.')
    copy_an.create()


if __name__ == "__main__":
    random_dataset('dataset1', 'who')
