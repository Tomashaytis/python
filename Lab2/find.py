import os
from typing import Optional
import re


def next_instance(current_instance_path: str) -> Optional[str]:
    """
    Возвращает следующий экземпляр класса на основе предыдущего (current_instance_path).
    Если экземпляры закончились, вернёт None.

    :param current_instance_path: Путь к текущему экземпляру класса.
    :return: Следующий экземпляр класса или None (если они закончились).
    """
    if not os.path.exists(current_instance_path):
        raise FileExistsError(f'Файл по пути {current_instance_path} не существует.')
    cur_dir, old_filename = os.path.split(current_instance_path)
    instance_number = re.search(r'\d{4}', old_filename)
    instance_number = int(instance_number.group(0)) if instance_number is not None else 0
    while instance_number < 10000:
        instance_number += 1
        new_filename = os.path.join(cur_dir, re.sub(r'\d{4}', f'{instance_number:04d}', old_filename))
        if os.path.exists(new_filename):
            return new_filename
    return None


if __name__ == "__main__":
    print(next_instance('dataset\\tiger\\0111.jpg'))
    print(next_instance('dataset1\\tiger_0023.jpg'))
    print(next_instance('who\\0050.jpg'))
