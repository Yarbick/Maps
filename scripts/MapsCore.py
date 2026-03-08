"""Главный скрипт-соединитель приложения"""

# Работа с кэшом
from scripts.Cacher import Cacher
# Работа с графикой
import arcade
# Работа с API
from scripts.MapsAPI import API


class Maps(arcade.Window, API):
    """Основной класс приложения"""

    def setup(self):
        # Масштаб карты
        self.min_map_z, self.max_map_z = 0, 21
        self.delta_map_z_coef = 1
        self.map_z = 12

        # Движение карты
        self.min_map_long, self.max_map_long = -180, 180
        self.min_map_lat, self.max_map_lat = -90, 90
        self.delta_map_ll_coef = 250
        self.map_long, self.map_lat = 37.617698, 55.755864

        # Получение карты
        self.get_map_image()

    def get_map_image(self) -> None:
        """Получение и запись изображения карты из кэша в атрибут класса"""

        self.map_image: arcade.Texture = API.StaticMaps.get_map_image(
            Cacher.CACHE_PARAMS["MAP_IMAGE_FILE_NAME"],
            ll=f"{self.map_long},{self.map_lat}",
            z=str(self.map_z)
        )

    # Методы arcade.Window
    def on_draw(self) -> None:
        self.clear()

        # Отрисовка карты
        arcade.draw_texture_rect(
            self.map_image, arcade.Rect(0, 0, 0, 0, self.width, self.height, self.width / 2, self.height / 2)
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        map_changed = False  # Флаг для обновления карты только при наличии изменений

        # Зум карты
        if key == key == arcade.key.PAGEUP and self.map_z + self.delta_map_z_coef <= self.max_map_z:
            self.map_z += self.delta_map_z_coef
            map_changed = True
        if key == key == arcade.key.PAGEDOWN and self.map_z - self.delta_map_z_coef >= self.min_map_z:
            self.map_z -= self.delta_map_z_coef
            map_changed = True

        # Движение карты
        delta_map_long = self.delta_map_ll_coef * (2 ** -self.map_z)
        if key == arcade.key.LEFT and self.map_long - delta_map_long >= self.min_map_long:
            self.map_long -= delta_map_long
            map_changed = True
        if key == arcade.key.RIGHT and self.map_long + delta_map_long <= self.max_map_long:
            self.map_long += delta_map_long
            map_changed = True

        delta_map_lat = delta_map_long * 0.5
        if key == arcade.key.DOWN and self.map_lat - delta_map_lat >= self.min_map_lat:
            self.map_lat -= delta_map_lat
            map_changed = True
        if key == arcade.key.UP and self.map_lat + delta_map_lat <= self.max_map_lat:
            self.map_lat += delta_map_lat
            map_changed = True

        # Обновление карты
        if map_changed:
            self.get_map_image()
