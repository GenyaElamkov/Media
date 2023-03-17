import locale
import os
import shutil
from datetime import datetime


def create_directory(dir_name: str) -> None:
    """
    Создаём директорию.
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def get_dates(file_name: str) -> datetime:
    """
    Получаем дату с медия.
    """
    dt = os.path.getmtime(file_name)
    return datetime.fromtimestamp(dt)


def copy_file_in_dir(start_dir: str, finish_dir: str) -> None:
    """
    Копируем файлы в директорию.
    """
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = f"{root}{os.sep}{file}"
            shutil.copy2(path, finish_dir)
            print('True')


def main():
    start_path = r"C:\Users\User\Desktop\фото Еська"
    finish_path = r"C:\Users\User\Desktop\test"

    copy_file_in_dir(start_dir=start_path, finish_dir=finish_path)

    locale.setlocale(category=locale.LC_ALL, locale="Russian")

    os.chdir(finish_path)
    for root, dirs, files in os.walk(finish_path):
        for file in files:
            path = f"{root}{os.sep}{file}"
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
