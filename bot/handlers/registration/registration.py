"""
Модуль основной логики регистрации.
"""

import time

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
)

from bot.handlers.main_menu.main_menu import main_menu
from bot.handlers.registration.kb_for_registration import (
    agree_disagree_kb_with_treaty,
    send_contact_kb,
    agree_disagree_kb,
)
from bot.handlers.registration.messages_for_registration import (
    welcome_message,
    take_phone,
    personal_data_agreement,
    error_phone,
    text_for_successful_registration,
)
from bot.utils.states import RegisterStates

from bot.utils.work_with_db import get_user_by_chat_id, registration_new_user
from database.confdb import session
from database.models import User


router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    """
    Команда /start.

    Проверяет зарегистрирован ли пользователь,
    Если да:
        Выдает панель с меню.
    Если нет:
        Присылает welcome message и начинает процесс регистрации.
    """
    user: User = await get_user_by_chat_id(
        chat_id=message.chat.id,
        session=session,
    )

    if user:
        await main_menu(message, state)
        return

    await message.answer(
        text=welcome_message, reply_markup=agree_disagree_kb_with_treaty()
    )


@router.callback_query(lambda c: c.data == "disagree_to_process")
async def user_disagree(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция для отказа от обработки персональных данных.

    На момент 31.01.2025 с помощью aiogram нет возможности
    получить информацию о всем чате, так что происходит
    удаление последнего сообщения.
    """
    await callback_query.message.delete()


@router.callback_query(lambda c: c.data == "agree_to_process")
async def user_disagree(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция для подтверждения обработки персональных данных.
    """
    await callback_query.message.answer(text=take_phone, reply_markup=send_contact_kb())
    await state.set_state(RegisterStates.take_phone_num)


@router.callback_query(lambda c: c.data == "personal_data")
async def personal_data(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция для получения текста согласия обработки персональных
    данных.
    """
    await callback_query.message.edit_text(
        text=personal_data_agreement, reply_markup=agree_disagree_kb()
    )


@router.message(RegisterStates.take_phone_num)
async def finish_registration(message: Message, state: FSMContext):
    """
    Функция для завершения регистрации.

    Создает новые модели в базе данных.
    """

    if message.contact:
        user_phone = message.contact.phone_number.lstrip("+")
    else:
        await message.answer(text=error_phone)
        time.sleep(3)
        return

    user = await registration_new_user(
        chat_id=message.chat.id,
        fisrt_name=message.from_user.first_name,
        phone_number=user_phone,
        username=message.from_user.username,
        session=session,
    )
    answer_for_message = await message.answer(
        text=text_for_successful_registration,
        reply_markup=ReplyKeyboardRemove(),
    )
    time.sleep(3)
    await main_menu(message, state)
