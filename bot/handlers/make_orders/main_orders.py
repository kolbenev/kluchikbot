"""
Главный модуль логики оформления заказов.
"""

import os
import re
import time

from aiogram import F, Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy import select

from bot.handlers.main_menu.main_menu import main_menu
from bot.handlers.make_orders.kb_for_orders import (
    stage_photo,
    button_with_car_user,
    brand_car_kb,
    model_car_kb,
)
from bot.handlers.make_orders.messages_for_orders import (
    send_photo_please,
    get_info_about_order,
    successful_order,
    choice_your_car_or_add_new,
    accepted_information_about_car_go_to_order,
    get_text_about_brand_car,
    get_text_about_model_car,
    get_text_about_year_car,
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
    await state.update_data(user=user)
    data = await state.get_data()
    type_order = data["order_type"]

    if user.cars:
        await callback_query.message.answer(
            text=choice_your_car_or_add_new,
            reply_markup=button_with_car_user(user.cars),
        )
        await state.set_state(OrdersStates.get_info_about_car)
        return

    # Тут первый запрос авто.
    # Запрос у пользователя марки авто.
    await callback_query.message.answer(
        text=get_text_about_brand_car, reply_markup=brand_car_kb()
    )
    await state.set_state(OrdersStates.get_info_about_car)


@router.message(OrdersStates.get_info_about_car)
async def get_info_about_car(message: Message, state: FSMContext):
    """
    Функция для получения информации об авто пользователя.
    """
    data = await state.get_data()
    user = data["user"]
    car = next(
        (
            car
            for car in user.cars
            if f"{car.car_brand} {car.car_model} {car.car_year}" == message.text
        ),
        None,
    )

    if car:
        # Если машина найдена отправляем сразу на оформление заказа.
        await state.update_data(car_id=car.id)
        await message.answer(
            text=accepted_information_about_car_go_to_order,
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(OrdersStates.get_info_about_order)
        return

    if message.text == "➕ Добавить новое авто":
        await message.answer(text=get_text_about_brand_car, reply_markup=brand_car_kb())
        return

    await message.answer(
        text=get_text_about_model_car,
        reply_markup=model_car_kb(message.text),
    )

    await state.update_data(car_brand=message.text)
    await state.set_state(OrdersStates.get_info_about_model_car)


@router.message(OrdersStates.get_info_about_model_car)
async def take_info_about_model_car(message: Message, state: FSMContext):
    """
    Функция для принятия модели авто и запроса года.
    """
    await message.answer(
        text=get_text_about_year_car, reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(car_model=message.text)
    await state.set_state(OrdersStates.get_info_about_year_car)


@router.message(OrdersStates.get_info_about_year_car)
async def take_year_car(message: Message, state: FSMContext):
    """
    Функция для принятия года авто пользователя.
    И создания модели авто в бд.
    """
    is_year = bool(re.match(r"^\d{4}$", message.text))

    if not is_year:
        await message.answer(text="Вы ввели некорректный год, попробуйте еще раз.")
        return

    data = await state.get_data()
    car_model = data["car_model"]
    car_brand = data["car_brand"]
    user = data["user"]
    year = message.text

    car = await make_new_car(
        car_model=car_model,
        car_brand=car_brand,
        car_year=year,
        chat_id=message.chat.id,
        user_id=user.id,
        session=session,
    )

    await message.answer(
        text=accepted_information_about_car_go_to_order,
    )

    await state.update_data(car_id=car.id)
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


async def notify_admin_on_new_order(bot: Bot):
    stmt = select(User).filter(User.admin_level == 0, User.is_admin == True)
    result = await session.execute(stmt)
    admins = result.scalars().all()

    for admin in admins:
        message = (
            "🚨 Новый заказ был сделан! Пожалуйста, проверьте административную панель."
        )
        await bot.send_message(admin.chat_id, message)


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
    await notify_admin_on_new_order(bot)
    time.sleep(3)
    await main_menu(
        message=message,
        state=state,
    )


@router.callback_query(lambda c: c.data == "no_photo")
async def make_order_without_photo(
    callback_query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    """
    Создание заказа если пользователь не отправил фото.
    """
    data = await state.get_data()
    order_type = data["order_type"]
    info_about_order = data["info_about_order"]
    chat_id = callback_query.message.chat.id
    car_id = data["car_id"]
    user = await get_user_by_chat_id(chat_id=chat_id, session=session)

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
    await notify_admin_on_new_order(bot)
    time.sleep(3)
    await main_menu(
        message=callback_query.message,
        state=state,
    )
