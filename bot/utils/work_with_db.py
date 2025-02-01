"""
Модуль для работы с базой данных.
"""

from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import User, CarUser, Order, Report


async def get_user_by_chat_id(chat_id: int, session: AsyncSession) -> User or None:
    """
    Функция для получения модели пользователя
    из базы данных.
    """
    stmt = select(User).where(User.chat_id == chat_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    return user


async def get_user_with_car_by_chat_id(
    chat_id: int, session: AsyncSession
) -> User or None:
    """
    Функция для получения пользователя с его автомобилями.
    """
    stmt = select(User).where(User.chat_id == chat_id).options(joinedload(User.cars))
    result = await session.execute(stmt)
    user = result.scalars().first()

    return user


async def registration_new_user(
    chat_id: int,
    phone_number: str,
    username: str,
    fisrt_name: str,
    session: AsyncSession,
) -> User:
    """
    Функция для регистрации нового пользователя.
    """
    new_user = User(
        chat_id=chat_id,
        first_name=fisrt_name,
        phone_number=phone_number,
        username=username,
    )
    session.add(new_user)
    await session.commit()
    return new_user


async def make_new_car(
    chat_id: int, info_about_car: str, user_id: int, session: AsyncSession
) -> CarUser:
    """
    Создание новой машины для пользователя.
    """
    new_car = CarUser(
        chat_id=chat_id,
        info_about_car=info_about_car,
        user_id=user_id,
    )
    session.add(new_car)
    await session.commit()
    await session.refresh(new_car)
    return new_car


async def make_order(
    chat_id: int,
    type_order: str,
    info_order: str,
    attachment: str,
    user_id: int,
    session: AsyncSession,
    car_id=None,
) -> Order:
    """
    Функция создания нового заказа.
    """
    new_order = Order(
        chat_id=chat_id,
        type_order=type_order,
        info_order=info_order,
        attachment=attachment,
        car_id=car_id,
        user_id=user_id,
    )
    session.add(new_order)
    await session.commit()

    return new_order


async def make_report(report_text: str, user_id: int, session: AsyncSession) -> Report:
    """
    Функция для создания сообщения администратору.
    """
    new_report = Report(
        report_text=report_text,
        user_id=user_id,
    )
    session.add(new_report)
    await session.commit()

    return new_report


async def find_client_by_phone_number(
    phone: str, session: AsyncSession
) -> User or None:
    """
    Функция для получения клиента по номеру телефона.
    """
    stmt = select(User).where(User.phone_number == phone)
    result = await session.execute(stmt)
    user = result.scalars().first()

    return user


async def count_all_reports(session: AsyncSession) -> int:
    """
    Функция для подсчета общего количества запросов (отчетов) в таблице Report.
    """
    stmt = select(func.count(Report.id))
    result = await session.execute(stmt)
    count = result.scalar()

    return count


async def count_all_orders(session: AsyncSession) -> int:
    """
    Функция для подсчета общего количества заказов.
    """
    stmt = select(func.count(Order.id))
    result = await session.execute(stmt)
    count = result.scalar()

    return count
