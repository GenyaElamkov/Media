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
from src.media.disc_space import show_difference_disk
from src.media.move_files import create_directory, move_file


def clear() -> None:
    """
    Обновляем экран.
    """
    os.system('cls')


def core(start_path: str, files_name: list[tuple]) -> None:
    """
    Собирает все модули.
    """
    # Директория куда складываем файлы.
    dts_now = datetime.now().date().strftime('%d.%m.%Y')
    finish_dir = 'NewFolder' + f"_{dts_now}"
    os.chdir(start_path)

    # Проверяем на существование основной директории.
    if os.path.isdir(finish_dir):
        clear()
        input(directory_exists)
        sys.exit()

    create_directory(finish_dir)

    finish_path = os.path.join(start_path, finish_dir)
    # Копируем файлы.
    copy_file_in_dir(list_dir=files_name, finish_dir=finish_path)
    # Перемещаем файлы.
    move_file(finish_path)


def show_window() -> None:
    # Текущая директория.
    start_path = os.getcwd()

    init()

    print(Fore.GREEN + Art)
    print(txt_description)
    print(Fore.RED + txt_warning + Style.RESET_ALL)

    # Список файлов.
    files_name = get_list_acceptable_files(start_dir=start_path)
    # Показывает, сколько места занимают файлы.
    print(Fore.YELLOW)
    show_difference_disk(files_name=files_name, start_path=start_path)
    print(Style.RESET_ALL)

    start = input('Запустить скрипт (Y/N)(Д/Н): ').upper()

    clear()

    st_key = ('Y', 'Д')
    if start not in st_key:
        input(Fore.YELLOW + f'[!] Вы нажали клавишу: <<{start}>>. '
                            f'Для выхода нажмите <Enter>...')
        sys.exit('Good by!')

    print(Fore.YELLOW + '[Скрипт запущен]')

    core(start_path=start_path, files_name=files_name)

    print('[Скрипт закончил работу]')


def main() -> None:
    show_window()


if __name__ == '__main__':
    main()
