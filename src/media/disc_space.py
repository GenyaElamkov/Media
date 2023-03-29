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


def show_difference_disk(files_name: list[tuple],
                         start_path: str) -> None:
    """
    Получаем разницу в гб между оставшимся местом и используемым в файлах.
    """
    usage = get_folder_usage(files_name)
    free = disk_usage(start_path).free
    resoult = free - usage

    # Байт в мегабайте.
    mb = 1048576
    largest_space = 0

    if resoult <= largest_space:
        input(f'[!] Мало места, нужно {usage / mb:.0f} мб. '
              f'Для выхода нажмите <Enter>...')
        sys.exit()
    else:
        print(f'Используются места: {usage / mb:.0f} мб')
