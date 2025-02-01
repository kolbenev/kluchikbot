"""
Модуль запуска бота.
"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config.load_env import API_TOKEN
from config.logger_config import LoggingMiddleware, logger
from bot.handlers.registration.registration import router as registration_router
from bot.handlers.main_menu.main_menu import router as main_menu_router
from bot.handlers.service_workshop.main_menu_workshop import (
    router as service_workshop_router,
)
from bot.handlers.smart_keys.main_menu_smart_keys import router as smart_keys_router
from bot.handlers.make_orders.main_orders import router as make_orders_router
from bot.handlers.admin_panel.main_admin_menu import router as admin_menu_router


dp = Dispatcher()
dp.update.middleware(LoggingMiddleware())  # Для логирования всех сообщений.
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    dp.include_router(main_menu_router)
    dp.include_router(service_workshop_router)
    dp.include_router(registration_router)
    dp.include_router(smart_keys_router)
    dp.include_router(make_orders_router)
    dp.include_router(admin_menu_router)
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
