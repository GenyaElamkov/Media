"""
Модуль создаёт директории по года и месяцам.
Переносит файлы в созданные директории.
"""

import locale
import os
import shutil
from datetime import datetime

from PIL import ExifTags
from PIL import Image
from PIL import UnidentifiedImageError
from tqdm import tqdm

from src.media.acceptable_files import get_extensions
from src.media.description import fileNotFoundError


def get_metadates(file_name: str) -> str | None:
    """
    Получаем дату метаданных файла.
    """
    try:
        with Image.open(file_name) as img:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in img.getexif().items()
                if k in ExifTags.TAGS
            }
        return exif.get('DateTime')
    except UnidentifiedImageError:
        return None


def checking_metadata(file_name: str) -> bool:
    """
    Проверка файла на метаданные.
    list_extensions - список расширений для метаданных.
    """
    list_extensions = ['jpeg', 'png', 'jpg']
    return get_extensions(file_name=file_name) in list_extensions \
           and get_metadates(file_name=file_name) is not None


def get_dates(file_name: str) -> datetime:
    """
    Получаем дату создания файла.
    """
    dt = os.path.getmtime(file_name)
    return datetime.fromtimestamp(dt)


def create_directory(dir_name: str) -> None:
    """
    Создаём директорию.
    """
    dir_true = os.path.isdir(dir_name)
    if not dir_true:
        os.mkdir(dir_name)


def move_file(finish_path: str) -> None:
    """
    Создаём директории по годам и месяцам.
    Перемещаем файлы в созданные директории.
    """
    os.chdir(finish_path)

    locale.setlocale(category=locale.LC_ALL, locale="Russian")
    pattern = '%Y:%m:%d %H:%M:%S'

    for root, dirs, files in os.walk("."):
        for file in tqdm(files, ncols=80, desc='Move'):
            # Получаем метаданные с фото.
            metadates_true = checking_metadata(file_name=file)
            if metadates_true:
                dt = datetime.strptime(get_metadates(file_name=file), pattern)
                year = str(dt.year)
                month = dt.strftime("%B")
            else:
                year = get_dates(file).strftime("%Y")
                month = get_dates(file).strftime("%B")

            create_directory(year)
            os.chdir(year)

            create_directory(month)
            os.chdir('..')

            # Перемещаем копированные файлы в созданные директорий.
            try:
                shutil.move(file, os.path.join(year, month, file))
            except FileNotFoundError:
                print(fileNotFoundError)
