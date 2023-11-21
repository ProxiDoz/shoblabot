#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
import json                                 # Представляет словарь в строку
import time                                 # Для представления времени в читаемом формате
import datetime                             # ---//---
import secret                               # Файл с токенами
import constants                            # Файл с константами


# Запись событий в файл log.txt
def log(bot, text):
    try:
        with open(constants.log_file, 'a') as log_file:
            log_file.write(f'{time.ctime(time.time())} - {text}\n')
    except Exception as log_error:
        bot.send_message(secret.apol_id, f'❌ Ошибка при записи лога\nТекст ошибки:\n{log_error}')


# Функция отправки ошибки
def send_error(bot, message, error_id, error_text):
    try:
        text = f'❌ {constants.errors[error_id]}\nFrom user: {message.from_user.first_name} {message.from_user.last_name}\n'\
               f'Username: @{message.from_user.username}\nChat name: "{message.chat.title}" {message.chat.first_name} {message.chat.last_name}\n'\
               f'Chat id: {message.chat.id}\nMessage: {message.text}\nTime: {time.ctime(time.time())}\nError text: {error_text}'
        bot.send_message(secret.apol_id, text)
        log(bot, text)
    except Exception as send_error_error:
        log(bot, f'{constants.errors[13]}:\nСообщение: {message.text}\nТекст ошибки: {send_error_error}\nИзначальная ошибка: {error_text}')
        bot.send_message(secret.apol_id, f'❌ {constants.errors[13]}:\nСообщение: {message.text}\nТекст ошибки:\n{send_error_error}\nИзначальная ошибка: {error_text}')


# Функция сбора статистики по командам и функциям
def update_activity(bot, field):
    try:
        now_time = datetime.datetime.now()
        current_month = f'{now_time.year}.{now_time.month}'
        with open(constants.activity_file, 'r') as activity_file:  # Загружаем данные из файла activity_count
            activity_count = json.loads(activity_file.read())
        activity_count[current_month][field] += 1
        with open(constants.activity_file, 'w') as activity_file:  # Записываем данные в файл activity_count
            activity_file.write(json.dumps(activity_count))
    except Exception as update_activity_error:
        log(bot, f'Ошибка в функции update_activity:\nПоле: {field}\nТекст ошибки: {update_activity_error}')
        bot.send_message(secret.apol_id, f'❌ Ошибка в функции update_activity:\nПоле: {field}\nТекст ошибки:\n{update_activity_error}')
