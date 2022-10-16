import csv
import os
import logging
import shutil
from random import randint
from typing import List

logger = logging.getLogger()
logger.setLevel('INFO')


class ClassManager:
    _dataset_dir: str

    def __init__(self, cur_dir: str = os.getcwd()) -> None:
        self._dataset_dir = cur_dir

    @property
    def dir(self) -> str:
        return self._dataset_dir

    @dir.setter
    def dir(self, directory: str) -> None:
        self._dataset_dir = directory

    @staticmethod
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

    def create_annotation(self) -> None:
        try:
            with open(os.path.join(self._dataset_dir, 'annotation.csv'), 'w', newline='') as file:
                columns = ['absolute path', 'relative path', 'class']
                class_folders = []
                for root, dirs, files in os.walk(self._dataset_dir):
                    for class_name in dirs:
                        cur_dir = os.path.join(root, class_name)
                        if len(os.listdir(cur_dir)) >= 1000:
                            class_folder = {'absolute path': os.path.abspath(cur_dir),
                                            'relative path': os.path.relpath(cur_dir),
                                            'class': class_name}
                            class_folders.append(class_folder)
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                writer.writerows(class_folders)
                pass
        except OSError as err:
            logging.warning(f' При попытке создания аннотации по пути {self._dataset_dir} произошла ошибка:\n{err}.')

    def read_annotation(self) -> List:
        res = []
        try:
            with open(os.path.join(self._dataset_dir, 'annotation.csv'), 'r', newline='') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    res.append([row['absolute path'], row['relative path'], row['class']])
        except OSError as err:
            logging.warning(f' При попытке открытия аннотации по пути {self._dataset_dir} произошла ошибка:\n{err}.')
        return res
    
    @staticmethod
    def _copy_img(img_path: str, path_to_copy: str, old_img_name: str, new_img_name: str) -> None:
        cur_dir = os.getcwd()
        try:
            shutil.copy(img_path, path_to_copy)
            os.chdir(path_to_copy)
            os.rename(old_img_name, new_img_name)
            os.chdir(cur_dir)
        except OSError as err:
            os.chdir(cur_dir)
            raise err

    def copy_dataset(self, path_to_copy: str) -> None:
        self.create_directory(path_to_copy)
        self.create_annotation()
        class_list = self.read_annotation()
        for class_path in class_list:
            for img_name in os.listdir(class_path[1]):
                img_path = os.path.join(class_path[1], img_name)
                old_img_name = os.path.split(img_path)[1]
                new_img_name = f'{class_path[2]}_{old_img_name}'
                try:
                    self._copy_img(img_path, path_to_copy, old_img_name, new_img_name)
                except OSError as err:
                    logging.warning(f' При попытке копирования файла {old_img_name} в папку '
                                    f'{path_to_copy} произошла ошибка:\n{err}.')

    def random_dataset(self, path_to_copy: str) -> None:
        self.create_directory(path_to_copy)
        self.create_annotation()
        class_list = self.read_annotation()
        for class_path in class_list:
            for img_name in os.listdir(class_path[1]):
                img_path = os.path.join(class_path[1], img_name)
                old_img_name = os.path.split(img_path)[1]
                new_img_name = f'{randint(0, 9999)}.jpg'
                while True:
                    try:
                        self._copy_img(img_path, path_to_copy, old_img_name, new_img_name)
                        break
                    except FileExistsError:
                        new_img_name = f'{randint(0, 9999)}.jpg'
                    except OSError as err:
                        logging.warning(f' При попытке копирования файла {old_img_name} в папку '
                                        f'{path_to_copy} произошла ошибка:\n{err}.')
                        return
        dataset = self._dataset_dir
        self._dataset_dir = os.getcwd()
        self.create_annotation()
        self._dataset_dir = dataset


if __name__ == "__main__":
    cm = ClassManager('dataset')
    # cm.random_dataset('who')
    # cm.copy_dataset('dataset1')
    '''cm.create_annotation()
    a = cm.read_annotation()
    for i in a:
        print(i)'''
