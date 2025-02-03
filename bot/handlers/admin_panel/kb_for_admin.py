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


admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Количество пользователей")],
        [KeyboardButton(text="Количество пользователей с маркой авто")],
        [KeyboardButton(text="Сделать рассылку по авто")],
        [KeyboardButton(text="/make_sending")],
        [KeyboardButton(text="/make_sending_with_photo")],
        [KeyboardButton(text="/deleteadmin")],
        [KeyboardButton(text="/getadminlog")],
    ],
    resize_keyboard=True,
)
