"""
Модуль копирует файлы.
"""

import os
import shutil

from tqdm import tqdm


def copy_file_in_dir(list_dir: list, finish_dir: str) -> None:
    """
    Копируем файлы в директорию.
    list_dir - [root - путь к файлу, file - имя файла]
    finish_dir - куда сохранить файлы.
    """
    for root, file in tqdm(list_dir, ncols=80, desc='Copy'):
        path = os.path.join(root, file)
        copy_path = os.path.join(finish_dir, file)

        if os.path.isfile(copy_path):
            new_name = str(len(os.listdir(finish_dir))) + file
            copy_path = os.path.join(finish_dir, new_name)

        # Копируем файлы.
        shutil.copy2(path, copy_path)
