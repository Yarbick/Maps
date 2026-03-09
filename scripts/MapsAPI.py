"""Работа с API"""

# Работа с файлами и ОС
import os
from dotenv import load_dotenv
from sys import exit as sys_exit
# Работа с кэшом
from scripts.Cacher import Cacher
# Графика
import arcade
# Работа с API
import requests

# Загрузка переменных окружения из .env файла
load_dotenv(".env")


class API:
    """Класс для работы с API"""

    class Base:
        """Класс макетов для работы с API"""

        class Response:
            """Класс с методами для работы с запросами"""

            @staticmethod
            def get(server_address: str, params: dict) -> requests.Response:
                """Стандартный GET-запрос"""

                try:
                    # Запрос
                    response: requests.Response = requests.get(server_address, params=params)

                    if response:  # Выдача результата при верном запросе
                        return response
                    else:  # Вызов ошибки при неверном запросе
                        API.Base.Response.call_error(response)
                except requests.exceptions.ConnectionError:
                    # Вывод ошибки
                    print("Подключение к интернету отсутствует")

                    # Завершение работы
                    sys_exit(1)

            @staticmethod
            def call_error(response: requests.Response) -> None:
                """Вызов ошибки"""

                # Вывод ошибки
                print(response.url)
                print(f"Status code: {response.status_code} ({response.reason})")

                # Завершение работы
                sys_exit(1)

    class StaticMaps:
        """Класс для работы с API сервиса static-maps.yandex.ru"""

        @staticmethod
        def get_map_image(file_name: str, **params) -> arcade.Texture:
            """Готовый метод для получения изображения карты"""

            # Запрос
            response = API.StaticMaps.Response.get(**params)
            # Сохранение изображения в кэш
            Cacher.CacheFile.write_cache_file(file_name, response.content)
            # Загрузка изображения из кэша
            map_image: arcade.Texture = API.StaticMaps.AnswerProcessing.load_map_image(file_name)

            return map_image

        class Response:
            """Класс с методами для работы с запросами"""

            @staticmethod
            def get(**params) -> requests.Response:
                """Static-maps GET-запрос"""

                # Параметры запроса
                server_address = "https://static-maps.yandex.ru/v1"
                params["apikey"] = params.get("apikey", os.getenv("STATIC_MAPS_APIKEY"))

                # Запрос
                response: requests.Response = API.Base.Response.get(server_address, params=params)

                return response

        class AnswerProcessing:
            """Класс для обработки ответов из запросов"""

            @staticmethod
            def load_map_image(file_name: str) -> arcade.Texture:
                """Загрузка изображения карты Static-maps"""

                map_image: arcade.Texture = arcade.load_texture(Cacher.create_cache_path(file_name))

                return map_image

    class GeocodeMaps:
        """Класс для работы с API сервиса geocode-maps.yandex.ru"""

        @staticmethod
        def get_toponym(**params) -> dict | None:
            """Готовый метод для получения топонима"""

            # Запрос
            response: requests.Response = API.GeocodeMaps.Response.get(**params)
            # Получение топонима
            toponym: dict = API.GeocodeMaps.AnswerProcessing.get_toponym(response)

            return toponym

        @staticmethod
        def get_toponym_ll(toponym: dict) -> str:
            """Готовый метод для получения координат топонима"""

            # Получение координат
            toponym_ll: str = API.GeocodeMaps.AnswerProcessing.get_toponym_ll(toponym)

            return toponym_ll

        class Response:
            """Класс с методами для работы с запросами"""

            @staticmethod
            def get(**params) -> requests.Response:
                """GeocodeMaps GET-запрос"""

                # Параметры запроса
                server_address = "https://geocode-maps.yandex.ru/v1"
                params["apikey"] = params.get("apikey", os.getenv("GEOCODE_MAPS_APIKEY"))
                params["format"] = params.get("format", "json")

                # Запрос
                response: requests.Response = API.Base.Response.get(server_address, params=params)

                return response

        class AnswerProcessing:
            """Класс для обработки ответов из запросов"""

            @staticmethod
            def get_toponym(response: requests.Response) -> dict | None:
                """Получение топонима из запроса"""

                json_response = response.json()

                try:
                    toponym: dict = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

                    return toponym
                except IndexError:
                    return None

            @staticmethod
            def get_toponym_ll(toponym: dict) -> str:
                """Получение координат топонима в виде <долгота,широта>"""

                toponym_ll: str = ",".join(toponym["Point"]["pos"].split())

                return toponym_ll
