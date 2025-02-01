"""
Модуль клавиатур смарт-ключей.
"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def smart_keys_main_menu() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="📝 Описание Smart-ключей и наших преимуществ",
                callback_data="smart_key_description",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔧 Программирование Smart-ключа",
                callback_data="smart_key_programming",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Полная утеря Smart-ключа",
                callback_data="lost_smart_key",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅ Обратно в меню",
                callback_data="main_menu"
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def make_application_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="💬 Оставить заявку", callback_data="make_order"
            ),
        ],
        [
            InlineKeyboardButton(text="⬅ Вернутся назад", callback_data="smart_keys"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard