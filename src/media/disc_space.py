"""
Определяем место на жёстком диске.
Определяем сколько занимает места файлы.
Определяем сколько нужна места для файлов.
Выводим предупреждение, если места не хватает.
"""
import os
import sys
from shutil import disk_usage


def get_folder_usage(files: list[tuple]) -> int:
    """
    Возращает количество байтов в директориях, где лежат файлы.
    """
    size = 0
    for root, file in files:
        path = os.path.join(root, file)
        size += os.stat(path).st_size
    return size


def get_disk_usage(path: str) -> int:
    return disk_usage(path).free


def difference_place_disk_free(files_name: list[tuple],
                               start_path: str) -> None:
    """
    Получаем разницу в гб между оставшимся местом и используемым в файлах.
    """

    usage = get_folder_usage(files_name)
    free = get_disk_usage(start_path)
    resoult = free - usage

    # gb = 2 ** 30
    # Байт в мегабайте.
    mb = 1048576
    largest_space = 0

    if resoult <= largest_space:
        input(f'[!] Мало места, нужно {usage / mb:.0f} мб')
        sys.exit()
    else:
        print(f'Используются места: {usage / mb:.0f} мб')
