"""
Скрипт копирует фотографии в установленную папку.
Раскладывает по годам и месяцам.
Информацию берез из метаданных файла - время последней модификации
файла (дата создания).
"""

import locale
import os
import shutil
from datetime import datetime

from PIL import ExifTags
from PIL import Image


def copy_file_in_dir(start_dir: str, finish_dir: str) -> None:
    """
    Копируем файлы в директорию.
    """
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = f"{root}{os.sep}{file}"
            shutil.copy2(path, finish_dir)


def create_directory(dir_name: str) -> None:
    """
    Создаём директорию.
    """
    # if not os.path.exists(dir_name):
    #     os.makedirs(dir_name)
    dir_true = os.path.isdir(dir_name)
    if not dir_true:
        os.makedirs(dir_name)


def get_dates(file_name: str) -> datetime:
    """
    Получаем дату создания с файла.
    """
    dt = os.path.getmtime(file_name)
    return datetime.fromtimestamp(dt)


def get_metadates(file_name: str) -> str | None:
    """
    Получаем дату с метаданных файла.
    """
    with Image.open(file_name) as img:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img.getexif().items()
            if k in ExifTags.TAGS
        }
    return exif.get('DateTime')


def get_extensions(file_name: str) -> str:
    """
    Получаем расширения файлов.
    """
    return file_name.split('.')[-1].lower()


def _checking_metadata(file_name: str) -> bool:
    """
    Проверка файла на метаданные.
    """
    list_extensions = ['jpeg', 'png', 'jpg']
    return get_extensions(file_name=file_name) in list_extensions \
           and get_metadates(file_name=file_name) is not None


def main():
    start_path = r"C:\Users\User\Desktop\фото Еська"
    finish_path = r"C:\Users\User\Desktop\test"
    # Копируем файлы.
    copy_file_in_dir(start_dir=start_path, finish_dir=finish_path)

    locale.setlocale(category=locale.LC_ALL, locale="Russian")

    os.chdir(finish_path)

    for root, dirs, files in os.walk(finish_path):
        for file in files:
            path = f"{root}{os.sep}{file}"

            # Получаем метаданные с фото.
            metadates_true = _checking_metadata(file_name=path)
            if metadates_true:
                pattern = '%Y:%m:%d %H:%M:%S'
                dt = datetime.strptime(get_metadates(file_name=path), pattern)
                year = str(dt.year)
                month = dt.strftime("%B")
            else:
                year = get_dates(path).strftime("%Y")
                month = get_dates(path).strftime("%B")

            create_directory(year)
            os.chdir(f"{finish_path}{os.sep}{year}")

            create_directory(month)
            os.chdir(finish_path)

            try:
                shutil.move(file, f"{year}{os.sep}{month}{os.sep}{file}")
            except FileNotFoundError:
                print('[!] Файлов нет')


if __name__ == '__main__':
    main()
