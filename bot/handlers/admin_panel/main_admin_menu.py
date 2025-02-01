"""
Модуль обработки административной панели.
"""

import os

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot.handlers.admin_panel.kb_for_admin import (
    cancel_kb,
    main_menu_admin_kb,
    check_report_kb,
    check_order_kb,
)
from bot.handlers.main_menu.main_menu import main_menu
from bot.utils.decorators import is_admin
from bot.utils.states import AdminStates
from bot.utils.work_with_db import (
    get_user_by_chat_id,
    find_client_by_phone_number,
    count_all_reports,
    count_all_orders,
)
from config.load_env import BIG_ADMIN_PASSWORD, ADMIN_PASSWORD
from config.logger_config import logger, admin_action_logger
from database.confdb import session
from database.models import User, Report, Order

router = Router()


# ======================================================================================================================
"""
Логика обработки авторизации

Команды:
/bigadminlogin
/adminlogin
"""

@router.message(Command("bigadminlogin"))
async def big_boss_login(message: Message, state: FSMContext):
    """
    Авторизация старшего администратора.
    """
    await message.answer(text="Введите пароль старшего администратора: ")
    await state.set_state(AdminStates.bid_admin_login)


@router.message(AdminStates.bid_admin_login)
async def check_big_admin_pass(message: Message, state: FSMContext):
    """
    Проверка пароля старшего администратора.
    """
    if message.text != BIG_ADMIN_PASSWORD:
        await message.answer("Вы ввели неверный пароль!")
        logger.warning(
            f"{message.from_user.username}:{message.chat.id} | ВВЕЛ НЕВЕРНЫЙ ПАРОЛЬ СТАРШЕГО АДМИНА!"
        )
        await main_menu(message, state)
        return

    elif message.text == BIG_ADMIN_PASSWORD:
        user: User = await get_user_by_chat_id(
            chat_id=message.chat.id,
            session=session,
        )
        user.is_admin = True
        user.admin_level = 1
        await session.commit()
        logger.warning(
            f"{message.from_user.username}:{message.chat.id} | АВТОРИЗОВАЛСЯ КАК СТАРШИЙ АДМИН!"
        )

        await message.answer(
            text="Вы успешно авторизовались как старший администратор."
        )
        await main_menu(message, state)


@router.message(Command("adminlogin"))
async def login_admin(message: Message, state: FSMContext):
    """
    Авторизация администратора.
    """
    await message.answer(text="Введите пароль администратора:")
    await state.set_state(AdminStates.admin_login)


@router.message(AdminStates.admin_login)
async def check_admin_pass(message: Message, state: FSMContext):
    """
    Проверка пароля администратора.
    """
    if message.text != ADMIN_PASSWORD:
        await message.answer("Вы ввели неверный пароль!")
        logger.warning(
            f"{message.from_user.username}:{message.chat.id} | ВВЕЛ НЕВЕРНЫЙ ПАРОЛЬ АДМИНА!"
        )
        await main_menu(message, state)
        return

    elif message.text == ADMIN_PASSWORD:
        user: User = await get_user_by_chat_id(
            chat_id=message.chat.id,
            session=session,
        )
        user.is_admin = True
        user.admin_level = 0
        await session.commit()
        logger.warning(
            f"{message.from_user.username}:{message.chat.id} | АВТОРИЗОВАЛСЯ КАК АДМИН!"
        )

        await message.answer(text="Вы успешно авторизовались как администратор.")
        await main_menu(message, state)


# ======================================================================================================================
"""
Логика обработки команды /sale
"""
@router.message(Command("sale"))
@is_admin
@admin_action_logger
async def make_sale(message: Message, state: FSMContext):
    """
    Обработка команды /sale

    Запрос у пользователя номера телефона клиента.
    """
    await message.answer(
        text="Введите номер телефона клиента:\nПример: +79161231212",
        reply_markup=cancel_kb(),
    )
    await state.set_state(AdminStates.sale)


@router.message(AdminStates.sale)
@admin_action_logger
async def make_sale_process(message: Message, state: FSMContext):
    """
    Поиск пользователя по номеру телефона.

    В случае неудачи вывод информации о неверном номере телефоне.
    """
    if message.text == "Отмена":
        await message.answer(text="Отмена", reply_markup=ReplyKeyboardRemove())
        await main_menu(message, state)
        return

    client: User = await find_client_by_phone_number(
        phone=message.text,
        session=session,
    )

    if client is None:
        await message.answer(
            text="Введен неверный номер телефона.", reply_markup=cancel_kb()
        )
        return

    await message.answer(
        reply_markup=cancel_kb(),
        text=f"""
Все ли верно?
Клиент:
{client.first_name}, @{client.username}, {client.phone_number}

Текущий баланс бонусов: {client.count_bonuses}

Выберите действие:
1. Добавить бонусы
2. Снять бонусы
"""
    )
    await state.update_data(client=client)
    await state.set_state(AdminStates.select_bonus_action)


