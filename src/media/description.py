"""
Текстовый модуль.
"""

from art import text2art

Art = text2art("media", font='block',
               chr_ignore=True)

txt_description = """Этот скрипт раскладывает файлы (фото, видео) по директориям.
Файлы (фото, видео) хранятся в созданной директории.
Имя директории: NewFolder + текущая дата.
"""

txt_warning = """Внимание: Разместите скрипт в корне директории, где хотите отфильтровать.
В корне директории файлы должны находится в директориях (папках)"""

start = 'Запустить скрипт (Y/N)(Д/Н): '

fileNotFoundError = '[!] Файл перенесен'

directory_exists = '[!] Директория существует'
