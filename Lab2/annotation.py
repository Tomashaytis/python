import os
import csv
import logging
from typing import List

logger = logging.getLogger()
logger.setLevel('INFO')
CLASSES = ["tiger", "leopard"]


class Annotation:
    _annotation_dir: str
    _exemplars: List

    def __init__(self, dataset_dir):
        """
        При инициализации задаётся директория, содержащая экземпляры класса.
        Создаётся файл annotation.csv, если он ещё не был создан.
        :param dataset_dir: Путь к датасету с экземплярами класса.
        """
        self._annotation_dir = dataset_dir
        self._exemplars = []

    def __del__(self):
        del self._exemplars

    def add(self, class_mark: str, ex_number: int) -> None:
        """
        Добавляет к файлу-аннотации следующий по счёту экземпляр с меткой класса class_mark.
        :param ex_number: Номер экземпляра в списке экземпляров.
        :param class_mark: Метка класса добавляемого экземпляра.
        :return: Нет возвращаемого значения.
        """
        try:
            files = os.listdir(self._annotation_dir)
            if len(files) == 1 or ex_number >= len(files) - 1:
                return
            cur_ex = os.path.join(self._annotation_dir, files[ex_number])
            class_exemplar = {'absolute path': os.path.abspath(cur_ex),
                              'relative path': os.path.relpath(cur_ex),
                              'class': class_mark}
            self._exemplars.append(class_exemplar)
        except OSError as err:
            logging.warning(f' При работе с файлами {self._annotation_dir} произошла ошибка:\n{err}.')

    def create(self, class_mark: str = None) -> None:
        """
        Создаёт готовую аннотацию для датасета с экземплярами одного класса.
        :param class_mark: Метка класса.
        :return: Нет возвращаемого значения.
        """
        if class_mark is not None:
            files = os.listdir(self._annotation_dir)
            for n in range(len(files) - 1):
                self.add(class_mark, n)
        columns = ['absolute path', 'relative path', 'class']
        an_path = os.path.join(self._annotation_dir, 'annotation.csv')
        if os.path.exists(an_path):
            rows = self.read()
            adder = []
            for row in rows:
                adder = adder + [dict(zip(columns, row))]
            self._exemplars = adder + self._exemplars
        with open(an_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, columns)
            writer.writeheader()
            writer.writerows(self._exemplars)

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
        an.create(i)

'''import os
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
        :param dataset_dir: Путь к датасету с экземплярами класса.
        """
        self._annotation_dir = dataset_dir

    def create_for_copy(self, class_marks: List) -> None:
        """
        Создаёт готовую аннотацию для датасета с экземплярами одного класса.
        :param class_marks: Список меток класса добавляемых экземпляров.
        :return: Нет возвращаемого значения.
        """
    def create_for_class(self, class_mark: str) -> None:
        """
        Создаёт готовую аннотацию для датасета с экземплярами одного класса.
        :param class_mark: Метка класса добавляемых экземпляров.
        :return: Нет возвращаемого значения.
        """
        try:
            columns = ['absolute path', 'relative path', 'class']
            files = os.listdir(self._annotation_dir)
            class_exemplars = []
            with open(os.path.join(self._annotation_dir, 'annotation.csv'), 'w', newline='') as file:
                for filename in files:
                    cur_ex = os.path.join(self._annotation_dir, filename)
                    class_exemplar = {'absolute path': os.path.abspath(cur_ex),
                                      'relative path': os.path.relpath(cur_ex),
                                      'class': class_mark}
                    class_exemplars.append(class_exemplar)
                writer = csv.DictWriter(file, columns)
                writer.writeheader()
                writer.writerows(class_exemplars)
        except OSError as err:
            logging.warning(f' При попытке добавления новой строки к аннотации по пути {self._annotation_dir}'
                            f' произошла ошибка:\n{err}.')

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
        an.create_for_class(i)'''