@router.message(AdminStates.select_bonus_action)
@admin_action_logger
async def select_bonus_action(message: Message, state: FSMContext):
    """
    Выбор действия для бонусов (добавить или снять).
    """
    if message.text == "Отмена":
        await message.answer(text="Отмена", reply_markup=ReplyKeyboardRemove())
        await main_menu(message, state)
        return

    if message.text not in ["1", "2"]:
        await message.answer(
            text="Пожалуйста, выберите действие: 1 для добавления бонусов, 2 для снятия.",
            reply_markup=cancel_kb()
        )
        return

    action = "add" if message.text == "1" else "remove"
    await state.update_data(action=action)

    await message.answer(
        text=f"Введите количество бонусов, которые будут {'добавлены' if action == 'add' else 'сняты'}:"
    )
    await state.set_state(AdminStates.accrue_bonuses)


@router.message(AdminStates.accrue_bonuses)
@admin_action_logger
async def accrue_or_remove_bonuses(message: Message, state: FSMContext):
    """
    Начисление или снятие баллов пользователю в зависимости от выбора администратора.
    Если текст от администратора == Отмена, операция завершается.
    """
    data = await state.get_data()
    client: User = data["client"]
    action = data.get("action")

    if message.text == "Отмена":
        await message.answer(text="Отмена", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        await state.set_state(AdminStates.sale)
        return

    try:
        bonus_amount = int(message.text)
    except ValueError:
        await message.answer(
            text="Пожалуйста, введите количество бонусов в виде числа.",
            reply_markup=cancel_kb(),
        )
        return

    if action == "add":
        client.count_bonuses += bonus_amount
        await message.answer(
            text=f"Пользователю {client.first_name} добавлено {bonus_amount} баллов.",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif action == "remove":
        client.count_bonuses = max(0, client.count_bonuses - bonus_amount)
        await message.answer(
            text=f"У пользователя {client.first_name} снято {bonus_amount} баллов.",
            reply_markup=ReplyKeyboardRemove(),
        )

    await session.commit()
    await state.clear()
    await state.set_state(AdminStates.sale)



# ======================================================================================================================
"""
Работа кнопок администраторов и выдача клавиатуры администратора -> /admin
"""

@router.message(Command("admin"))
@is_admin
@admin_action_logger
async def admin_panel(message: Message, state: FSMContext):
    await message.answer(
        text="Меню администратора",
        reply_markup=main_menu_admin_kb(),
    )


@router.message(F.text == "Количество сообщений от пользователей")
@is_admin
@admin_action_logger
async def get_count_report(message: Message, state: FSMContext):
    count_report = await count_all_reports(session=session)
    await message.answer(text=f"Количество запросов от пользователей: {count_report}")


@router.message(F.text == "Количество новых заказов")
@is_admin
@admin_action_logger
async def get_count_report(message: Message, state: FSMContext):
    count_report = await count_all_orders(session=session)
    await message.answer(text=f"Количество новых заказов: {count_report}")


# ======================================================================================================================
"""
Логика работы меню режима ответов на сообщения
"""


@router.message(F.text == "Меню ответов на сообщения")
@is_admin
@admin_action_logger
async def check_user_reports(message: Message, state: FSMContext) -> None:
    """
    Функция запускающая режим "ответов на репорты" для администратора.
    """
    stmt = (
        select(Report)
        .options(joinedload(Report.user))
        .order_by(Report.created_at.asc())
        .limit(1)
    )
    result = await session.execute(stmt)
    user_report: Report = result.scalar()

    if not user_report:
        await message.answer(text="Сообщений нет.", reply_markup=main_menu_admin_kb())
        await state.clear()
        return

    user = user_report.user
    await message.answer(
        text=f"{user_report.report_text}\n\nПользователь: {user.first_name}\n"
        f"{user.username}:{user.chat_id}\n"
        f"Номер телефона: {user.phone_number}\n"
        f"Дата создания: {user_report.created_at}\n",
        reply_markup=check_report_kb(),
    )
    await state.update_data(user_report=user_report)
    await state.set_state(AdminStates.report_answer)


@router.message(AdminStates.report_answer)
@admin_action_logger
async def reply_to_report(message: Message, state: FSMContext) -> None:
    """
    Функция для обработки репорта. Если ответ администратора равен
    "Ответить ✅" -> у администратора запросят сообщение для пользователя,
    "Удалить ❌" -> репорт удаляется из базы данных без ответа,
    "Выйти" -> администратор выходит из режима ответов на репорты.
    """
    data = await state.get_data()
    user_report = data.get("user_report")

    if message.text == "Ответить ✅":
        await message.answer(
            text="Введите сообщение для пользователя:", reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.report_answer_for_user)

    elif message.text == "Удалить ❌":
        await session.delete(user_report)
        await session.commit()
        await message.answer(text="Репорт удален")
        return await check_user_reports(message, state)

    elif message.text == "Выйти":
        await message.answer(
            text="Выход из чекера репортов", reply_markup=main_menu_admin_kb()
        )
        await state.clear()


@router.message(AdminStates.report_answer_for_user)
@admin_action_logger
async def report_for_user(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Функция для отправки ответа на репорт пользователю.
    Если сообщение администратора равно "Отмена", админ
    возвращается в режим обработки репорта. В ином случае,
    сообщение администратора отправляется пользователю.
    """
    if message.text == "Отмена":
        await message.answer(text="Отмена отправки сообщения (репорт остается в бд)")
        return await check_user_reports(message, state)

    data = await state.get_data()
    user_report = data.get("user_report")

    await bot.send_message(
        chat_id=user_report.user.chat_id,
        text=f"👨‍💻 Сообщение от администратора:\n\n {message.text}",
    )
    await message.answer(text="Сообщение успешно отправлено пользователю")
    await session.delete(user_report)
    await session.commit()
    await state.clear()
    return await check_user_reports(message, state)


# ======================================================================================================================
"""
Логика работы режима обработки заказов.
"""

@router.message(F.text == "Меню обработки заказов")
@is_admin
@admin_action_logger
async def check_user_orders(message: Message, state: FSMContext) -> None:
    """
    Функция запускающая режим "обработки заказов" для администратора.
    """
    stmt = (
        select(Order)
        .options(joinedload(Order.user), joinedload(Order.car))
        .order_by(Order.created_at.asc())
        .limit(1)
    )
    result = await session.execute(stmt)
    user_order: Order = result.scalars().first()

    if not user_order:
        await message.answer(text="Заказов нет.", reply_markup=main_menu_admin_kb())
        await state.clear()
        return

    user = user_order.user
    car_info = user_order.car.info_about_car if user_order.car else "Без авто"

    await message.answer(
        text=f"Заказ: {user_order.info_order}\n\n"
        f"Пользователь: {user.first_name}\n"
        f"{user.username}: {user.chat_id}\n"
        f"Тип заказа: {user_order.type_order}\n"
        f"Номер телефона: {user.phone_number}\n"
        f"Автомобиль: {car_info}\n"
        f"Дата создания: {user_order.created_at}\n",
        reply_markup=check_order_kb(),
    )

    if user_order.attachment and os.path.exists(user_order.attachment):
        try:
            await message.answer_document(document=FSInputFile(user_order.attachment))
        except Exception as e:
            await message.answer(text=f"⚠ Ошибка отправки вложения: {e}")

    await state.update_data(user_order=user_order)
    await state.set_state(AdminStates.order_answer)


@router.message(AdminStates.order_answer)
@admin_action_logger
async def reply_to_order(message: Message, state: FSMContext) -> None:
    """
    Обработка заказа. Возможные действия:
    - "Ответить ✅" - запрашивает сообщение администратора пользователю.
    - "Удалить ❌" - удаляет заказ и вложение.
    - "Выйти" - выходит из режима работы с заказами.
    """
    data = await state.get_data()
    user_order = data.get("user_order")

    if message.text == "Ответить ✅":
        await message.answer(
            text="Введите сообщение для пользователя:", reply_markup=cancel_kb()
        )
        await state.set_state(AdminStates.order_answer_for_user)

    elif message.text == "Удалить ❌":
        if user_order.attachment and os.path.exists(user_order.attachment):
            os.remove(user_order.attachment)

        await session.delete(user_order)
        await session.commit()
        await message.answer(text="Заказ удалён")
        return await check_user_orders(message, state)

    elif message.text == "Выйти":
        await message.answer(
            text="Выход из обработки заказов", reply_markup=main_menu_admin_kb()
        )
        await state.clear()


@router.message(AdminStates.order_answer_for_user)
@admin_action_logger
async def order_for_user(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Отправка ответа на заказ пользователю.
    """
    if message.text == "Отмена":
        await message.answer(text="Отмена отправки сообщения (заказ остается в БД)")
        return await check_user_orders(message, state)

    data = await state.get_data()
    user_order = data.get("user_order")

    await bot.send_message(
        chat_id=user_order.user.chat_id,
        text=f"\U0001f4e2 Сообщение от администратора по поводу вашего заказа:\n\n{message.text}",
    )

    await message.answer(text="Сообщение успешно отправлено пользователю")

    if user_order.attachment and os.path.exists(user_order.attachment):
        os.remove(user_order.attachment)

    await session.delete(user_order)
    await session.commit()
    await state.clear()
    return await check_user_orders(message, state)

# ======================================================================================================================
"""
Команды старшего администратора

/make_sending
/make_sending_with_photo
/deleteadmin
"""

@router.message(F.text == "/make_sending")
@is_admin
async def make_sending(message: Message, state: FSMContext):
    """
    Команда для отправки текстового сообщения всем пользователям.
    Запрашивает у администратора текст для рассылки. Если текст = "Отмена",
    то операция отменяется.
    """

    user: User = await get_user_by_chat_id(chat_id=message.chat.id, session=session)
    if user.admin_level != 1:
        await message.answer("Ваш уровень не позволяет пользоваться этой командой.")
        return

    await message.answer("Введите текст для рассылки.", reply_markup=cancel_kb())
    await state.set_state(AdminStates.sending_message)


@router.message(AdminStates.sending_message)
@is_admin
async def handle_sending(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка текста для рассылки. Если текст = "Отмена", то отменяем операцию.
    Если текст не "Отмена", отправляем его всем пользователям.
    """

    if message.text == "Отмена":
        await message.answer("Рассылка отменена.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()

    for user in users:
        try:
            await bot.send_message(user.chat_id, message.text)
        except Exception as e:
            logger.warning(f"Не удалось отправить сообщение пользователю {user.chat_id}: {e}")

    await message.answer("Сообщение отправлено всем пользователям.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(F.text == "/make_sending_with_photo")
@is_admin
async def make_sending_with_photo(message: Message, state: FSMContext):
    """
    Команда для отправки текстового сообщения с фото всем пользователям.
    Запрашивает у администратора текст и фото для рассылки. Если текст = "Отмена",
    то операция отменяется. Если текст не введен, то напомнить про первую команду.
    """

    user: User = await get_user_by_chat_id(chat_id=message.chat.id, session=session)
    if user.admin_level != 1:
        await message.answer("Ваш уровень не позволяет пользоваться этой командой.")
        return

    await message.answer("Отправьте фото и текст для рассылки", reply_markup=cancel_kb())
    await state.set_state(AdminStates.sending_photo)


@router.message(AdminStates.sending_photo, F.photo)
@is_admin
async def handle_sending_photo(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка фото и текста для рассылки. Если текст не задан, напомнить об
    использовании первой команды. Если текст = "Отмена", то отменяем операцию.
    """

    if message.text == "Отмена":
        await message.answer("Рассылка отменена.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    if not message.caption:
        await message.answer("Пришлите фото с текстом, чтобы сделать рассылку.")
        await state.clear()
        return

    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()

    for user in users:
        try:
            await bot.send_photo(user.chat_id, message.photo[-1].file_id, caption=message.caption)
        except Exception as e:
            logger.warning(f"Не удалось отправить сообщение пользователю {user.chat_id}: {e}")

    await message.answer("Фото с сообщением отправлены всем пользователям.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(F.text == "/deleteadmin")
@is_admin
async def delete_admin(message: Message, state: FSMContext):
    """
    Команда для понижения уровня администратора. Запрашивает логин администратора,
    чьи права нужно понизить.
    """

    user: User = await get_user_by_chat_id(chat_id=message.chat.id, session=session)
    if user.admin_level != 1:
        await message.answer("Ваш уровень не позволяет пользоваться этой командой.")
        return

    await message.answer("Введите логин администратора, которого вы хотите понизить.")
    await state.set_state(AdminStates.delete_admin)


@router.message(AdminStates.delete_admin)
@is_admin
async def handle_delete_admin(message: Message, state: FSMContext):
    """
    Обрабатывает логин администратора для понижения его прав.
    Если администратор найден, его права понижаются.
    """

    stmt = select(User).filter(User.username == message.text)
    result = await session.execute(stmt)
    admin_to_demote = result.scalars().first()

    if not admin_to_demote:
        await message.answer(f"Администратор с логином @{message.text} не найден.")
        await state.clear()
        return

    admin_to_demote.is_admin = False
    admin_to_demote.admin_level = 0
    await session.commit()

    await message.answer(f"Права администратора @{admin_to_demote.username} были понижены.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("getadminlog"))
@is_admin
async def get_admin_log(message: Message, state: FSMContext):
    """
    Команда /getadminlog для отправки файла логов администратору 1 уровня.
    """

    LOG_FILE_PATH = "admin_log.txt"

    user: User = await get_user_by_chat_id(chat_id=message.chat.id, session=session)
    if user.admin_level != 1:
        await message.answer("Ваш уровень не позволяет пользоваться этой командой.")
        return

    if os.path.exists(LOG_FILE_PATH):
        document = FSInputFile(LOG_FILE_PATH)
        await message.answer_document(document=document)
    else:
        await message.answer(
            text="Ошибка: файл логов не найден."
        )
