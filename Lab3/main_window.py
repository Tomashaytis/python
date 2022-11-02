import os
import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QGridLayout, QWidget
from PyQt6.QtGui import QPixmap
from annotation import CLASSES, Annotation


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("lab-3")
        dataset_path = QFileDialog.getExistingDirectory(self, 'Введите путь к папке исходного датасета')
        src = QLabel(f'Исходный датасет:\n{dataset_path}', self)
        layout = QGridLayout()
        layout.addWidget(src, 0, 0)
        create_annotation_button = QPushButton("Сформировать аннотацию")
        create_annotation_button.setFixedSize(QSize(250, 50))
        layout.addWidget(create_annotation_button, 1, 0)
        copy_dataset_button = QPushButton("Скопировать датасет")
        copy_dataset_button.setFixedSize(QSize(250, 50))
        layout.addWidget(copy_dataset_button, 2, 0)
        copy_random_dataset_button = QPushButton("Рандомизировать датасет")
        copy_random_dataset_button.setFixedSize(QSize(250, 50))
        layout.addWidget(copy_random_dataset_button, 3, 0)
        next_tiger_button = QPushButton("Следующий тигр")
        next_tiger_button.setFixedSize(QSize(250, 50))
        layout.addWidget(next_tiger_button, 4, 0)
        next_leopard_button = QPushButton("Следующий леопард")
        next_leopard_button.setFixedSize(QSize(250, 50))
        layout.addWidget(next_leopard_button, 5, 0)
        an = Annotation(os.path.join(dataset_path, CLASSES[0]))
        cur_tiger = an.first_instance()[1]
        an = Annotation(os.path.join(dataset_path, CLASSES[1]))
        cur_leopard = an.first_instance()[1]
        label_image = QLabel('Здесь будет картинка')
        label_image.setPixmap(QPixmap(cur_tiger))
        layout.addWidget(label_image, 1, 1, 6, 2)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
