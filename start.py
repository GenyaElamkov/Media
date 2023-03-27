# -*- codng: utf8 -*-
"""
Раскладывает файлы (фото, видео) по годам и месяцам.

Этот скрипт раскладывает файлы (фото, видео) по директориям:
- Создает основную директорию (NewFolder_data).
    Где data создания этой директории.
- Копирует файлы в эту директорию.
- Вытаскивает из файлов год и месяц (дата съемки или дата создания).
- Создает в директории (NewFolder_data) директории (год)
    и в директории (год) создает (месяц).
- Копированные файлы переносит по созданным директориям.

--Warning--
Разместите скрипт в корне директории.
В корне директории файлы должны находится в директориях (папках)
"""

import sys

from colorama import init, Style, Fore

from src import clear
from src.description import txt_description, txt_warning, Art
from src.main import start_main

from src.disc_space import difference_place_disk_free

init()

print(Fore.GREEN + Art)
print(txt_description)
print(Fore.RED + txt_warning + Style.RESET_ALL)


def main():
    print(Fore.YELLOW)
    difference_place_disk_free()
    print(Style.RESET_ALL)

    start = input('Запустить скрипт (Y/N)(Д/Н): ').upper()

    clear()

    st_key = ('Y', 'Д')
    if start not in st_key:
        input(Fore.YELLOW + f'[!] Вы нажали клавишу: <<{start}>>')
        sys.exit('Good by!')

    print(Fore.YELLOW + '[Скрипт запущен]')

    start_main()

    print('[Скрипт закончил работу]')


if __name__ == '__main__':
    main()
