"""
Модуль запуска.
"""

import os
import sys
from datetime import datetime

from colorama import init, Style, Fore

from src.media.acceptable_files import get_list_acceptable_files
from src.media.copy_files import copy_file_in_dir
from src.media.description import directory_exists
from src.media.description import txt_description, txt_warning, Art
from src.media.disc_space import difference_place_disk_free
from src.media.move_files import create_directory, move_file

clear = lambda: os.system('cls')
# Текущая директория.
start_path = r"C:\Users\User\Desktop\test"

# start_path = os.getcwd()
path_file_name = get_list_acceptable_files(start_dir=start_path)


def collecting() -> None:
    # Директория куда складываем файлы.
    dts_now = datetime.now().date().strftime('%d.%m.%Y')
    finish_dir = 'NewFolder' + f"_{dts_now}"
    os.chdir(start_path)

    # Проверяем на существование основной директории.
    finish_dir_true = os.path.isdir(finish_dir)
    if finish_dir_true:
        clear()
        input(directory_exists)
        sys.exit()

    create_directory(finish_dir)

    finish_path = os.path.join(start_path, finish_dir)
    # Копируем файлы.

    copy_file_in_dir(list_dir=path_file_name, finish_dir=finish_path)
    # Перемещаем файлы.
    move_file(finish_path)


def start_window():
    init()

    print(Fore.GREEN + Art)
    print(txt_description)
    print(Fore.RED + txt_warning + Style.RESET_ALL)

    print(Fore.YELLOW)
    difference_place_disk_free(files_name=path_file_name,
                               start_path=start_path)
    print(Style.RESET_ALL)

    start = input('Запустить скрипт (Y/N)(Д/Н): ').upper()

    clear()

    st_key = ('Y', 'Д')
    if start not in st_key:
        input(Fore.YELLOW + f'[!] Вы нажали клавишу: <<{start}>>')
        sys.exit('Good by!')

    print(Fore.YELLOW + '[Скрипт запущен]')

    collecting()

    print('[Скрипт закончил работу]')


if __name__ == '__main__':
    start_window()
