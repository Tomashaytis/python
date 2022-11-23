import pandas as pd
import numpy as np
import cv2
CLASSES = ["tiger", "leopard"]


def image_shapes(image_paths: pd.Series) -> tuple:
    """
    Функция находит ширину, высоту и количество каналов для каждого изображения в столбце
    image_paths, хранящего пути до них.

    :param image_paths: Столбец с путями до изображений.
    :return: Кортеж из 3 столбцов, хранящих ширину, высоту и количество каналов изображений.
    """
    width = []
    height = []
    channels = []
    for image_path in image_paths:
        image = cv2.imread(image_path)
        img_height, img_width, img_channels = image.shape
        width.append(img_width)
        height.append(img_height)
        channels.append(img_channels)
    return pd.Series(width), pd.Series(height), pd.Series(channels)


def class_mark_filter(df: pd.DataFrame, class_mark: str) -> pd.DataFrame:
    """
    Функция возвращает отфильтрованный по метке класса датафрейм.

    :param df: Датафрейм, который требуется отфильтровать.
    :param class_mark: Метка класса, по которой производится фильтрация.
    :return: Отфильтрованный датафрейм.
    """
    return df[df.class_mark == class_mark]


def multi_filter(df: pd.DataFrame, max_width: int, max_height: int, class_mark: str) -> pd.DataFrame:
    """
    Функция возвращает отфильтрованный по метке класса, максимальной высоте и ширине изображения датафрейм.
    Результатом будет датафрейм, состоящий из изображений, удовлетворяющих условиям:
    width <= max_width, height <= max_height, и метка класса соответствует заданной.

    :param df: Датафрейм, который требуется отфильтровать.
    :param max_width: Максимальная ширина изображения.
    :param max_height: Максимальная высота изображения.
    :param class_mark: Метка класса, по которой производится фильтрация.
    :return: Отфильтрованный датафрейм.
    """
    return df[((df.class_mark == class_mark) & (df.width <= max_width) & (df.height <= max_height))]


def grouper(df: pd.DataFrame) -> tuple:
    """
    Функция выполняет группировки датафрейма по метке класса, дополнительно вычисляя максимальное, минимальное
    и среднее значение по количеству пикселей. Возвращает кортеж из 3 получившихся группировок.

    :param df: Датафрейм, по которому строятся группировки.
    :return: Кортеж из 3 группировок: максимальное, минимальное и среднее количество пикселей изображения.
    """
    df['pixels'] = df['width'] * df['height'] * df['channels']
    return df.groupby('class_mark').max(), df.groupby('class_mark').min(), df.groupby('class_mark').mean()


def histograms(df: pd.DataFrame, class_mark: str) -> tuple:
    """
    Функция возвращает гистограммы по 3 каналам изображения, выбранного случайно из изображений,
    отфильтрованных по метке класса.

    :param df: Датафрейм, по изображению из которого будет строиться гистограмма.
    :param class_mark: Метка класса, по которой фильтруется датафрейм.
    :return: Кортеж из 3 списков (гистограмм).
    """
    df = class_mark_filter(df, class_mark)
    image_paths = df.absolute_path.to_numpy()
    image_path = np.random.choice(image_paths)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hist0 = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist1 = cv2.calcHist([image], [1], None, [256], [0, 256])
    hist2 = cv2.calcHist([image], [2], None, [256], [0, 256])
    return hist0, hist1, hist2


if __name__ == "__main__":
    instance_df = pd.read_csv('annotation.csv')
    instance_df.drop(['relative path'], axis=1, inplace=True)
    instance_df = instance_df.rename(columns={'absolute path': 'absolute_path', 'class': 'class_mark'})
    mask = (instance_df.class_mark == CLASSES[1])
    instance_df['numerical_class_mark'] = mask.astype(int)
    instance_df['width'], instance_df['height'], instance_df['channels'] = image_shapes(instance_df['absolute_path'])
    h0, h1, h2 = histograms(instance_df, CLASSES[0])
    print(h1)

