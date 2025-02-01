"""
Модуль для загрузки глобальных переменных.
"""

import dotenv

import os

dotenv.load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
BIG_ADMIN_PASSWORD = os.getenv("BIG_ADMIN_PASSWORD")
