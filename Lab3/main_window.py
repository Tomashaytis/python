import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        dataset_path = QFileDialog.getExistingDirectory(self, 'Введите путь к папке исходного датасета')
        lbl1 = QLabel(f'Текущий исходный датасет: {dataset_path}', self)
        lbl1.setFixedSize(QSize(400, 50))
        lbl1.move(10, 0)
        h_box = QVBoxLayout()
        h_box.addStretch(1)
        change_dataset_button = QPushButton("Изменить исходный датасет")
        change_dataset_button.setFixedSize(QSize(200, 100))
        h_box.addWidget(change_dataset_button)
        copy_dataset_button = QPushButton("Скопировать датасет")
        copy_dataset_button.setFixedSize(QSize(200, 100))
        h_box.addWidget(copy_dataset_button)
        copy_random_dataset_button = QPushButton("Рандомизировать датасет")
        copy_random_dataset_button.setFixedSize(QSize(200, 100))
        h_box.addWidget(copy_random_dataset_button)
        central_widget = QWidget()
        central_widget.setLayout(h_box)
        self.setFixedSize(QSize(500, 500))
        self.setCentralWidget(central_widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
