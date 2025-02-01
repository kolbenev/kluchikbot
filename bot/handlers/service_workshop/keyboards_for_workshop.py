"""
Клавиатура меню мастерской.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_workshop_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="🏠 Изготовление ключей для дома", callback_data="keys_for_home"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🚗 Изготовление автоключей", callback_data="keys_for_cars"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔑 Изготовление автоключа с чипом",
                callback_data="keys_for_car_with_chip",
            )
        ],
        [
            InlineKeyboardButton(
                text="🔥 Чипы для автозапуска", callback_data="chip_for_autostart"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 Ремонт пультов и брелоков",
                callback_data="repair_controls_and_key",
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙ Пайка и восстановление плат",
                callback_data="soldering_and_restoration_of_boards",
            )
        ],
        [
            InlineKeyboardButton(
                text="🔒 Калибровка иммобилайзера",
                callback_data="immobilizer_calibration",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅ Вернутся назад",
                callback_data="main_menu",
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def leave_an_application() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="💬 Оставить заявку", callback_data="make_order"),
        ],
        [
            InlineKeyboardButton(text="⬅ Вернутся назад", callback_data="workshop"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def leave_an_application_with_car() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="💬 Оставить заявку", callback_data="make_order_with_car"
            ),
        ],
        [
            InlineKeyboardButton(text="⬅ Вернутся назад", callback_data="workshop"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
