# Работа с кэшом
from scripts.Cacher import Cacher
# Работа с графикой
import arcade
# Приложение
from scripts.MapsCore import Maps

# Константы окна
TITLE: str = "Maps"
SCREEN_WIDTH: int = 648
SCREEN_HEIGHT: int = 448


def main() -> None:
    # Инициализация кэша
    Cacher.init_cache()

    try:
        # Окно
        maps = Maps(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, resizable=True)
        maps.set_minimum_size(390, 270)
        maps.set_maximum_size(975, 675)
        maps.setup()

        # Запуск
        arcade.run()
    finally:
        # Очистка кэша
        Cacher.clean_cache()


if __name__ == "__main__":
    main()
