"""
Главное меню мастерской.
"""

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.handlers.service_workshop.keyboards_for_workshop import (
    main_menu_workshop_kb,
    leave_an_application,
    leave_an_application_with_car,
)
from bot.handlers.service_workshop.text_for_message_workshop import (
    main_menu_workshop_text,
    text_for_auto_keys,
    text_for_cars_with_cheap,
    text_for_cheap_autostart,
    text_for_repair_controler,
    text_for_soldering,
    text_for_immobilizer,
    text_keys_for_home,
)


router = Router()


@router.callback_query(lambda c: c.data == "workshop")
async def main_menu_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Главное меню раздела мастерская.
    """
    await callback_query.message.edit_text(
        text=main_menu_workshop_text, reply_markup=main_menu_workshop_kb()
    )
    await state.clear()


@router.callback_query(lambda c: c.data == "keys_for_home")
async def main_menu_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Ключи для дома
    """
    await callback_query.message.edit_text(
        text=text_keys_for_home, reply_markup=leave_an_application()
    )
    await state.update_data(order_type="Ключи для дома")


@router.callback_query(lambda c: c.data == "keys_for_cars")
async def keys_for_car_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Изготовление автоключей.
    """
    await callback_query.message.edit_text(
        text=text_for_auto_keys, reply_markup=leave_an_application_with_car()
    )
    await state.update_data(order_type="Изготовление автоключей")


@router.callback_query(lambda c: c.data == "keys_for_car_with_chip")
async def cars_with_chip(callback_query: CallbackQuery, state: FSMContext):
    """
    Изготовление автоключа с чипом.
    """
    await callback_query.message.edit_text(
        text=text_for_cars_with_cheap, reply_markup=leave_an_application_with_car()
    )
    await state.update_data(order_type="Изготовление автоключа с чипом")


@router.callback_query(lambda c: c.data == "chip_for_autostart")
async def chip_with_autostart(callback_query: CallbackQuery, state: FSMContext):
    """
    Чипы для автозапуска
    """
    await callback_query.message.edit_text(
        text=text_for_cheap_autostart, reply_markup=leave_an_application_with_car()
    )
    await state.update_data(order_type="Чипы для автозапуска")


@router.callback_query(lambda c: c.data == "repair_controls_and_key")
async def reapair_controlers(callback_query: CallbackQuery, state: FSMContext):
    """
    Ремонт пультов и брелков.
    """
    await callback_query.message.edit_text(
        text=text_for_repair_controler, reply_markup=leave_an_application_with_car()
    )
    await state.update_data(order_type="Ремонт пультов и брелков")


@router.callback_query(lambda c: c.data == "soldering_and_restoration_of_boards")
async def soldering_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Пайка и восстановление плат
    """
    await callback_query.message.edit_text(
        text=text_for_soldering, reply_markup=leave_an_application_with_car()
    )
    await state.update_data(order_type="Пайка и восстановление плат")


@router.callback_query(lambda c: c.data == "immobilizer_calibration")
async def immobilizer_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Калибровка иммобилайзера
    """
    await callback_query.message.edit_text(
        text=text_for_immobilizer, reply_markup=leave_an_application_with_car()
    )
    await state.update_data(order_type="Калибровка иммобилайзера")
