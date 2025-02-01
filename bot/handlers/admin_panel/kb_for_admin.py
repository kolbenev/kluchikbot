"""
Модуль клавиатур администратора.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_admin_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Меню обработки заказов"),
        ],
        [
            KeyboardButton(text="Меню ответов на сообщения"),
        ],
        [KeyboardButton(text="Количество сообщений от пользователей")],
        [KeyboardButton(text="Количество новых заказов")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Отмена"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard


def check_report_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Ответить ✅"), KeyboardButton(text="Удалить ❌")],
        [KeyboardButton(text="Выйти")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        input_field_placeholder="Выберите действие:",
        resize_keyboard=True,
    )
    return keyboard


def check_order_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Ответить ✅"), KeyboardButton(text="Удалить ❌")],
        [KeyboardButton(text="Выйти")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        input_field_placeholder="Выберите действие:",
        resize_keyboard=True,
    )
    return keyboard
