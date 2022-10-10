import csv
import os
from typing import List


# классы
# обработка исключений
# типы
# class Create: - создаёт аннотацию, итераторы
class ClassManager:
    _dir: str

    def __init__(self, cur_dir=os.getcwd()) -> None:
        self._dir = cur_dir

    def create_annotation(self) -> None:
        # Исключение
        file = open(os.path.join(self._dir, 'annotation.csv'), 'w', newline='')
        columns = ['absolute path', 'relative path', 'class']
        class_folders = []
        for root, dirs, files in os.walk(self._dir):
            for class_name in dirs:
                class_folder = {'absolute path': os.path.abspath(class_name),
                                'relative path': os.path.join(self._dir, class_name),
                                'class': class_name}
                class_folders.append(class_folder)
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(class_folders)
        file.close()

    def read_annotation(self) -> List:
        filename = os.path.join(self._dir, 'annotation.csv')
        file = open(filename, 'r', newline='')
        rows = csv.DictReader(file)
        res = []
        for row in rows:
            res.append([row['absolute path'], row['relative path'], row['class']])
        file.close()
        return res


if __name__ == "__main__":
    cm = ClassManager('lab1')
    cm.create_annotation()
    a = cm.read_annotation()
    for i in a:
        print(i)
