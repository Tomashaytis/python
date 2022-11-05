import os
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QGridLayout, QWidget
from PyQt6.QtGui import QPixmap
from annotation import Annotation
from iterator import InstanceIterator
from dataset_replication import copy_dataset
from dataset_random import random_dataset

CLASSES = ["tiger", "leopard"]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("lab-3")
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Введите путь к папке исходного датасета')
        src = QLabel(f'Исходный датасет:\n{self.dataset_path}', self)
        layout = QGridLayout()
        layout.addWidget(src, 0, 0)
        create_annotation_button = QPushButton("Сформировать аннотацию")
        create_annotation_button.setFixedSize(QSize(250, 50))
        create_annotation_button.clicked.connect(self.create_annotation)
        layout.addWidget(create_annotation_button, 1, 0)
        copy_dataset_button = QPushButton("Скопировать датасет")
        copy_dataset_button.setFixedSize(QSize(250, 50))
        copy_dataset_button.clicked.connect(self.dataset_copy)
        layout.addWidget(copy_dataset_button, 2, 0)
        copy_random_dataset_button = QPushButton("Рандомизировать датасет")
        copy_random_dataset_button.setFixedSize(QSize(250, 50))
        copy_random_dataset_button.clicked.connect(self.dataset_random)
        layout.addWidget(copy_random_dataset_button, 3, 0)
        self.next_tiger_button = QPushButton("Следующий тигр")
        self.next_tiger_button.setFixedSize(QSize(250, 50))
        self.next_tiger_button.clicked.connect(self.next_tiger)
        layout.addWidget(self.next_tiger_button, 4, 0)
        self.next_leopard_button = QPushButton("Следующий леопард")
        self.next_leopard_button.setFixedSize(QSize(250, 50))
        self.next_leopard_button.clicked.connect(self.next_leopard)
        layout.addWidget(self.next_leopard_button, 5, 0)
        self.label_image = QLabel('Здесь будет картинка')
        self.label_image.setMinimumSize(QSize(500, 300))
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_image, 1, 1, 6, 2)
        if not (os.path.exists(os.path.join(self.dataset_path, CLASSES[0])) or
                os.path.exists(os.path.join(self.dataset_path, CLASSES[1]))):
            create_annotation_button.setEnabled(False)
            copy_dataset_button.setEnabled(False)
            copy_random_dataset_button.setEnabled(False)
            self.next_tiger_button.setEnabled(False)
            self.next_leopard_button.setEnabled(False)
            self.label_image.setText('Ошибка!\n'
                                     'В исходном датасете отсутствует одна из папок классов: "tiger" или "leopard"')
        else:
            an = Annotation(os.path.join(self.dataset_path, CLASSES[0]))
            self.cur_tiger = InstanceIterator(an.first_instance()[1])
            an = Annotation(os.path.join(self.dataset_path, CLASSES[1]))
            self.cur_leopard = InstanceIterator(an.first_instance()[1])
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()

    def create_annotation(self):
        when_dir = QFileDialog.getExistingDirectory(self, 'Введите путь к папке, в которой будет создана аннотация')
        for cls in CLASSES:
            an = Annotation(os.path.join(self.dataset_path, cls), when_dir)
            an.add_from_old_annotation()
            an.create_for_class(cls)

    def dataset_copy(self):
        when_dir = QFileDialog.getExistingDirectory(self, 'Введите путь к папке, в которую будет скопирован датасет')
        for cls in CLASSES:
            copy_dataset(os.path.join(self.dataset_path, cls), when_dir)

    def dataset_random(self):
        when_dir = QFileDialog.getExistingDirectory(self, 'Введите путь к папке, в которую будет скопирован датасет')
        for cls in CLASSES:
            copy_dataset(os.path.join(self.dataset_path, cls), when_dir)
        random_dataset(when_dir)

    def next_tiger(self):
        self.label_image.setPixmap(QPixmap(self.cur_tiger.__iter__()))
        try:
            self.cur_tiger.__next__()
        except StopIteration:
            self.label_image.setText("Тигры закончились")
            self.next_tiger_button.setEnabled(False)

    def next_leopard(self):
        self.label_image.setPixmap(QPixmap(self.cur_leopard.__iter__()))
        try:
            self.cur_leopard.__next__()
        except StopIteration:
            self.label_image.setText("Леопарды закончились")
            self.next_leopard_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
