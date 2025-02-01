"""
Модуль конфигурации базы данных.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


DATABASE_PATH = "database/database.db"
url = f"sqlite+aiosqlite:///{DATABASE_PATH}"
engine = create_async_engine(url=url)
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
session = Session()
