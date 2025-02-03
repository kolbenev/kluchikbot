"""
Модуль состояний.
"""

from aiogram.fsm.state import State, StatesGroup


class RegisterStates(StatesGroup):
    take_phone_num = State()


class OrdersStates(StatesGroup):
    get_info_about_order = State()
    get_photo = State()
    get_info_about_car = State()
    get_info_about_model_car = State()
    get_info_about_brand_car = State()
    get_info_about_year_car = State()


class ReportStates(StatesGroup):
    make_report = State()


class AdminStates(StatesGroup):
    select_car_brand = State()
    broadcast_text = State()
    broadcast_photo = State()
    broadcast_type = State()
    select_brand_for_count = State()
    bid_admin_login = State()
    admin_login = State()
    sale = State()
    accrue_bonuses = State()
    report_answer_for_user = State()
    report_answer = State()
    order_answer = State()
    order_answer_for_user = State()
    sending_message = State()
    sending_photo = State()
    delete_admin = State()
    select_bonus_action = State()
