#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
import json                                 # Представляет словарь в строку
import time                                 # Для представления времени в читаемом формате
import datetime                             # ---//---
import psutil                               # Для вытаскивания данных по ОЗУ сервера
from secret import apol_id, shobla_id, log_file, activity_file       # Файл с токенами
import constants                            # Файл с константами

# Строка для месячной статистики
month_statistics_string = '🤖 *Статистика по боту за прошлый месяц:*\n\n' \
                          '✅❌ Создано опросов: *{0} шт*\n' \
                          '🛍  Запрошено скидок: *{1} раз*\n' \
                          '💁‍♀️🚗 Обнаружено девок за рулём: *{2} шт*\n' \
                          '👩🏻‍⚕️ Врача вызывали: *{3} раз*\n' \
                          '📌 Запинено сообщений: *{4} шт*\n' \
                          '✅️ Сохранено номеров Рапидов: *{5} шт*\n' \
                          '🦡 Отправлено барсуков: *{6} раз*\n' \
                          '💵 Рубль встал с колен: *{19} раз*\n' \
                          '🫡🇷🇺 Спето российских гимнов: *{7} раз*\n' \
                          '🌐 Заблокировано по маске /29: *{13} раз*\n' \
                          '🇬🇧 Переведено с транслитского: *{17} раз*\n' \
                          '🎤 Отрапортовано кировов: *{14} раз*\n' \
                          '🤌️️️️️️ Cпародировано итальянцев: *{18} раз*\n' \
                          '🥺 Получено эмоционального урона: *{15} раз*\n' \
                          '🧐 Задано вопросов ИИ: *{20} раз*\n' \
                          '👥 Вызваны все участники Шоблы: *{8} раз*\n\n' \
                          'А так же отправлено следующих команд:\n\n' \
                          '/start: *{9} раз*\n/help: *{10} раз*\n/who: *{11} раз*\n/meeting: *{16} раз*\n/rapid: *{12} раз*'


# Функция формирования текста по статистике за месяц
def month_statistics(bot, activity_count, cur_month):
    try:
        return month_statistics_string.format(activity_count[cur_month]['opros'], activity_count[cur_month]['discount'], activity_count[cur_month]['car_girl'],
                                              activity_count[cur_month]['hey_doc'], activity_count[cur_month]['pin'], activity_count[cur_month]['rapid_new'],
                                              activity_count[cur_month]['cyk'], activity_count[cur_month]['russia'], activity_count[cur_month]['team'],
                                              activity_count[cur_month]['start'], activity_count[cur_month]['help'], activity_count[cur_month]['who'],
                                              activity_count[cur_month]['rapid'], activity_count[cur_month]['/29'], activity_count[cur_month]['kirov'],
                                              activity_count[cur_month]['damage'], activity_count[cur_month]['meeting'], activity_count[cur_month]['transl'],
                                              activity_count[cur_month]['mamma'], activity_count[cur_month]['usd'], activity_count[cur_month]['yapoznaumir'])
    except Exception as month_statistics_error:
        log(bot, f'Ошибка в функции service_func.month_statistics:\nТекст ошибки: {month_statistics_error}')
        bot.send_message(apol_id, f'❌ Ошибка в функции service_func.month_statistics:\nТекст ошибки:\n{month_statistics_error}')
        return 'Error'


# Запись событий в файл log.txt
def log(bot, text):
    try:
        with open(log_file, 'a') as log_stream:
            log_stream.write(f'{time.ctime(time.time())} - {text}\n')
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
        with open(activity_file, 'r') as activity_stream:  # Загружаем данные из файла activity_count
            activity_count = json.loads(activity_stream.read())
        activity_count[current_month][field] += 1
        with open(activity_file, 'w') as activity_stream:  # Записываем данные в файл activity_count
            activity_stream.write(json.dumps(activity_count))
    except Exception as update_activity_error:
        log(bot, f'Ошибка в функции service_func.update_activity:\nПоле: {field}\nТекст ошибки: {update_activity_error}')
        bot.send_message(apol_id, f'❌ Ошибка в функции service_func.update_activity:\nПоле: {field}\nТекст ошибки:\n{update_activity_error}')


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
