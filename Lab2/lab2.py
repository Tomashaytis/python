import csv
import os
from typing import List
# классы
# обработка исключений
# типы
# class Create: - создаёт аннотацию, итераторы


def create_annotation(directory: str) -> None:
    file = open(os.path.join(directory, 'annotation.csv'), 'w', newline='')
    columns = ['absolute path', 'relative path', 'class']
    class_folders = []
    for root, dirs, files in os.walk(directory):
        for class_name in dirs:
            class_folder = {'absolute path': os.path.abspath(class_name),
                            'relative path': os.path.join(directory, class_name),
                            'class': class_name}
            class_folders.append(class_folder)
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(class_folders)
    file.close()


def read_annotation(directory: str) -> List:
    filename = os.path.join(directory, 'annotation.csv')
    file = open(filename, 'r', newline='')
    rows = csv.DictReader(file)
    res = []
    for row in rows:
        res.append(row['absolute path'])
        res.append(row['relative path'])
        res.append(row['class'])
    file.close()
    return res


if __name__ == "__main__":
    create_annotation('dataset')
    a = read_annotation('dataset')
    for i in a:
        print(i)
