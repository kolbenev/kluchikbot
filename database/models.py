"""
Модуль моделей базы данных.
"""

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    BigInteger,
    DateTime,
    ForeignKey,
)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    first_name = Column(String)
    username = Column(String)
    count_bonuses = Column(Integer, default=0)
    level = Column(Integer, default=0)
    phone_number = Column(String(20))
    is_admin = Column(Boolean, default=False)
    admin_level = Column(Integer, default=0)

    cars = relationship("CarUser", backref="user")


class CarUser(Base):
    __tablename__ = "car_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    info_about_car = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    type_order = Column(String())
    info_order = Column(String())
    created_at = Column(DateTime, default=datetime.now)
    attachment = Column(String(), default=None)
    car_id = Column(Integer, ForeignKey("car_users.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    car = relationship("CarUser", backref="orders")
    user = relationship("User", backref="orders")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_text = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(ForeignKey("users.id"))

    user = relationship("User", backref="reports")
