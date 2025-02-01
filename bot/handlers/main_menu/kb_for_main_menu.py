"""
Модуль клавиатур главного меню.
"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="🔑 Мастерская", callback_data="workshop"),
        ],
        [
            InlineKeyboardButton(text="🎉 Акции", callback_data="discount"),
            InlineKeyboardButton(text="💰 Бонусы", callback_data="bonuses"),
            InlineKeyboardButton(text="🤖 Smart-ключи", callback_data="smart_keys"),
        ],
        [
            InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def contats_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="Связь с администратором", callback_data="report_from_user"
            ),
        ],
        [
            InlineKeyboardButton(text="⬅ Вернутся назад", callback_data="main_menu"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
