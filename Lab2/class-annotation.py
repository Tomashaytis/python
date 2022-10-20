import os
import csv
import logging
from typing import List

logger = logging.getLogger()
logger.setLevel('INFO')
CLASSES = ["tiger", "leopard"]


class Annotation:
    _annotation_dir: str

    def __init__(self, dataset_dir):
        """
        При инициализации задаётся директория, содержащая экземпляры класса.
        Создаётся файл annotation.csv, если он ещё не был создан.
        :param dataset_dir: Путь к датасету с экземплярами класса.
        """
        self._annotation_dir = dataset_dir
        an_path = os.path.join(self._annotation_dir, 'annotation.csv')
        if not os.path.exists(an_path):
            columns = ['absolute path', 'relative path', 'class']
            with open(an_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, columns)
                writer.writeheader()

    def add(self, class_mark: str) -> None:
        """
        Добавляет к файлу-аннотации следующий по счёту экземпляр с меткой класса class_mark.
        :param class_mark: Метка класса добавляемого экземпляра.
        :return: Нет возвращаемого значения.
        """
        try:
            with open(os.path.join(self._annotation_dir, 'annotation.csv'), 'a+', newline='') as file:
                rows = self.read()
                files = os.listdir(self._annotation_dir)
                if len(files) == 1 or len(rows) == len(files) - 1:
                    return
                cur_ex = os.path.join(self._annotation_dir, files[len(rows)])
                columns = ['absolute path', 'relative path', 'class']
                class_exemplar = {'absolute path': os.path.abspath(cur_ex),
                                  'relative path': os.path.relpath(cur_ex),
                                  'class': class_mark}
                writer = csv.DictWriter(file, columns)
                writer.writerow(class_exemplar)
                pass
        except OSError as err:
            logging.warning(f' При попытке создания аннотации по пути {self._annotation_dir} произошла ошибка:\n{err}.')

    def create_for_class(self, class_mark: str) -> None:
        """
        Создаёт готовую аннотацию для датасета с экземплярами одного класса.
        :param class_mark: Метка класса.
        :return: Нет возвращаемого значения.
        """
        for exemplar in range(len(os.listdir(self._annotation_dir)) - 1):
            self.add(class_mark)

    def read(self) -> List:
        """
        Читает аннотацию, возвращая список с путями к экземплярам и их метками классов.
        :return: Список путей к экземплярам с и их метками классов.
        """
        res = []
        try:
            with open(os.path.join(self._annotation_dir, 'annotation.csv'), 'r', newline='') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    res.append([row['absolute path'], row['relative path'], row['class']])
        except OSError as err:
            logging.warning(f' При попытке открытия аннотации по пути {self._annotation_dir} произошла ошибка:\n{err}.')
        return res


if __name__ == "__main__":
    for i in CLASSES:
        an = Annotation(os.path.join('dataset', i))
        an.create_for_class(i)
