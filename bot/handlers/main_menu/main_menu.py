"""
Модуль логики главного меню.
"""

import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.handlers.main_menu.kb_for_main_menu import main_menu_kb, contats_kb
from bot.handlers.main_menu.messages_for_main_menu import (
    main_menu_text,
    text_for_section_contacts,
    text_for_discounts,
    text_for_report_from_user,
    text_for_successful_send_report, get_bonuses_text,
)
from bot.utils.keyboards import go_back_kb
from bot.utils.states import ReportStates
from bot.utils.work_with_db import get_user_by_chat_id, make_report
from database.confdb import session
from database.models import User


router = Router()


@router.message(Command("menu"))
async def main_menu(message: Message, state: FSMContext):
    """
    Выдача главного меню по команде /menu

    Используется для работы внутри функций, для
    отправки в главное меню.
    """
    await state.clear()
    await message.answer(text=main_menu_text, reply_markup=main_menu_kb())


@router.callback_query(lambda c: c.data == "main_menu")
async def main_menu_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Выдача главного меню по callback_query.
    """
    await state.clear()
    await callback_query.message.edit_text(
        text=main_menu_text, reply_markup=main_menu_kb()
    )


@router.callback_query(lambda c: c.data == "contacts")
async def get_contacts(callback_query: CallbackQuery, state: FSMContext):
    """
    Открытие раздела контакты.
    """
    await callback_query.message.edit_text(
        text=text_for_section_contacts, reply_markup=contats_kb()
    )


@router.callback_query(lambda c: c.data == "bonuses")
async def get_contacts(callback_query: CallbackQuery, state: FSMContext):
    """
    Открытие раздела бонусов и отображение текущего баланса и уровня пользователя.
    """
    user: User = await get_user_by_chat_id(chat_id=callback_query.from_user.id, session=session)

    if user is None:
        await callback_query.message.edit_text(
            text="Ошибка! Пользователь не найден.",
            reply_markup=go_back_kb(callback_data="main_menu"),
        )
        return

    bonuses_text = get_bonuses_text(user)
    await callback_query.message.edit_text(
        text=bonuses_text,
        reply_markup=go_back_kb(callback_data="main_menu"),
    )


@router.callback_query(lambda c: c.data == "discount")
async def get_contacts(callback_query: CallbackQuery, state: FSMContext):
    """
    Открытие раздела скидок.
    """
    await callback_query.message.edit_text(
        text=text_for_discounts,
        reply_markup=go_back_kb(callback_data="main_menu"),
    )


@router.callback_query(lambda c: c.data == "report_from_user")
async def get_text_for_report(callback_query: CallbackQuery, state: FSMContext):
    """
    Открытия раздела связь с администрацией.
    """
    await callback_query.message.answer(
        text=text_for_report_from_user,
        reply_markup=go_back_kb(callback_data="main_menu"),
    )
    await state.set_state(ReportStates.make_report)


@router.message(ReportStates.make_report)
async def report_from_user(message: Message, state: FSMContext):
    """
    Функция для отправки сообщения администратору.
    """
    user: User = await get_user_by_chat_id(chat_id=message.chat.id, session=session)
    await make_report(
        user_id=user.id,
        report_text=message.text,
        session=session,
    )
    await message.answer(text=text_for_successful_send_report)
    time.sleep(3)
    await main_menu(message, state)
