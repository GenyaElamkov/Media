"""
Скрипт копирует фотографии в установленную папку (NewFolder).
Раскладывает по годам и месяцам.
Информацию берез из метаданных файла: дата съемки.
Если отсутствует дата съемки, то время последней модификации
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
    # TODO: Не копирует файлы с одинаковыми именами.
    os.chdir(start_dir)
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = os.path.join(root, file)
            try:
                shutil.copy2(path, finish_dir)
            except shutil.SameFileError:
                print('Копия')


def create_directory(dir_name: str) -> None:
    """
    Создаём директорию.
    """
    dir_true = os.path.isdir(dir_name)
    if not dir_true:
        os.mkdir(dir_name)


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
    start_path = r"C:\Users\User\Desktop\фото_Еська"
    # start_path = input("Скопируйте сюда путь к фото: ")
    # Текущая директория.
    # start_path = os.getcwd()
    os.chdir(start_path)

    # Директория куда складываем файлы.
    finish_dir = 'NewFolder'
    create_directory(finish_dir)

    # Путь куда складываем файлы.
    finish_path = os.path.join(start_path, finish_dir)
    # Копируем файлы.
    copy_file_in_dir(start_dir=start_path, finish_dir=finish_path)

    locale.setlocale(category=locale.LC_ALL, locale="Russian")

    os.chdir(finish_path)

    for root, dirs, files in os.walk("."):
        for file in files:
            path = os.path.join(root, file)
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
            os.chdir(year)

            create_directory(month)
            os.chdir('..')

            try:
                shutil.move(file, os.path.join(year, month, file))
            except FileNotFoundError:
                print('[!] Файл перенесен')


if __name__ == '__main__':
    main()
