"""Главный скрипт-соединитель приложения"""

# Работа с кэшом
from scripts.Cacher import Cacher
# Работа с графикой
import arcade
import arcade.gui
import data.styles.ui.light_theme as light_theme_style
import data.styles.ui.dark_theme as dark_theme_style
# Работа с API
from scripts.MapsAPI import API
# Математические расчёты
from math import cos


class Maps(arcade.Window, API):
    """Основной класс приложения"""

    def setup(self):
        self.theme = "light"

        self.setup_map()
        self.setup_ui()

    # Методы карты
    def setup_map(self) -> None:
        """Загрузка карты"""

        # Размер карты
        self.map_width, self.map_height = 650, 450

        # Масштаб карты
        self.min_map_z, self.max_map_z = 0, 21
        self.delta_map_z_coef = 1
        self.map_z = 12

        # Движение карты
        self.min_map_long, self.max_map_long = -180, 180
        self.min_map_lat, self.max_map_lat = -90, 90
        self.delta_map_ll_coef = 250
        self.map_long, self.map_lat = 37.617698, 55.755864

        # Метки карты
        self.map_pt = []
        self.map_pt_style = "pm2rdm"

        # Получение карты
        self.get_map_image()

    # Методы интерфейса
    def setup_ui(self) -> None:
        """Загрузка интерфейса"""

        self.ui_manager: arcade.gui.UIManager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Кнопка смены темы
        self.change_theme_button: arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(
            width=150, height=40, text="Change theme"
        )
        self.change_theme_button.on_click = lambda event: self.change_theme()
        self.ui_manager.add(self.change_theme_button)

        # Кнопка включения поиска почтового индекса
        self.postal_code_button: arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(
            width=150, height=40, text="On postal"
        )
        self.postal_code_button.on_click = lambda event: self.change_postal_code()
        self.postal_code_button.value_status = False
        self.ui_manager.add(self.postal_code_button)

        # Поле ввода текста для поиска
        self.search_input_text: arcade.gui.UIInputText = arcade.gui.UIInputText(
            width=200, height=40, font_size=16, text_color=(140, 140, 140)
        )
        self.ui_manager.add(self.search_input_text)

        # Кнопка для поиска
        self.search_button: arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(
            width=100, height=40, text="Search"
        )
        self.search_button.on_click = lambda event: self.search_toponym(self.search_input_text.text, True)
        self.ui_manager.add(self.search_button)

        # Кнопка для очистки результатов поиска
        self.clear_result_button: arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(
            width=75, height=40, text="Clear"
        )
        self.clear_result_button.on_click = lambda event: self.clear_result()
        self.ui_manager.add(self.clear_result_button)

        # Поле вывода адреса
        self.address_label: arcade.gui.UILabel = arcade.gui.UILabel(
            width=300, height=40, size_hint_max=(300, 40)
        )
        self.address_label.visible = False
        self.ui_manager.add(self.address_label)

        # Поле вывода почтового индекса
        self.postal_code_label: arcade.gui.UILabel = arcade.gui.UILabel(
            width=80, height=40, size_hint_max=(80, 40)
        )
        self.postal_code_label.visible = False
        self.ui_manager.add(self.postal_code_label)

        # Настройка расположения и стилей виджетов
        self.update_ui()

    def update_ui(self) -> None:
        """Обновление параметров UI под текущие параметры окна"""

        theme_style = light_theme_style if self.theme == "light" else dark_theme_style

        # Кнопка смены темы
        self.change_theme_button.right, self.change_theme_button.top = self.width - 10, self.height - 10
        self.change_theme_button.style = theme_style.ui_flat_button

        # Кнопка включения поиска почтового индекса
        self.postal_code_button.right, self.postal_code_button.top = (
            self.width - 10, self.change_theme_button.bottom - 10
        )
        self.postal_code_button.style = theme_style.ui_flat_button

        # Поле ввода текста для поиска
        self.search_input_text.left, self.search_input_text.top = 10, self.height - 10
        self.search_input_text.style = theme_style.ui_input_text
        # Меняем состояния для обновления стиля
        self.search_input_text.disabled = not self.search_input_text.disabled
        self.search_input_text.disabled = not self.search_input_text.disabled

        # Кнопка поиска
        self.search_button.left, self.search_button.top = self.search_input_text.right + 5, self.height - 10
        self.search_button.style = theme_style.ui_flat_button

        # Кнопка очистки результатов поиска
        self.clear_result_button.left, self.clear_result_button.top = self.search_button.right + 5, self.height - 10
        self.clear_result_button.style = theme_style.ui_flat_button

        # Поле вывода адреса
        self.address_label.left, self.address_label.top = 10, self.search_input_text.bottom - 10
        self.address_label.update_font(
            font_size=theme_style.ui_label["font_size"],
            font_color=theme_style.ui_label["text_color"]
        )
        self.address_label._bg_color = theme_style.ui_label["bg_color"]
        self.address_label._border_color = theme_style.ui_label["border_color"]
        self.address_label._border_width = theme_style.ui_label["border_width"]

        # Поле вывода почтового индекса
        self.postal_code_label.left, self.postal_code_label.top = self.address_label.right + 5, self.address_label.top
        self.postal_code_label.update_font(
            font_size=theme_style.ui_label["font_size"],
            font_color=theme_style.ui_label["text_color"]
        )
        self.postal_code_label._bg_color = theme_style.ui_label["bg_color"]
        self.postal_code_label._border_color = theme_style.ui_label["border_color"]
        self.postal_code_label._border_width = theme_style.ui_label["border_width"]

    def change_theme(self) -> None:
        """Изменение темы приложения (тёмная/светлая)"""

        self.theme = "light" if self.theme == "dark" else "dark"

        # Смена темы у всех объектов
        self.update_ui()
        self.get_map_image()

    def change_postal_code(self) -> None:
        """Включает/выключает отображение почтового индекса"""

        # Смена режима кнопки
        self.postal_code_button.value_status = not self.postal_code_button.value_status
        self.postal_code_button.text = f"{"Off" if self.postal_code_button.value_status else "On"} Postal"
        self.postal_code_label.visible = self.postal_code_button.value_status and self.address_label.visible

    def clear_result(self) -> None:
        """Очистка результатов поиска"""

        # Очистка данных о найденном топониме
        self.address_label.text = ""
        self.address_label.visible = False
        self.postal_code_label.text = ""
        self.postal_code_label.visible = False

        # Очистка меток на карте
        self.map_pt.clear()
        # Обновление карты
        self.get_map_image()

    # Запросы
    def get_map_image(self) -> None:
        """Получение и запись изображения карты из кэша в атрибут класса"""

        self.map_image: arcade.Texture = API.StaticMaps.get_map_image(
            Cacher.CACHE_PARAMS["MAP_IMAGE_FILE_NAME"],
            ll=f"{self.map_long},{self.map_lat}",
            z=str(self.map_z),
            pt="~".join(self.map_pt),
            size=f"{self.map_width},{self.map_height}",
            theme=self.theme
        )

    def search_toponym(self, geocode: str, move: bool) -> None:
        """Поиск топонима и указание на карте"""

        # Получение топонима
        toponym: dict | None = API.GeocodeMaps.get_toponym(
            geocode=geocode
        )
        if toponym:
            # Получение информации о топониме
            toponym_ll: str = API.GeocodeMaps.get_toponym_ll(toponym)
            toponym_address: str = API.GeocodeMaps.get_toponym_address(toponym)
            toponym_postal_code: str = API.GeocodeMaps.get_toponym_postal_code(toponym)

            # Вывод адреса
            self.address_label.text = toponym_address
            self.address_label.visible = True
            self.postal_code_label.text = toponym_postal_code if toponym_postal_code else "Почтовый ID отсутствует"
            self.postal_code_label.visible = self.postal_code_button.value_status

            if move:
                # Перемещение карты к топониму
                self.map_long, self.map_lat = map(float, toponym_ll.split(","))
            # Добавление метки на карту
            self.map_pt.clear()
            self.map_pt.append(f"{toponym_ll},{self.map_pt_style}")
            # Обновление карты
            self.get_map_image()
        else:
            self.search_input_text.text = "Адрес не найден"

    # Методы arcade.Window
    def on_draw(self) -> None:
        self.clear()

        # Отрисовка карты
        arcade.draw_texture_rect(
            self.map_image, arcade.Rect(0, 0, 0, 0, self.width, self.height, self.width / 2, self.height / 2)
        )

        # Отрисовка интерфейса
        self.ui_manager.draw()

    def on_resize(self, width: int, height: int) -> None:
        # Изменение положения интерфейса
        self.update_ui()

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

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Расчёт разницы между центром и кликом мыши в пикселях
            size_diff_x, size_diff_y = self.map_width / self.width, self.map_height / self.height
            delta_x, delta_y = (x - self.width / 2) * size_diff_x, (y - self.height / 2) * size_diff_y

            # Расчёт широты координат клика мыши
            coef_lat = 180 / 2 ** (self.map_z + 8)
            mouse_click_lat = self.map_lat + delta_y * coef_lat
            # Расчёт долготы координат клика мыши
            coef_long = cos(0) * 360 / 2 ** (self.map_z + 8)
            mouse_click_long = self.map_long + delta_x * coef_long

            # Поиск объекта по координатам клика
            self.search_toponym(f"{mouse_click_long},{mouse_click_lat}", False)
