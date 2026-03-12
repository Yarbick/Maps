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
            toponym: dict | None = API.GeocodeMaps.AnswerProcessing.get_toponym(response)

            return toponym

        @staticmethod
        def get_toponym_ll(toponym: dict) -> str:
            """Готовый метод для получения координат топонима"""

            # Получение координат
            toponym_ll: str = API.GeocodeMaps.AnswerProcessing.get_toponym_ll(toponym)

            return toponym_ll

        @staticmethod
        def get_toponym_address(toponym: dict) -> str:
            """Готовый метод для получения адреса топонима"""

            # Получение адреса
            toponym_address: str = API.GeocodeMaps.AnswerProcessing.get_toponym_address(toponym)

            return toponym_address

        @staticmethod
        def get_toponym_postal_code(toponym: dict) -> str:
            """Готовый метод для получения почтового индекса топонима"""

            # Получение почтового индекса
            toponym_postal_code: str = API.GeocodeMaps.AnswerProcessing.get_toponym_postal_code(toponym)

            return toponym_postal_code

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

            @staticmethod
            def get_toponym_address(toponym: dict) -> str:
                """Получение адреса топонима"""

                toponym_address: str = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

                return toponym_address

            @staticmethod
            def get_toponym_postal_code(toponym: dict) -> str | None:
                """Получение адреса топонима"""

                try:
                    toponym_postal_code: str = (
                        toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                    )

                    return toponym_postal_code
                except KeyError:
                    return None

    class SearchMaps:
        """Класс для работы с API сервиса search-maps.yandex.ru"""

        @staticmethod
        def get_organization(**params) -> dict | None:
            """Готовый метод для получения организации"""

            # Запрос
            response: requests.Response = API.SearchMaps.Response.get(**params)
            # Получение топонима
            organization: dict | None = API.SearchMaps.AnswerProcessing.get_organization(response)

            return organization

        @staticmethod
        def get_organization_id(organization: dict) -> str:
            """Готовый метод для ID организации"""

            # Получение координат организации
            organization_id: str = API.SearchMaps.AnswerProcessing.get_organization_id(organization)

            return organization_id

        @staticmethod
        def get_organization_ll(organization: dict) -> str:
            """Готовый метод для получения координат организации"""

            # Получение координат организации
            organization_ll: str = API.SearchMaps.AnswerProcessing.get_organization_ll(organization)

            return organization_ll

        @staticmethod
        def get_organization_address(organization: dict) -> str:
            """Готовый метод для получения адреса организации"""

            # Получение адреса организации
            organization_address: str = API.SearchMaps.AnswerProcessing.get_organization_address(organization)

            return organization_address

        @staticmethod
        def get_organization_name(organization: dict) -> str:
            """Готовый метод для получения имени организации"""

            # Получение имени организации
            organization_name: str = API.SearchMaps.AnswerProcessing.get_organization_name(organization)

            return organization_name

        @staticmethod
        def get_organization_categories(organization: dict) -> list | None:
            """Готовый метод для получения категорий организации"""

            # Получение имени организации
            organization_categories: list | None = (
                API.SearchMaps.AnswerProcessing.get_organization_categories(organization))

            return organization_categories

        @staticmethod
        def get_organization_phones(organization: dict) -> list | None:
            """Готовый метод для получения номеров телефонов организации"""

            # Получение имени организации
            organization_phones: list | None = API.SearchMaps.AnswerProcessing.get_organization_phones(organization)

            return organization_phones

        @staticmethod
        def get_organization_postal_code(organization: dict) -> str:
            """Готовый метод для получения почтового индекса организации"""

            # Получение почтового индекса организации
            organization_postal_code: str = API.SearchMaps.AnswerProcessing.get_organization_postal_code(organization)

            return organization_postal_code

        class Response:
            """Класс с методами для работы с запросами"""

            @staticmethod
            def get(**params) -> requests.Response:
                """SearchMaps GET-запрос"""

                # Параметры запроса
                server_address = "https://search-maps.yandex.ru/v1"
                params["apikey"] = params.get("apikey", os.getenv("SEARCH_MAPS_APIKEY"))
                params["lang"] = params.get("lang", "ru_RU")
                params["type"] = params.get("type", "biz")

                # Запрос
                response: requests.Response = API.Base.Response.get(server_address, params=params)

                return response

        class AnswerProcessing:
            """Класс для обработки ответов из запросов"""

            @staticmethod
            def get_organization(response: requests.Response) -> dict | None:
                """Получение организации из запроса"""

                json_response = response.json()

                # Получение координат точки центра и запроса
                for param in response.url.split("&"):
                    if param.split("=")[0] == "ll":
                        center_long, center_lat = map(float, param.split("=", 1)[1].split("%2C"))

                        break

                # Получение ближайшей организации
                organizations: dict = json_response["features"]
                for organization in organizations:
                    # Расчёт дистанции между центральной точкой и организации
                    organization_long, organization_lat = organization["geometry"]["coordinates"]
                    distant = ((organization_long - center_long) ** 2 + (organization_lat - center_lat) ** 2) ** 0.5

                    if distant * 11100 <= 50:
                        return organization
                return None

            @staticmethod
            def get_organization_id(organization: dict) -> str:
                """Получение ID организации"""

                organization_id: str = organization["properties"]["CompanyMetaData"]["id"]

                return organization_id

            @staticmethod
            def get_organization_ll(organization: dict) -> str:
                """Получение координат организации"""

                organization_ll: str = ",".join(map(str, organization["geometry"]["coordinates"]))

                return organization_ll

            @staticmethod
            def get_organization_address(organization: dict) -> str:
                """Получение адреса организации"""

                organization_address: str = organization["properties"]["CompanyMetaData"]["address"]

                return organization_address

            @staticmethod
            def get_organization_name(organization: dict) -> str:
                """Получение имени организации"""

                organization_name: str = organization["properties"]["CompanyMetaData"]["name"]

                return organization_name

            @staticmethod
            def get_organization_categories(organization: dict) -> list | None:
                """Получение категорий организации"""

                try:
                    organization_categories: list = [
                        category["name"]
                        for category in organization["properties"]["CompanyMetaData"]["Categories"]
                    ]

                    return organization_categories
                except KeyError:
                    return None

            @staticmethod
            def get_organization_phones(organization: dict) -> list | None:
                """Получение номеров телефонов организации"""

                try:
                    organization_phones: list = [
                        phone["formatted"]
                        for phone in organization["properties"]["CompanyMetaData"]["Phones"]
                    ]

                    return organization_phones
                except KeyError:
                    return None

            @staticmethod
            def get_organization_postal_code(organization: dict) -> str | None:
                """Получение почтового индекса организации"""

                try:
                    organization_postal_code: str = (
                        organization["properties"]["CompanyMetaData"]["Address"]["postal_code"]
                    )

                    return organization_postal_code
                except KeyError:
                    return None
