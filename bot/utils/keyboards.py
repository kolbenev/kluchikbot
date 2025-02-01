"""
Модуль универсальных клавиатур.
"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def go_back_kb(callback_data: str) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="⬅ Вернутся назад", callback_data=callback_data),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
