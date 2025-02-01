import logging
from functools import wraps
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Update, Message

from bot.utils.work_with_db import get_user_by_chat_id
from database.models import User
from database.confdb import session

# Логгер для обычных пользователей
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Уровень логирования
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Логгер для администраторов
admin_logger = logging.getLogger("admin_logger")
admin_logger.setLevel(logging.INFO)  # Уровень логирования
file_handler = logging.FileHandler("admin_log.txt")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)
admin_logger.addHandler(file_handler)


class LoggingMiddleware(BaseMiddleware):
    """
    Данный класс реализует middleware для логирования
    сообщений пользователя.
    """

    def __init__(self):
        super().__init__()
        self.logger = logger

    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            logger.info(
                f"{event.message.from_user.username}:{event.message.chat.id} | Message: {event.message.text}"
            )
        elif event.message is None:
            logger.info(
                f"{event.callback_query.from_user.username}:{event.callback_query.from_user.id}"
                f" | Callback_query: {event.callback_query.data}"
            )
        return await handler(event, data)


def admin_action_logger(func):
    """
    Декоратор для логирования действий админа 0 уровня.
    Логирует только те функции, к которым применяется этот декоратор.
    """

    @wraps(func)
    async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
        user: (
            User) = await get_user_by_chat_id(chat_id=message.chat.id, session=session)

        if user.admin_level == 0:
            admin_logger.info(
                f"Admin {message.from_user.username}:{message.chat.id} ({user.admin_level}) "
                f"executed {func.__name__} with message: {message.text}"
            )
            return await func(message, state, *args, **kwargs)

    return wrapper
