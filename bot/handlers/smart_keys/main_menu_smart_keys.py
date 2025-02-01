"""
Меню смарт ключей.
"""

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.handlers.smart_keys.smart_keys_kb import smart_keys_main_menu, make_application_kb
from bot.handlers.smart_keys.text_for_smartkeys import (
    text_for_main_menu_smartkeys,
    text_for_smart_description,
    text_for_programming_smart_keys,
    text_for_lost_smart_keys,
)
from bot.utils.keyboards import go_back_kb


router = Router()


@router.callback_query(lambda c: c.data == "smart_keys")
async def main_menu_smart_keys(callback_query: CallbackQuery, state: FSMContext):
    """
    Главное меню смарт-ключей.
    """
    await callback_query.message.edit_text(
        text=text_for_main_menu_smartkeys, reply_markup=smart_keys_main_menu()
    )


@router.callback_query(lambda c: c.data == "smart_key_description")
async def smart_description(callback_query: CallbackQuery, state: FSMContext):
    """
    Описание Smart-ключей и наших преимуществ
    """
    await callback_query.message.edit_text(
        text=text_for_smart_description, reply_markup=go_back_kb(callback_data="smart_keys")
    )


@router.callback_query(lambda c: c.data == "smart_key_programming")
async def smart_programming(callback_query: CallbackQuery, state: FSMContext):
    """
    Программирование Smart-ключа
    """
    await callback_query.message.edit_text(
        text=text_for_programming_smart_keys, reply_markup=make_application_kb()
    )
    await state.update_data(order_type="Программирование Smart-ключа")


@router.callback_query(lambda c: c.data == "lost_smart_key")
async def main_menu_smart_keys(callback_query: CallbackQuery, state: FSMContext):
    """
    Полная утеря Smart-ключа
    """
    await callback_query.message.edit_text(
        text=text_for_lost_smart_keys, reply_markup=make_application_kb()
    )
    await state.update_data(order_type="Полная утеря Smart-ключа")

