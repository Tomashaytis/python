import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QGridLayout, QWidget
from PyQt6.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        dataset_path = QFileDialog.getExistingDirectory(self, 'Введите путь к папке исходного датасета')
        src = QLabel(f'Текущий исходный датасет: {dataset_path}', self)
        src.setFixedSize(QSize(400, 20))
        layout = QGridLayout()
        layout.addWidget(src, 0, 1)
        copy_dataset_button = QPushButton("Скопировать датасет")
        copy_dataset_button.setFixedSize(QSize(200, 50))
        layout.addWidget(copy_dataset_button, 3, 5)
        copy_random_dataset_button = QPushButton("Рандомизировать датасет")
        copy_random_dataset_button.setFixedSize(QSize(200, 50))
        layout.addWidget(copy_random_dataset_button, 4, 5)
        next_tiger_button = QPushButton("Следующий тигр")
        next_tiger_button.setFixedSize(QSize(200, 50))
        layout.addWidget(next_tiger_button, 5, 0)
        next_leopard_button = QPushButton("Следующий леопард")
        next_leopard_button.setFixedSize(QSize(200, 50))
        layout.addWidget(next_leopard_button, 5, 2)
        label_image = QLabel('Здесь будет картинка')
        label_image.setFixedSize(QSize(500, 400))
        layout.addWidget(label_image, 1, 0, 4, 4)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
