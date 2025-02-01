"""
Главный модуль логики оформления заказов.
"""

import os
import time

from aiogram import F, Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from bot.handlers.main_menu.main_menu import main_menu
from bot.handlers.make_orders.kb_for_orders import stage_photo, button_with_car_user
from bot.handlers.make_orders.messages_for_orders import (
    send_photo_please,
    get_info_about_order,
    successful_order,
    choice_your_car_or_add_new,
    accepted_information_about_car_go_to_order,
    text_get_info_about_car,
)
from bot.utils.keyboards import go_back_kb
from bot.utils.states import OrdersStates
from bot.utils.work_with_db import (
    get_user_with_car_by_chat_id,
    get_user_by_chat_id,
    make_order,
    make_new_car,
)
from database.confdb import session
from database.models import User, CarUser

router = Router()


@router.callback_query(lambda c: c.data == "make_order")
async def make_order_without_car(
    callback_query: CallbackQuery,
    state: FSMContext,
):
    """
    Функция для создания заказа без авто.
    """
    await callback_query.message.answer(
        text=get_info_about_order, reply_markup=go_back_kb(callback_data="main_menu")
    )
    await state.update_data(car_id=None)
    await state.set_state(OrdersStates.get_info_about_order)


@router.callback_query(lambda c: c.data == "make_order_with_car")
async def make_order_with_car(
    callback_query: CallbackQuery,
    state: FSMContext,
):
    """
    Функция для создания заказа c авто.
    """
    user: User = await get_user_with_car_by_chat_id(
        chat_id=callback_query.message.chat.id,
        session=session,
    )
    if user.cars:
        await callback_query.message.answer(
            text=choice_your_car_or_add_new,
            reply_markup=button_with_car_user(cars=user.cars),
        )
        await state.set_state(OrdersStates.get_info_about_car)
        return

    await callback_query.message.answer(
        text=text_get_info_about_car, reply_markup=go_back_kb(callback_data="main_menu")
    )
    await state.set_state(OrdersStates.get_info_about_car)


@router.message(OrdersStates.get_info_about_car)
async def get_info_about_car(message: Message, state: FSMContext):
    """
    Функция для получения информации об авто пользователя.
    """
    user: User = await get_user_with_car_by_chat_id(
        chat_id=message.chat.id, session=session
    )
    car = next((car for car in user.cars if car.info_about_car == message.text), None)

    if car is None:
        car = await make_new_car(
            chat_id=message.chat.id,
            info_about_car=message.text,
            user_id=user.id,
            session=session,
        )

    await message.answer(
        text=accepted_information_about_car_go_to_order,
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.update_data(car_id=car.id)
    await state.update_data(user=user)
    await state.set_state(OrdersStates.get_info_about_order)


@router.message(OrdersStates.get_info_about_order)
async def get_info_about_order_from_user(
    message: Message,
    state: FSMContext,
):
    """
    Функция для получения информации о заказе.
    """
    await state.update_data(info_about_order=message.text)
    await message.answer(
        text=send_photo_please,
        reply_markup=stage_photo(),
    )
    await state.set_state(OrdersStates.get_photo)


@router.message(F.photo and OrdersStates.get_photo)
async def get_photo_from_user(message: Message, state: FSMContext, bot: Bot):
    """
    Создание заказа с фото.
    """
    data = await state.get_data()
    order_type = data["order_type"]
    info_about_order = data["info_about_order"]
    chat_id = message.chat.id
    car_id = data["car_id"]
    user = await get_user_by_chat_id(chat_id=chat_id, session=session)

    photo = message.photo[-1]
    photo_path = f"media/{chat_id}/{photo.file_id}.jpg"
    os.makedirs(os.path.dirname(photo_path), exist_ok=True)
    file = await bot.get_file(photo.file_id)
    await bot.download_file(file.file_path, photo_path)

    await make_order(
        chat_id=chat_id,
        type_order=order_type,
        info_order=info_about_order,
        attachment=photo_path,
        car_id=car_id,
        user_id=user.id,
        session=session,
    )

    await message.answer(text=successful_order)
    time.sleep(3)
    await main_menu(
        message=message,
        state=state,
    )


@router.callback_query(lambda c: c.data == "no_photo")
async def make_order_without_photo(
    callback_query: CallbackQuery,
    state: FSMContext,
):
    """
    Создание заказа если пользователь не отправил фото.
    """
    data = await state.get_data()
    order_type = data["order_type"]
    info_about_order = data["info_about_order"]
    chat_id = callback_query.message.chat.id
    car_id = data["car_id"]
    user = await get_user_by_chat_id(chat_id=callback_query.message.chat.id, session=session)

    await make_order(
        chat_id=chat_id,
        type_order=order_type,
        info_order=info_about_order,
        attachment=None,
        car_id=car_id,
        user_id=user.id,
        session=session,
    )

    await callback_query.message.answer(text=successful_order)
    time.sleep(3)
    await main_menu(
        message=callback_query.message,
        state=state,
    )
