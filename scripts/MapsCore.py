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
        # Масштаб карты
        self.min_map_zoom: int = 0
        self.max_map_zoom: int = 21
        self.map_zoom: int = 12

        # Получение карты
        self.get_map_image()

    def get_map_image(self) -> None:
        """Получение и запись изображения карты из кэша в атрибут класса"""

        self.map_image: arcade.Texture = API.StaticMaps.get_map_image(
            Cacher.CACHE_PARAMS["MAP_IMAGE_FILE_NAME"], ll=LL, z=str(self.map_zoom)
        )

    # Методы arcade.Window
    def on_draw(self) -> None:
        self.clear()

        # Отрисовка карты
        arcade.draw_texture_rect(
            self.map_image, arcade.Rect(0, 0, 0, 0, self.width, self.height, self.width / 2, self.height / 2)
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        # Зум карты
        if key == arcade.key.PAGEUP or key == arcade.key.PAGEDOWN:
            delta_zoom: int = 1 if key == arcade.key.PAGEUP else -1
            if self.min_map_zoom <= self.map_zoom + delta_zoom <= self.max_map_zoom:
                self.map_zoom += delta_zoom
                self.get_map_image()
