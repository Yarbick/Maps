# Работа с графикой
import arcade.gui
# Работа с классами
from dataclasses import dataclass

# Стандартные стили для всей темы
DEFAULT_BUTTON_STYLE = {
    "normal": arcade.gui.UIFlatButton.UIStyle(
        bg=(0, 200, 120),
        border_width=0,
        font_size=16,
        font_color=(255, 255, 255)
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        bg=(0, 220, 132),
        border_width=0,
        font_size=16,
        font_color=(255, 255, 255)
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        bg=(0, 240, 144),
        border_width=0,
        font_size=16,
        font_color=(255, 255, 255)
    ),
    "disabled": arcade.gui.UIFlatButton.UIStyle(
        bg=(0, 255, 150),
        border_width=0,
        font_size=16,
        font_color=(220, 220, 220)
    )
}

uiflatbutton = DEFAULT_BUTTON_STYLE
