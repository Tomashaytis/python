import os
from typing import Optional
from annotation import Annotation


def next_instance(current_instance_path: str) -> Optional[str]:
    """
    Возвращает следующий экземпляр класса на основе предыдущего (current_instance_path).
    Если экземпляры закончились, вернёт None.

    :param current_instance_path: Путь к текущему экземпляру класса.
    :return: Следующий экземпляр класса или None (если они закончились).
    """
    if not os.path.exists(current_instance_path):
        raise FileExistsError(f'Файл по пути {current_instance_path} не существует.')
    an = Annotation(os.path.split(current_instance_path)[0], os.path.split(current_instance_path)[0])
    instances = an.read()
    for inst in range(len(instances) - 1):
        if instances[inst][1] == os.path.relpath(current_instance_path):
            return instances[inst + 1][1]
    return None
