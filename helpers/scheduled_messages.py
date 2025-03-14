#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
import json                                 # Представляет словарь в строку
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
        with open(secret.meeting_file, 'r') as meeting_file:
            curr_meeting_poll = json.loads(meeting_file.read())
        # Отправка предупреждения о загрузке оперативной памяти
        service_func.alarm(bot)
        # Если сейчас время для рассылки уведомлений о созвоне (все остальные рассылки только в 9 утра)
        if now_time.hour != 9:
            if now_time.weekday() - 3 == curr_meeting_poll['max_date'] and now_time.hour - 13 == curr_meeting_poll['max_time'] and curr_meeting_poll['first_poll'] == 1:
                reminder = bot.send_message(secret.shobla_id, 'Сегодня шоблосозвон будет через час. Ожидайте ссылку.', parse_mode='Markdown')
                bot.pin_chat_message(secret.shobla_id, reminder.message_id, disable_notification=False)
                service_func.log(bot, 'отправлено напоминание на общий созвон')
            if now_time.weekday() - 3 == curr_meeting_poll['max_date'] and now_time.hour - 14 == curr_meeting_poll['max_time'] and curr_meeting_poll['first_poll'] == 1:
                photo = bot.send_photo(secret.shobla_id, constants.meeting_pic, caption=f'*Го созвон: *{constants.meeting_link}', parse_mode='Markdown')
                bot.pin_chat_message(secret.shobla_id, photo.message_id, disable_notification=False)
                curr_meeting_poll['first_poll'] = 0  # Флаг, что это не первый опрос в этом месяце
                with open(secret.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
                    meeting_file.write(json.dumps(curr_meeting_poll))
                service_func.log(bot, 'отправлено приглашение на общий созвон')
                service_func.log(bot, 'поставлен флаг, что уже был опрос в этом месяце')
            return
        # Если сейчас 9 утра (по МСК), то начать различные рассылки
        else:
            if now_time.weekday() == 3 and now_time.day <= 7:  # День (четверг) для отправки опроса о принятии участия в созвоне
                meeting_poll = bot.send_poll(secret.shobla_id, constants.opros, constants.meeting_options, is_anonymous=False, allows_multiple_answers=True)
                bot.pin_chat_message(secret.shobla_id, meeting_poll.message_id, disable_notification=False)
                curr_meeting_poll['msg_id'] = meeting_poll.id
                curr_meeting_poll['poll_id'] = meeting_poll.poll.id
                curr_meeting_poll['max_date'] = 10
                curr_meeting_poll['max_time'] = 10
                curr_meeting_poll['first_poll'] = 1  # Флаг, что это первый опрос в этом месяце
                with open(secret.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
                    meeting_file.write(json.dumps(curr_meeting_poll))
                service_func.log(bot, 'отправка опроса о принятии участия в созвоне')
                service_func.log(bot, 'поставлен флаг, что это первый опрос в этом месяце')
            if now_time.weekday() == 4 and 1 < now_time.day <= 8:  # День (пятница) для остановки опроса о принятии участия в созвоне
                with open(secret.meeting_file, 'r') as meeting_file:
                    curr_meeting_poll = json.loads(meeting_file.read())
                try:
                    bot.stop_poll(secret.shobla_id, curr_meeting_poll['msg_id'])
                except Exception as stop_poll_error:
                    service_func.log(bot, f'Ошибка при закрытии опроса в sdr:\nТекст ошибки:\n{stop_poll_error}')
                    bot.send_message(secret.apol_id, f'❌ Ошибка при закрытии опроса в sdr:\nТекст ошибки:\n{stop_poll_error}')
            # Рассылка по 10челлендж
            if now_time.day == 1:
                challenge = bot.send_message(secret.shobla_id, '📸 Шоблятки, время для #10челлендж и ваших фоточек за месяц!', parse_mode='Markdown')
                bot.pin_chat_message(secret.shobla_id, challenge.message_id, disable_notification=False)
            # Отправка поздравлений с особым днём
            today = f'{now_time.day}.{now_time.month}'
            if today == '28.5':  # День Баяна в Шобле отмечается 28 мая
                bot.send_photo(secret.shobla_id, constants.bayan_day_pic, caption='🪗 Шобла, поздравляю с Днём Баяна!')
            if today == '24.11':  # День Рождения бота
                bot.send_message(secret.shobla_id, f'🥳 Сегодня ботику уже *{now_time.year - 2016} лет*!', parse_mode='Markdown')
            # Отправка поздравлений с ДР
            try:
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
