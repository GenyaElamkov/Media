import locale
import os
import shutil
import sys
from datetime import datetime

from PIL import ExifTags
from PIL import Image
from PIL import UnidentifiedImageError
from tqdm import tqdm

from src import clear
from src import start_path

from src.media.description import fileNotFoundError, directory_exists


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
    excep = ['exe', 'psd', 'thm']
    return get_extensions(file_name) in excep


def get_list_acceptable_files(start_dir: str) -> list[tuple]:
    """
    Получаем список разрешенных файлов.
    :return [root - путь к файлу, file - имя файла]
    """
    arr = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if not _set_except_extensions(file):
                arr.append((root, file))
    return arr


def copy_file_in_dir(list_dir: list, finish_dir: str) -> None:
    """
    Копируем файлы в директорию.
    list_dir - [root - путь к файлу, file - имя файла]
    finish_dir - куда сохранить файлы.
    """
    for root, file in tqdm(list_dir, ncols=80, desc='Copy'):
        path = os.path.join(root, file)
        copy_path = os.path.join(finish_dir, file)

        if os.path.isfile(copy_path):
            new_name = str(len(os.listdir(finish_dir))) + file
            copy_path = os.path.join(finish_dir, new_name)

        # Копируем файлы.
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


def _checking_metadata(file_name: str) -> bool:
    """
    Проверка файла на метаданные.
    list_extensions - список расширений для метаданных.
    """
    list_extensions = ['jpeg', 'png', 'jpg']
    return get_extensions(file_name=file_name) in list_extensions \
           and get_metadates(file_name=file_name) is not None


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
                print(fileNotFoundError)


start_path_file_name = get_list_acceptable_files(start_dir=start_path)


def start_main() -> None:
    # Текущая директория.
    # start_path = r"C:\Users\User\Desktop\test"
    # start_path = os.getcwd()

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
    # start_path_file_name = get_list_acceptable_files(start_dir=start_path)
    copy_file_in_dir(list_dir=start_path_file_name, finish_dir=finish_path)
    # Перемещаем файлы.
    move_file(finish_path)


if __name__ == '__main__':
    start_main()
