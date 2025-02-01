"""
Модуль проверки прав пользователей.
"""

from functools import wraps

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.models import User
from database.confdb import session
from config.logger_config import logger
from bot.utils.work_with_db import get_user_by_chat_id


def is_admin(func):
    """
    Декоратор проверяющий является ли
    пользователь администатором.
    """

    @wraps(func)
    async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
        user: User = await get_user_by_chat_id(chat_id=message.chat.id, session=session)

        if user is None:
            logger.warning(
                f"{message.from_user.username}:{message.chat.id} попытался получить доступ к {func.__name__}, будучи не зарегистрированным."
            )
            return

        if user.is_admin:
            return await func(message, state, *args, **kwargs)

        await message.answer(text="Недостаточно прав для использования этой команды")
        logger.warning(
            f"{message.from_user.username}:{message.chat.id} попытался получить доступ к {func.__name__}"
        )

    return wrapper
