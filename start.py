# -*- codng: utf8 -*-
import os
import sys

from art import *
from colorama import init, Style, Fore

from src.main import start_main

init()

Art = text2art("media", font='block',
               chr_ignore=True)
print(Fore.GREEN + Art)

txt_description = """Этот скрипт раскладывает файлы (фото, видео) по директориям.
Файлы (фото, видео) хранятся в созданной директории.
Имя директории: NewFolder + текущая дата.
"""

print(txt_description)

txt_warning = """Внимание: Разместите скрипт в корне директории, где хотите отфильтровать.
В корне директории файлы должны находится в директориях (папках)
"""
print(Fore.RED + txt_warning + Style.RESET_ALL)


def main():
    start = input('Запустить скрипт (Y/N)(Д/Н): ').upper()

    os.system('cls')

    st_key = ('N', 'Н')
    if start in st_key:
        sys.exit('Good by!')

    print(Fore.YELLOW + '[Скрипт запущен]')

    start_main()

    print('[Скрипт закончил работу]')
    input('Для выхода нажмите любую клавишу')

if __name__ == '__main__':
    main()
