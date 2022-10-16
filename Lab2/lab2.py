import csv
import os
import logging
from typing import List

logger = logging.getLogger()
logger.setLevel('INFO')


class ClassManager:
    _dir: str

    @property
    def dir(self) -> str:
        return self._dir

    @dir.setter
    def dir(self, directory: str) -> None:
        self._dir = directory

    def __init__(self, cur_dir: str = os.getcwd()) -> None:
        self._dir = cur_dir

    def create_annotation(self) -> None:
        try:
            with open(os.path.join(self._dir, 'annotation.csv'), 'w', newline='') as file:
                columns = ['absolute path', 'relative path', 'class']
                class_folders = []
                for root, dirs, files in os.walk(self._dir):
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
            logging.warning(f' При попытке создания аннотации по пути {self._dir} произошла ошибка:\n{err}.')

    def read_annotation(self) -> List:
        res = []
        try:
            with open(os.path.join(self._dir, 'annotation.csv'), 'r', newline='') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    res.append([row['absolute path'], row['relative path'], row['class']])
        except OSError as err:
            logging.warning(f' При попытке открытия аннотации по пути {self._dir} произошла ошибка:\n{err}.')
        return res


if __name__ == "__main__":
    cm = ClassManager('D:\\Projects\\Python\\python')
    cm.create_annotation()
    a = cm.read_annotation()
    for i in a:
        print(i)
