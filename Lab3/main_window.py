import logging
import os
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
from annotation import Annotation
from iterator import InstanceIterator
from dataset_replication import copy_dataset
from dataset_random import random_dataset

CLASSES = ["tiger", "leopard"]


class MainWindow(QMainWindow):
    """
    Класс реализует графический интерфейс для работы с функциями из 2 лабораторной.
    """
    dataset_path: str
    label_image: QLabel

    def __init__(self):
        """
        Инициализация класса MainWindow.
        """
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """
        Функция инициализирует графический интерфейс приложения.
        От пользователя запрашивается путь к исходному датасету.

        :return: Нет возвращаемого значения.
        """
        self.setWindowTitle("Dataset Manager")
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Введите путь к папке исходного датасета')
        src = QLabel(f'Исходный датасет:\n{self.dataset_path}', self)
        v_box1 = QVBoxLayout()
        v_box1.addStretch(1)
        v_box1.addWidget(src)
        create_annotation_button = self.new_button(v_box1, "Сформировать аннотацию", 250, 50)
        copy_dataset_button = self.new_button(v_box1, "Скопировать датасет", 250, 50)
        copy_random_dataset_button = self.new_button(v_box1, "Рандомизировать датасет", 250, 50)
        next_tiger_button = self.new_button(v_box1, "Следующий тигр", 250, 50)
        next_leopard_button = self.new_button(v_box1, "Следующий леопард", 250, 50)
        self.label_image = QLabel('Нажмите кнопку "Следующий тигр" или "Следующий леопард".')
        self.label_image.setMinimumSize(QSize(500, 300))
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box2 = QVBoxLayout()
        v_box2.addStretch(1)
        v_box2.addWidget(self.label_image)
        if not (os.path.exists(os.path.join(self.dataset_path, CLASSES[0])) or
                os.path.exists(os.path.join(self.dataset_path, CLASSES[1]))):
            create_annotation_button.setEnabled(False)
            copy_dataset_button.setEnabled(False)
            copy_random_dataset_button.setEnabled(False)
            next_tiger_button.setEnabled(False)
            next_leopard_button.setEnabled(False)
            self.label_image.setText('Ошибка!\n'
                                     'В исходном датасете отсутствует одна из папок классов: "tiger" или "leopard."')
        else:
            an = Annotation(os.path.join(self.dataset_path, CLASSES[0]))
            cur_tiger = InstanceIterator(an.first_instance()[1])
            an = Annotation(os.path.join(self.dataset_path, CLASSES[1]))
            cur_leopard = InstanceIterator(an.first_instance()[1])
            next_tiger_button.clicked.connect(lambda cur_inst=cur_tiger, button=next_tiger_button,
                                              class_mark=CLASSES[0]:
                                              self.next_instance(cur_tiger, next_tiger_button, CLASSES[0]))
            next_leopard_button.clicked.connect((lambda cur_inst=cur_tiger, button=next_leopard_button,
                                                 class_mark=CLASSES[0]:
                                                 self.next_instance(cur_leopard, next_leopard_button, CLASSES[1])))
        create_annotation_button.clicked.connect(self.create_annotation)
        copy_dataset_button.clicked.connect(self.dataset_copy)
        copy_random_dataset_button.clicked.connect(self.dataset_random)
        central_widget = QWidget()
        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addLayout(v_box1)
        h_box.addLayout(v_box2)
        central_widget.setLayout(h_box)
        central_widget.setFixedSize(775, 325)
        self.setCentralWidget(central_widget)
        self.show()

    @staticmethod
    def new_button(v_box: QVBoxLayout, button_name: str, width: int, height: int) -> QPushButton:
        """
        Функция создаёт кнопу с заданной шириной и высотой, размещая её в сетке.

        :param v_box: V-бокс, в который добавляется кнопка.
        :param button_name: Текстовое содержимое кнопки.
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :return: Нет возвращаемого значения.
        """
        button = QPushButton(button_name)
        button.setFixedSize(QSize(width, height))
        v_box.addWidget(button)
        return button

    def create_annotation(self) -> None:
        """
        Функция создаёт аннотацию исходного датасета, реагируя на нажатие кнопки "Сформировать аннотацию".
        Пользователь должен выбрать путь к папке-назначения для файла-аннотации.

        :return: Нет возвращаемого значения.
        """
        when_dir = QFileDialog.getExistingDirectory(self, 'Введите путь к папке, в которой будет создана аннотация')
        if not when_dir:
            return
        for cls in CLASSES:
            an = Annotation(os.path.join(self.dataset_path, cls), when_dir)
            an.add_from_old_annotation()
            an.create_for_class(cls)

    def dataset_copy(self) -> None:
        """
        Функция копирует экземпляры исходного датасета, реагируя на нажатие кнопки "Скопировать датасет".
        Пользователь должен выбрать путь к папке-назначения, в которую будет скопирован датасет.

        :return: Нет возвращаемого значения.
        """
        when_dir = QFileDialog.getExistingDirectory(self, 'Введите путь к папке, в которую будет скопирован датасет')
        if not when_dir:
            return
        for cls in CLASSES:
            copy_dataset(os.path.join(self.dataset_path, cls), when_dir)

    def dataset_random(self) -> None:
        """
        Функция копирует экземпляры исходного датасета, реагируя на нажатие кнопки "Рандомизировать датасет".
        Пользователь должен выбрать путь к папке-назначения, в которую будет скопирован датасет.
        Каждый экземпляр будет иметь случайный номер от 0000 до 9999.

        :return: Нет возвращаемого значения.
        """
        when_dir = QFileDialog.getExistingDirectory(self, 'Введите путь к папке, в которую будет скопирован датасет')
        if not when_dir:
            return
        for cls in CLASSES:
            copy_dataset(os.path.join(self.dataset_path, cls), when_dir)
        random_dataset(when_dir)

    def next_instance(self, cur_inst: InstanceIterator, button: QPushButton, class_mark: str) -> None:
        """
        Функция меняет текущее содержание метки Label на изображение экземпляра с классом class_mark,
        реагируя на нажатие кнопки button.
        Если изображения закончатся - оповестит об этом.

        :param cur_inst: Итератор для класса.
        :param button: Кнопка, на нажатие которой реагирует функция.
        :param class_mark: Метка класса.
        :return: Нет возвращаемого значения.
        """
        self.label_image.setPixmap(QPixmap(cur_inst.__iter__()))
        try:
            cur_inst.__next__()
        except StopIteration:
            self.label_image.setText(f"Экземпляры класса {class_mark} закончились.")
            button.setEnabled(False)
        except OSError as err:
            logging.warning(f'При работе итератора была вызвана ошибка:\n{err}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
