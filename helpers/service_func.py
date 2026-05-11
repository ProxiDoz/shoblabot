#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time                                 # Для представления времени в читаемом формате
import psutil                               # Для вытаскивания данных по ОЗУ сервера
from secret import apol_id, shobla_id, log_file, shobla_member       # Файл с токенами
import constants                            # Файл с константами
from functools import wraps                 # Для декоратора


# Функция для декоратора ошибок
def handler_error(error_code):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                bot = args[0] if args else None
                message = args[1] if len(args) > 1 else None
                send_error(bot, message, error_code, e)
        return wrapper
    return decorator


# Запись событий в файл log.txt при старте бота
def start_log(bot, text):
    try:
        with open(log_file, 'a') as log_stream:
            log_stream.write(f'{time.ctime(time.time())} - {text}\n')
    except Exception as log_error:
        bot.send_message(apol_id, f'❌ Ошибка при записи лога\nТекст ошибки:\n{log_error}')


# Запись событий в файл log.txt
def log(bot, message, text):
    try:
        with open(log_file, 'a') as log_stream:
            log_stream.write(f'{time.ctime(time.time())} - {text} by {shobla_member[message.from_user.id]["name"]}\n')
    except Exception as log_error:
        bot.send_message(apol_id, f'❌ Ошибка при записи лога\nТекст ошибки:\n{log_error}')


# Функция отправки ошибки
def send_error(bot, message, error_id, error_text):
    try:
        text = f'❌ {constants.errors[error_id]}\nFrom user: {message.from_user.first_name} {message.from_user.last_name}\n'\
               f'Username: @{message.from_user.username}\nChat name: "{message.chat.title}" {message.chat.first_name} {message.chat.last_name}\n'\
               f'Chat id: {message.chat.id}\nMessage: {message.text}\nTime: {time.ctime(time.time())}\nError text: {error_text}'
        bot.send_message(apol_id, text)
        start_log(bot, text)
    except Exception as send_error_error:
        start_log(bot, f'{constants.errors[29]}:\nТекст ошибки: {send_error_error}\nИзначальная ошибка: {error_text}')
        bot.send_message(apol_id, f'❌ {constants.errors[29]}:\nСообщение: {message.text}\nТекст ошибки:\n{send_error_error}\nИзначальная ошибка: {error_text}')


# Функция отправки статуса загрузки памяти на сервере бота
def server_status(bot, message):
    try:
        if len(message.text) == 2:
            bot.send_message(apol_id, f'🤖 RAM free: {psutil.virtual_memory()[2]}% из 1024 Мбайт')
            log(bot, message, f'Отправка статуса памяти сервера - RAM free: {psutil.virtual_memory()[2]}% из 1024 Мбайт')
        else:
            bot.send_message(shobla_id, message.text[3:len(message.text)])
    except Exception as server_info_error:
        send_error(bot, message, 30, server_info_error)


# Функция отправки предупреждения о загрузке ОП на сервере бота
def alarm(bot):
    if psutil.virtual_memory()[2] > 60:
        bot.send_message(apol_id, f'‼️ *Oh shit, attention* ‼️\n💾 Used RAM: {psutil.virtual_memory()[2]}%', parse_mode='Markdown')
