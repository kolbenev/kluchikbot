"""
Модуль с сообщениями для главного меню.
"""
from database.models import User

main_menu_text = """
🔑 Главное меню – Бобер Мастер 🦫
"""

text_for_discounts = """
<b>💬 Скидка за отзыв в 2ГИС:</b> 
Оставьте отзыв о наших услугах в 2ГИС, и получите специальную скидку на заказ. Это отличная возможность для вас сэкономить и помочь нам стать лучше!
<b>Покажите телефон с оставленным отзывом:</b> Скидка 150₽!

<b>🔑 Скидка на комплект ключей:</b> 
При покупке комплекта ключей вы получаете скидку на весь набор. Акция действует на определённые комплекты — уточняйте у наших консультантов.

<b>🎁 Каждый пятый ключ бесплатно:</b> 
При заказе 5 ключей, вы получаете пятый в подарок! Это отличное предложение для тех, кто нуждается в большем количестве ключей.

<b>🔗 Кольца для связок ключей бесплатно:</b> 
При покупке ключей мы подарим вам кольца для связок, чтобы вы могли удобно носить все ключи вместе. Акция действует при покупке от двух ключей.

<b>🔋 Диагностика батареек бесплатно:</b> 
Мы проведём диагностику батареек ваших ключей совершенно бесплатно. Акция действительна для всех наших клиентов.

<b>⚡ Зарядка смарт-ключей бесплатно:</b> 
Если ваш смарт-ключ разрядился, мы бесплатно зарядим его для вас. Эта услуга доступна в нашем сервисном центре.
"""

text_for_section_contacts = """
📍 <b>Адрес</b>: Кирова 56, ТЦ "Выбор", Левое крыло
⏰ <b>Время работы</b>: Пн-Пт: 10:00-20:00, Сб-Вс: 10:00-19:30
📱 <b>Телефон</b>: +7 994 136 22 44
🌐 <b>Ссылка на 2ГИС</b>
"""

def get_bonuses_text(user: User) -> str:
    """
    Формирует текст с информацией о бонусах и уровне пользователя.
    """
    if user.count_bonuses < 100:
        user_level = "Уровень 1"
    elif user.count_bonuses < 500:
        user_level = "Уровень 2"
    elif user.count_bonuses < 1000:
        user_level = "Уровень 3"
    else:
        user_level = "Уровень 4"

    bonuses_text = f"""
<b>Накопительная система уровней:</b>

🥉 <b>Уровень 1</b>: 2.5% скидка
🥈 <b>Уровень 2</b>: 5% скидка
🥇 <b>Уровень 3</b>: 7.5% скидка
🏆 <b>Уровень 4</b>: 12.5% скидка

<b>Ваши бонусы:</b> {user.count_bonuses}
<b>Ваш уровень:</b> {user_level}
"""

    return bonuses_text

text_for_report_from_user = """
Введите ваше сообщение которое хотите отправить администратору:
"""

text_for_successful_send_report = """
Ваш запрос администратору успешно отправлен!
"""
