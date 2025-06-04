#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
import threading                            # Для отсчета времени для отправки сообщений
import datetime                             # Для представления времени в читаемом формате
import constants                            # Файл с константами
import secret                               # Файл с токенами
from helpers import service_func            # Файл со служебными функциями


# Функция отправки сообщений по расписанию
def send_message(bot):
    try:
        threading.Timer(3600, send_message).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
        now_time = datetime.datetime.now()
        today = f'{now_time.day}.{now_time.month}'
        service_func.alarm(bot)  # Отправка предупреждения о загрузке оперативной памяти
        if now_time.hour == 9:
            if now_time.day == 1:  # Рассылка по 10челлендж
                challenge = bot.send_message(secret.shobla_id, '📸 Шоблятки, время для #10челлендж и ваших фоточек за месяц!', parse_mode='Markdown')
                bot.pin_chat_message(secret.shobla_id, challenge.message_id, disable_notification=False)
            # Отправка поздравлений с особым днём
            if today == '28.5':  # День Баяна в Шобле отмечается 28 мая
                bot.send_photo(secret.shobla_id, constants.bayan_day_pic, caption='🪗 Шобла, поздравляю с Днём Баяна!')
            elif today == '24.11':  # День Рождения бота
                bot.send_message(secret.shobla_id, f'🥳 Сегодня ботику уже *{now_time.year - 2016} лет*!', parse_mode='Markdown')
            try:  # Отправка поздравлений с ДР
                for user_id in secret.shobla_member:
                    age = now_time.year - secret.shobla_member[user_id]['year']
                    if secret.shobla_member[user_id]['dd_mm'] == today:
                        if age % 10 == 0:  # Если у человека юбилей
                            bot.send_message(secret.shobla_id, constants.happy_anniversary.format(secret.shobla_member[user_id]['name'], user_id, age), parse_mode='Markdown')
                        else:
                            bot.send_message(secret.shobla_id, f'🥳 [{secret.shobla_member[user_id]["name"]}](tg://user?id={user_id}), с др!', parse_mode='Markdown')
            except Exception as happy_bd_error:
                service_func.log(bot, f'{constants.errors[35]}:\nТекст ошибки:\n{happy_bd_error}')
                bot.send_message(secret.apol_id, f'❌ {constants.errors[35]}\nТекст ошибки:\n{happy_bd_error}')
    except Exception as sdr_error:
        service_func.log(bot, f'{constants.errors[34]}:\nТекст ошибки:\n{sdr_error}')
        bot.send_message(secret.apol_id, f'❌ {constants.errors[34]}\nТекст ошибки:\n{sdr_error}')
