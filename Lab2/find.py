import os
from typing import Optional
import re


def next_exemplar(current_exemplar_path: str) -> Optional[str]:
    if not os.path.exists(current_exemplar_path):
        raise FileExistsError(f'Файл по пути {current_exemplar_path} не существует.')
    cur_dir, old_filename = os.path.split(current_exemplar_path)
    ex_number = re.search(r'\d{4}', old_filename)
    ex_number = ex_number.group(0) if ex_number is not None else '0'
    while int(ex_number) < 10000:
        ex_number = f'{(int(ex_number) + 1):04d}'
        new_filename = os.path.join(cur_dir, re.sub(r'\d{4}', ex_number, old_filename))
        if os.path.exists(new_filename):
            return new_filename
    return None


if __name__ == "__main__":
    print(next_exemplar('dataset\\tiger\\0111.jpg'))
    print(next_exemplar('dataset1\\tiger_0023.jpg'))
    print(next_exemplar('who\\9997.jpg'))
