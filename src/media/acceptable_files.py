"""
Модуль фильтрует файлы.
"""
import os


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
