#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
import json                                 # Представляет словарь в строку
import time                                 # Для представления времени в читаемом формате
import datetime                             # ---//---
import psutil                               # Для вытаскивания данных по ОЗУ сервера
from secret import apol_id, shobla_id       # Файл с токенами
import constants                            # Файл с константами


# Запись событий в файл log.txt
def log(bot, text):
    try:
        with open(constants.log_file, 'a') as log_file:
            log_file.write(f'{time.ctime(time.time())} - {text}\n')
    except Exception as log_error:
        bot.send_message(apol_id, f'❌ Ошибка при записи лога\nТекст ошибки:\n{log_error}')


# Функция отправки ошибки
def send_error(bot, message, error_id, error_text):
    try:
        text = f'❌ {constants.errors[error_id]}\nFrom user: {message.from_user.first_name} {message.from_user.last_name}\n'\
               f'Username: @{message.from_user.username}\nChat name: "{message.chat.title}" {message.chat.first_name} {message.chat.last_name}\n'\
               f'Chat id: {message.chat.id}\nMessage: {message.text}\nTime: {time.ctime(time.time())}\nError text: {error_text}'
        bot.send_message(apol_id, text)
        log(bot, text)
    except Exception as send_error_error:
        log(bot, f'{constants.errors[13]}:\nСообщение: {message.text}\nТекст ошибки: {send_error_error}\nИзначальная ошибка: {error_text}')
        bot.send_message(apol_id, f'❌ {constants.errors[13]}:\nСообщение: {message.text}\nТекст ошибки:\n{send_error_error}\nИзначальная ошибка: {error_text}')


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
        bot.send_message(apol_id, f'❌ Ошибка в функции update_activity:\nПоле: {field}\nТекст ошибки:\n{update_activity_error}')


# Функция отправки статуса загрузки памяти на сервере бота
def server_status(bot, message):
    try:
        if len(message.text) == 2:
            bot.send_message(apol_id, f'🤖 RAM free: {psutil.virtual_memory()[2]}% из 512Мбайт')
            log(bot, f'Отправка статуса памяти сервера - RAM free: {psutil.virtual_memory()[2]}% из 512Мбайт')
        else:
            bot.send_message(shobla_id, message.text[3:len(message.text)])
    except Exception as server_info_error:
        send_error(bot, message, 5, server_info_error)


# Функция отправки предупреждения о загрузке ОП на сервере бота
def alarm(bot):
    if psutil.virtual_memory()[2] > 80:
        bot.send_message(apol_id, f'‼️ *Oh shit, attention* ‼️\n💾 Used RAM: {psutil.virtual_memory()[2]}%', parse_mode='Markdown')
