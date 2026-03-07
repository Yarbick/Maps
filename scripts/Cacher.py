"""Кэшировщик"""

# Работа с файлами
import os
from json import loads as json_loads
from shutil import rmtree


class Cacher:
    """Класс для работы с кэшом"""

    CACHE_PARAMS: dict

    @staticmethod
    def init_cache():
        """Инициализация кэша"""

        # Загрузка параметров кэша
        with open("data/cache_params.json", mode="r", encoding="UTF-8") as file:
            Cacher.CACHE_PARAMS = json_loads(file.read())

        # Создание папки с кэшом
        os.mkdir(Cacher.CACHE_PARAMS["CACHE_DIR"])

    @staticmethod
    def clean_cache() -> None:
        """Очистка всего кэша приложения"""

        # Удаление всех кэшированных файлов
        rmtree(Cacher.CACHE_PARAMS["CACHE_DIR"])

    @staticmethod
    def create_cache_path(path: str):
        """Создание пути к файлу в кэше"""

        return os.path.join(Cacher.CACHE_PARAMS["CACHE_DIR"], path)

    class CacheFile:
        """Класс для работы с отдельными файлами кэша"""

        @staticmethod
        def write_cache_file(file_name: str, data) -> None:
            """Запись данных в кэшированный файл"""

            # Создание пути к файлу
            cache_path = Cacher.create_cache_path(file_name)

            # Запись в файл
            with open(cache_path, mode="wb") as file:
                file.write(data)

        @staticmethod
        def load_cache_file(file_name: str):
            """Загрузка данных в байтах из кэшированного файла"""

            # Создание пути к файлу
            cache_path = Cacher.create_cache_path(file_name)

            # Чтение из файла
            with open(cache_path, mode="rb") as file:
                return file.read()
