from train import AlexNet, PredatorDataset, DEVICE
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import pickle

if __name__ == '__main__':
    # Загрузка данных
    bach_size = 100
    criterion = nn.CrossEntropyLoss()
    with open('predator_test.pickle', 'rb') as f:
        predator_test = pickle.load(f)
    test_dataloader = DataLoader(predator_test, batch_size=bach_size, shuffle=True)
    # Загрузка модели
    new_model = AlexNet(num_classes=2).to(DEVICE)
    new_model.load_state_dict(torch.load("alexnet.pt"))
    # Тест модели на тренировочных данных и визуализация её работы
    new_model.eval()
    test_loss = 0
    total = 0
    correct = 0
    first = True
    for data, label in test_dataloader:
        if len(label) < bach_size:
            break
        data = data.to(DEVICE)
        label = label.to(DEVICE)
        output = new_model(data)

        loss = criterion(output, label)

        _, predicted = torch.max(output.data, 1)
        total += label.size(0)
        correct += (predicted == label).sum().item()
        test_loss += loss / len(test_dataloader)
        predicted = predicted.numpy()
        if first:
            plt.figure(figsize=(15, 15))
            for i in range(12):
                plt.subplot(3, 4, i + 1)
                plt.title("leopard" if predicted[i] == 0 else "tiger")
                plt.axis('off')
                plt.imshow(data[i].permute(1, 2, 0).numpy()[:, :, ::-1])
            plt.show()
            first = False
        del data, label, output
    print('TEST: test accuracy: {}, test loss: {}'.format(correct / total, float(test_loss)))