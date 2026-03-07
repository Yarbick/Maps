"""Главный скрипт-соединитель приложения"""

# Работа с кэшом
from scripts.Cacher import Cacher
# Работа с графикой
import arcade
# Работа с API
from scripts.MapsAPI import API

# Временные константы (будут получаться при работе приложения в будущем)
LL, SPN = "37.617698,55.755864", "1,1"


class Maps(arcade.Window, API):
    """Основной класс приложения"""

    def setup(self):
        # Получение карты
        self.get_map_image(LL, SPN)

    def get_map_image(self, ll: str, spn: str) -> None:
        """Получение и запись изображения карты из кэша в атрибут класса"""

        self.map_image: arcade.Texture = API.StaticMaps.get_map_image(
            Cacher.CACHE_PARAMS["MAP_IMAGE_FILE_NAME"], ll, spn
        )

    # Методы arcade.Window
    def on_draw(self) -> None:
        self.clear()

        # Отрисовка карты
        arcade.draw_texture_rect(
            self.map_image, arcade.Rect(0, 0, 0, 0, self.width, self.height, self.width / 2, self.height / 2)
        )
