import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from PIL import Image
from sklearn.model_selection import train_test_split
from typing import Tuple, Any
import pickle

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

torch.manual_seed(1234)
if DEVICE == 'cuda':
    torch.cuda.manual_seed_all(1234)


def analysis_accuracy(accuracy_train: torch.tensor, accuracy_val: torch.tensor) -> None:
    plt.figure(figsize=(15, 5))
    plt.plot(range(len(accuracy_train)), accuracy_train, color="green")
    plt.plot(range(len(accuracy_val)), accuracy_val, color="red")
    plt.legend(["Train accuracy", "Valid accuracy"])
    plt.savefig(os.path.join('accuracy.png'))


def analysis_loss(train_loss: torch.tensor, valid_loss: torch.tensor) -> None:
    plt.figure(figsize=(15, 5))
    plt.plot(range(len(train_loss)), [float(value.detach()) for value in train_loss], color="blue")
    plt.plot(range(len(valid_loss)), [float(value.detach()) for value in valid_loss], color="orange")
    plt.legend(["Train loss", "Valid loss"])
    plt.savefig(os.path.join('loss.png'))


class PredatorDataset(Dataset):
    def __init__(self, image_paths: list, labels: list, transform: Any = None) -> None:
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, index: int) -> Tuple[torch.tensor, int]:
        path_to_image = self.image_paths[index]
        image = Image.open(path_to_image)
        image = self.transform(image.convert("RGB"))
        im_label = int(self.labels[index])
        return image, int(im_label)


class AlexNet(nn.Module):
    def __init__(self, num_classes: int):
        super(AlexNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=0),
            nn.BatchNorm2d(96),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(96, 256, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2))
        self.layer3 = nn.Sequential(
            nn.Conv2d(256, 384, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(384),
            nn.ReLU())
        self.layer4 = nn.Sequential(
            nn.Conv2d(384, 384, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(384),
            nn.ReLU())
        self.layer5 = nn.Sequential(
            nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2))
        self.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 5 * 5, 4096),
            nn.ReLU())
        self.fc1 = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU())
        self.fc2 = nn.Sequential(
            nn.Linear(4096, num_classes))

    def forward(self, x: torch.tensor) -> tuple:
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.fc1(out)
        out = self.fc2(out)
        return out


if __name__ == '__main__':
    dataset_dir = 'dataset'
    # Получение массива меток
    annotation = pd.read_csv('annotation.csv')
    annotation = annotation.rename(columns={'absolute path': 'absolute_path',
                                            'relative path': 'relative_path',
                                            'class': 'class_mark'})
    annotation = annotation.sort_values(by="absolute_path")
    class_marks = annotation["class_mark"]
    class_marks = class_marks.to_numpy()
    class_marks = class_marks == 'tiger'
    # Получение массива путей
    dataset_list = glob.glob(os.path.join(dataset_dir, '*.jpg'))
    # Деление на тренировочные, тестовые и валидационные данные
    x_train, x_test_val, y_train, y_test_val = train_test_split(dataset_list, class_marks, test_size=0.2, shuffle=True)
    x_test, x_val, y_test, y_val = train_test_split(x_test_val, y_test_val, test_size=0.5)
    print('Проверка выборок на сбалансированность')
    print(sum(y_train == 1), sum(y_train == 0))
    print(sum(y_test == 1), sum(y_test == 0))
    print(sum(y_val == 1), sum(y_val == 0))
    # Аугментации
    custom_transforms = transforms.Compose([transforms.ToTensor(),
                                            transforms.Resize((224, 224)),
                                            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                                            transforms.RandomResizedCrop(224),
                                            transforms.RandomHorizontalFlip()])
    # Создание датасетов
    predator_train = PredatorDataset(x_train, y_train, custom_transforms)
    predator_test = PredatorDataset(x_test, y_test, custom_transforms)
    with open('predator_test.pickle', 'wb') as f:
        pickle.dump(predator_test, f)
    predator_val = PredatorDataset(x_val, y_val, custom_transforms)
    # Инициализация модели и основных параметров
    model = AlexNet(num_classes=2).to(DEVICE)
    bach_size = 100
    lr = 0.005
    epochs = 17
    accuracy_values = []
    loss_values = []
    accuracy_values_val = []
    loss_values_val = []
    # Создание даталоадеров, инициализация функции потерь и оптимайзера
    train_dataloader = DataLoader(predator_train, batch_size=bach_size, shuffle=False)
    test_dataloader = DataLoader(predator_test, batch_size=bach_size, shuffle=False)
    val_dataloader = DataLoader(predator_val, batch_size=bach_size, shuffle=False)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=lr, weight_decay=0.005, momentum=0.9)
    # основной цикл
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        total = 0
        correct = 0

        for data, label in train_dataloader:
            if len(label) < bach_size:
                break
            data = data.to(DEVICE)
            label = label.to(DEVICE)

            output = model(data)
            loss = criterion(output, label)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            _, predicted = torch.max(output.data, 1)
            total += label.size(0)
            correct += (predicted == label).sum().item()
            epoch_loss += loss / len(train_dataloader)
            del data, label, output

        accuracy_values.append(correct / total)
        loss_values.append(epoch_loss)
        print('TRAIN: Epoch : {}, train accuracy : {}, train loss : {}'.format(epoch + 1, correct / total, epoch_loss))

        with torch.no_grad():
            val_loss = 0
            total = 0
            correct = 0
            for data, label in val_dataloader:
                if len(label) < bach_size:
                    break
                data = data.to(DEVICE)
                label = label.to(DEVICE)

                output = model(data)
                loss = criterion(output, label)

                _, predicted = torch.max(output.data, 1)
                total += label.size(0)
                correct += (predicted == label).sum().item()
                val_loss += loss / len(val_dataloader)
                del data, label, output
            accuracy_values_val.append(correct / total)
            loss_values_val.append(val_loss)
            print('VALID: Epoch : {}, valid accuracy : {}, valid loss : {}'.format(epoch + 1, correct / total, val_loss))
    # Сохранил модель и графики
    torch.save(model.state_dict(), 'model.pt')
    analysis_accuracy(accuracy_values, accuracy_values_val)
    analysis_loss(loss_values, loss_values_val)
