import os
import csv
import logging

logger = logging.getLogger()
logger.setLevel('INFO')
CLASSES = ["tiger", "leopard"]


class Annotation:
    _annotation_dir: str
    _exemplars: list

    def __init__(self, dataset_dir):
        """
        При инициализации задаётся директория, содержащая экземпляры класса.

        :param dataset_dir: Путь к датасету с экземплярами класса.
        """
        self._annotation_dir = dataset_dir
        self._exemplars = []

    def __del__(self):
        del self._exemplars

    def add(self, class_mark: str, exemplar: str) -> None:
        """
        Добавляет новую строку для экземпляра exemplar с меткой класса class_mark к сохранённым значениям внутри класса.

        :param exemplar: Экземпляр класса (имя файла).
        :param class_mark: Метка класса добавляемого экземпляра.
        :return: Нет возвращаемого значения.
        """
        try:
            cur_ex = os.path.join(self._annotation_dir, exemplar)
            if not os.path.exists(cur_ex):
                return
            class_exemplar = {'absolute path': os.path.abspath(cur_ex),
                              'relative path': os.path.relpath(cur_ex),
                              'class': class_mark}
            self._exemplars.append(class_exemplar)
        except OSError as err:
            logging.warning(f' При работе с файлами {self._annotation_dir} произошла ошибка:\n{err}.')

    def create_for_class(self, class_mark: str) -> None:
        """
        Создаёт готовую аннотацию для датасета с экземплярами одного класса.

        :param class_mark: Метка класса.
        :return: Нет возвращаемого значения.
        """
        files = os.listdir(self._annotation_dir)
        for n in range(len(files) - 1):
            self.add(class_mark, f'{n:04d}.jpg')
        columns = ['absolute path', 'relative path', 'class']
        an_path = os.path.join(self._annotation_dir, 'annotation.csv')
        with open(an_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, columns)
            writer.writeheader()
            writer.writerows(self._exemplars)

    def create(self) -> None:
        """
        Создаёт аннотацию, используя сохранённые значения внутри класса.
        Если аннотация уже существует, добавит к сохранённым строкам строки существующей аннотации.

        :return: Нет возвращаемого значения.
        """
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

    def read(self) -> list:
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
