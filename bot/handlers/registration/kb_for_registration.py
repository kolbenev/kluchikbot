"""
Модуль с клавиатурами регистрации.
"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def agree_disagree_kb_with_treaty() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="Согласен", callback_data="agree_to_process"),
        ],
        [
            InlineKeyboardButton(
                text="Несогласен", callback_data="disagree_to_process"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Соглашение на обработку персональных данных",
                callback_data="personal_data",
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def agree_disagree_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="Согласен", callback_data="agree_to_process"),
        ],
        [
            InlineKeyboardButton(
                text="Несогласен", callback_data="disagree_to_process"
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def send_contact_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Поделится номером", request_contact=True),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard
