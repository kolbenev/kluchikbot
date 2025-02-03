"""
Клавиатуры для формирования заказов.
"""

popular_car = {
    "Toyota": ["Crown", "Wish", "Alphard", "Prius", "Land Cruiser", "RAV4", "Passo"],
    "Honda": ["Fit", "Stepwgn", "CR-V", "Accord", "Freed", "Airwave", "Vezel"],
    "Nissan": ["X-Trail", "Serena", "Note", "Tiida", "Leaf", "Dualis"],
    "Mitsubishi": ["Pajero", "Delica", "Outlander", "Lancer", "Ek-Wagon"],
    "Mazda": ["CX-5", "Atenza", "Demio", "Alexa"],
    "Subaru": ["Forester", "Legacy", "Impreza", "Outback", "Levorg"],
    "Suzuki": ["Jimny", "Swift", "Escudo", "Solio"],
    "Daihatsu": ["Mira", "Tanto", "Move", "Hijet", "Rocky"],
    "Lada": ["Granta", "Vesta", "Niva", "Largus", "XRAY"],
    "Kia": ["Rio", "Sportage", "Seltos", "Cerato", "Optima"],
    "Hyundai": ["Creta", "Solaris", "Tucson", "Santa Fe", "Elantra"],
    "Volkswagen": ["Polo", "Tiguan", "Passat", "Golf", "Touareg"],
    "Skoda": ["Octavia", "Rapid", "Kodiaq", "Yeti", "Fabia"],
    "Renault": ["Logan", "Duster", "Sandero", "Kaptur", "Arkana"],
    "BMW": ["3 Series", "5 Series", "X5", "X3", "X6"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "S-Class", "GLE"],
    "Audi": ["A4", "A6", "Q5", "Q7", "A3"],
    "Ford": ["Focus", "Mondeo", "Kuga", "EcoSport", "Explorer"],
    "Chevrolet": ["Niva", "Cruze", "Aveo", "Orlando", "Captiva"],
    "Lexus": ["RX", "NX", "LX", "ES", "GX"],
    "Infiniti": ["Q50", "QX60", "FX", "EX", "Q70"],
    "Land Rover": ["Range Rover", "Discovery", "Defender", "Evoque"],
    "Volvo": ["XC60", "XC90", "S60", "V40", "XC40"],
    "Jeep": ["Grand Cherokee", "Wrangler", "Compass", "Renegade"],
    "Peugeot": ["308", "3008", "408", "508", "2008"],
    "Citroen": ["C4", "C5 Aircross", "Berlingo", "Jumper"],
    "Opel": ["Astra", "Insignia", "Corsa", "Mokka"],
    "Fiat": ["Ducato", "Panda", "500", "Tipo"],
}

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
    kb = [
        [KeyboardButton(text=f"{car.car_brand} {car.car_model} {car.car_year}")]
        for car in cars
    ]
    kb.append([KeyboardButton(text="➕ Добавить новое авто")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def brand_car_kb() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=car)] for car in popular_car.keys()]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def model_car_kb(brand_car: str) -> ReplyKeyboardMarkup or None:

    if brand_car in popular_car.keys():
        kb = [[KeyboardButton(text=car)] for car in popular_car[brand_car]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard

    return None
