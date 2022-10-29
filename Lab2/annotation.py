import os
import csv
import logging

logger = logging.getLogger()
logger.setLevel('INFO')
CLASSES = ["tiger", "leopard"]


class Annotation:
    """
    Класс предлагает методы для работы с аннотацией к датасету.
    """

    def __init__(self, dataset_dir: str):
        """
        При инициализации задаётся директория, содержащая экземпляры класса.

        :param dataset_dir: Путь к датасету с экземплярами класса.
        """
        self._annotation_dir = dataset_dir
        self._instances = []
        self.__header = ['absolute path', 'relative path', 'class']

    def __del__(self):
        del self._instances

    def add(self, class_mark: str, instance: str) -> None:
        """
        Добавляет новую строку для экземпляра instance с меткой класса class_mark к сохранённым значениям внутри класса.

        :param instance: Экземпляр класса (имя файла).
        :param class_mark: Метка класса добавляемого экземпляра.
        :return: Нет возвращаемого значения.
        """
        try:
            cur_ex = os.path.join(self._annotation_dir, instance)
            if not os.path.exists(cur_ex):
                return
            class_instance = {self.__header[0]: os.path.abspath(cur_ex),
                              self.__header[1]: os.path.relpath(cur_ex),
                              self.__header[2]: class_mark}
            self._instances.append(class_instance)
        except OSError as err:
            logging.warning(f' При работе с файлами {self._annotation_dir} произошла ошибка:\n{err}.')

    def create_for_class(self, class_mark: str) -> None:
        """
        Создаёт готовую аннотацию для датасета с экземплярами одного класса.

        :param class_mark: Метка класса.
        :return: Нет возвращаемого значения.
        """
        files = os.listdir(self._annotation_dir)
        for n in range(len(files)):
            self.add(class_mark, f'{n:04d}.jpg')
        self.create()

    def add_from_old_annotation(self) -> None:
        """
        Добавляет данные из уже существующей аннотации, к сохранённым значениям внутри класса.

        :return: Нет возвращаемого значения.
        """
        if os.path.exists(os.path.join(self._annotation_dir, 'annotation.csv')):
            rows = self.read()
            adder = []
            for row in rows:
                adder = adder + [dict(zip(self.__header, row))]
            self._instances = adder + self._instances

    def create(self) -> None:
        """
        Создаёт аннотацию, используя сохранённые значения внутри класса.

        :return: Нет возвращаемого значения.
        """
        with open(os.path.join(self._annotation_dir, 'annotation.csv'), 'w', newline='') as file:
            writer = csv.DictWriter(file, self.__header)
            writer.writeheader()
            writer.writerows(self._instances)

    def read(self) -> list:
        """
        Читает аннотацию к датасету, возвращая список с путями к экземплярам и их метками классов.

        :return: Список путей к экземплярам с и их метками классов.
        """
        res = []
        try:
            with open(os.path.join(self._annotation_dir, 'annotation.csv'), 'r', newline='') as file:
                rows = csv.DictReader(file)
                for row in rows:
                    res.append([row[self.__header[0]], row[self.__header[1]], row[self.__header[2]]])
        except OSError as err:
            logging.warning(f' При попытке открытия аннотации по пути {self._annotation_dir} произошла ошибка:\n{err}.')
        return res


if __name__ == "__main__":
    for i in CLASSES:
        an = Annotation(os.path.join('dataset', i))
        an.create_for_class(i)
