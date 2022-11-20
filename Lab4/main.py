import pandas as pd
import cv2


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


if __name__ == "__main__":
    instance_df = pd.read_csv('annotation.csv')
    instance_df.drop(['relative path'], axis=1, inplace=True)
    instance_df = instance_df.rename(columns={'absolute path': 'absolute_path', 'class': 'class_mark'})
    mask = (instance_df.class_mark == 'leopard')
    instance_df['numerical_class_mark'] = mask.astype(int)
    instance_df['width'], instance_df['height'], instance_df['channels'] = image_shapes(instance_df['absolute_path'])
    print(instance_df['width'])
