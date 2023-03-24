# -*- codng: utf8 -*-
import sys
import os
from art import *

from main import start_main

Art = text2art("media", font='block',
               chr_ignore=True)
print(Art)

txt_description = """
Этот скрипт раскладывает файлы (фото, видео) по директориям.
Файлы (фото, видео) хранятся в созданной директории.
Имя директории: NewFolder + текущая дата.
"""

print(txt_description)

txt_warning = """
Разместите скрипт в корне директории, где хотите отфильтровать.
В корне директории файлы должны находится в директориях (папках)
"""
print(txt_warning)


def main():
    start = input('Запустить скрипт (Y/N): ').upper()
    st_key = ('N', 'Н')

    os.system('cls')

    if start in st_key:
        sys.exit('Good by!')

    print('[Скрипт запущен]')
    start_main()
    print('[Скрипт закончил работу]')


if __name__ == '__main__':
    main()
