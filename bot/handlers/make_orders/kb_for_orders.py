"""
Клавиатуры для формирования заказов.
"""

from typing import List

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from database.models import CarUser


def stage_photo() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="У меня нет фото 😢", callback_data="no_photo"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Обратно в меню", callback_data="main_menu"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def new_car_or_back_to_menu_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="Добавить новое авто", callback_data=""),
        ],
        [
            InlineKeyboardButton(text="⬅️ Обратно в меню", callback_data="main_menu"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def button_with_car_user(cars: List[CarUser]) -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=car.info_about_car)] for car in cars]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
