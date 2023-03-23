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

--Help--
Разместите скрипт в корне директории.
В корне директории файлы должны находится в директориях (папках)
"""

import locale
import os
import shutil
import sys
from datetime import datetime

from PIL import ExifTags
from PIL import Image
from tqdm import tqdm

def create_directory(dir_name: str) -> None:
    """
    Создаём директорию.
    """
    dir_true = os.path.isdir(dir_name)
    if not dir_true:
        os.mkdir(dir_name)


def get_extensions(file_name: str) -> str:
    """
    Получаем расширения файлов.
    """
    return file_name.split('.')[-1].lower()


def _set_except_extensions(file_name) -> bool:
    """
    Устанавливаем исключения для расширений.
    Расширения в этом списке не копируются.
    """
    excep = ['exe', 'psd']
    return get_extensions(file_name) in excep


def progress_bar() -> None:
    """
    Показываем прогресс бар.
    """

def test(start_dir: str) -> list:
    for root, dirs, files in os.walk(start_dir):
        arr_file = [file for file in files if not _set_except_extensions(file)]

    return arr_file

def copy_file_in_dir(start_dir: str, finish_dir: str) -> None:
    """
    Копируем файлы в директорию.
    """
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = os.path.join(root, file)
            copy_path = os.path.join(finish_dir, file)

            if os.path.isfile(copy_path):
                new_name = str(len(os.listdir(finish_dir))) + file
                copy_path = os.path.join(finish_dir, new_name)

            # Проверяем на расширения из списка исключений.
            if not _set_except_extensions(file):
                shutil.copy2(path, copy_path)


def get_dates(file_name: str) -> datetime:
    """
    Получаем дату создания файла.
    """
    dt = os.path.getmtime(file_name)
    return datetime.fromtimestamp(dt)


def get_metadates(file_name: str) -> str | None:
    """
    Получаем дату метаданных файла.
    """
    with Image.open(file_name) as img:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img.getexif().items()
            if k in ExifTags.TAGS
        }
    return exif.get('DateTime')


def _checking_metadata(file_name: str) -> bool:
    """
    Проверка файла на метаданные.
    list_extensions - список расширений для метаданных.
    """
    list_extensions = ['jpeg', 'png', 'jpg']
    return get_extensions(file_name=file_name) in list_extensions \
           and get_metadates(file_name=file_name) is not None


def work(start_path: str, finish_path: str) -> None:
    # Копируем файлы.
    test(start_dir=start_path)
    copy_file_in_dir(start_dir=start_path, finish_dir=finish_path)


    locale.setlocale(category=locale.LC_ALL, locale="Russian")
    pattern = '%Y:%m:%d %H:%M:%S'

    os.chdir(finish_path)

    for root, dirs, files in os.walk("."):
        for file in files:
            # Получаем метаданные с фото.
            metadates_true = _checking_metadata(file_name=file)
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
                print('[!] Файл перенесен')


def main() -> None:
    # Текущая директория.
    # Тестовый путь
    start_path = r"C:\Users\User\Desktop\фото_Еська"
    # Путь для pruduct.
    # start_path = os.getcwd()
    os.chdir(start_path)

    # Директория куда складываем файлы.
    dts_now = datetime.now().date().strftime('%d.%m.%Y')
    finish_dir = 'NewFolder' + f"_{dts_now}"
    # Проверяем на существование основной директории.
    finish_dir_true = os.path.isdir(finish_dir)
    if finish_dir_true:
        sys.exit('[!] Директория существует')

    create_directory(finish_dir)

    finish_path = os.path.join(start_path, finish_dir)

    work(start_path, finish_path)


if __name__ == '__main__':
    main()
