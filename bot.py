#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
# # # # # # Импортозамещение # # # # # #
import telebot                              # Библиотека piTelegramBotAPI
import re                                   # Для поиска ссылки в тексте
import os                                   # Для проверки на существование файла
import g4f                                  # Для работы с нейронкой
import json                                 # Представляет словарь в строку
import time                                 # Для представления времени в читаемом формате
import datetime                             # ---//---
import psutil                               # Для вытаскивания данных по ОЗУ сервера
import random                               # Присвятой рандом
import threading                            # Для отсчета времени для отправки сообщений
import urllib.request as urllib2            # Для Кирюхиного Rapid'a
from urllib.parse import quote              # ---//---
import traceback                            # Для записи в лог файл при траблах бота
import constants                            # Файл с константами
import secret                               # Файл с токенами
import helpers.faggot as faggot             # Файл для функции faggot handler
import helpers.find_words as find_words     # Файл для функции kirov
import helpers.translitsky as translitsky   # Файл для функции транслитского
import helpers.cbr as cbr                   # Файл для команды запросв курса рубля

# # # # # # Инициализация # # # # # #
bot = telebot.TeleBot(secret.tg_token)  # Token бота
bot.set_my_commands([
    telebot.types.BotCommand("/discount", "🤑Скидки"),
    telebot.types.BotCommand("/usd", "💵 Курс рубля"),
    telebot.types.BotCommand("/who", "✅❌Создать опрос"),
    telebot.types.BotCommand("/help", "❓Полезная информация"),
    telebot.types.BotCommand("/meeting", "🎧Ссылка шоблосозвона"),
    telebot.types.BotCommand("/log", "📋Вывод логов бота"),
    telebot.types.BotCommand("/stat", "🤖Статистика по использованию бота"),
    telebot.types.BotCommand("/rapid", "✅ Зеленый Rapid"),
    telebot.types.BotCommand("/yapoznaumir", "🧐 Задай вопрос")
])
activity_count = {}  # Переменная для сбора статистики по командам
curr_meeting_poll = {}  # Переменная для сбора данных по опросу
if os.path.isfile(constants.meeting_file):  # Загружаем данные из файла meeting_file
    with open(constants.meeting_file, 'r') as lang:
        curr_meeting_poll = json.loads(lang.read())
meeting_results = [0, 0, 0, 0, 0, 0, 0, 0]  # Массив для подсчета кол-ва голосов опроса по созвону


# # # # # # Служебные функции и миниадминка /s # # # # # #
# Функция сбора статистики по командам и функциям
def update_activity(field):
    global activity_count
    try:
        now_time = datetime.datetime.now()
        current_month = str(now_time.year) + '.' + str(now_time.month)
        if os.path.isfile(constants.activity_file):  # Загружаем данные из файла activity_count
            with open(constants.activity_file, 'r') as activity_file:
                activity_count = json.loads(activity_file.read())
        activity_count[current_month][field] += 1
        with open(constants.activity_file, 'w') as activity_file:  # Записываем данные в файл activity_count
            activity_file.write(json.dumps(activity_count))
    except Exception as update_activity_error:
        log('Ошибка в функции update_activity:\nПоле: {0}\nТекст ошибки: {1}'.format(field, update_activity_error))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции update_activity:\nПоле: {0}\nТекст ошибки:\n{1}'.format(field, update_activity_error))


# Функция отправки ошибки
def send_error(message, error_id, error_text):
    try:
        bot.send_message(secret.apple_id,
                         '❌ {0}\nОт: {1} {2}\nUsername: @{3}\nЧат: {4} {5} {6}\nid: {7}\nСообщение: {8}\nВремя: {9}\nТекст ошибки: '
                         '{10}'.format(constants.errors[error_id], message.from_user.first_name, message.from_user.last_name, message.from_user.username,
                                       message.chat.title, message.chat.first_name, message.chat.last_name, message.chat.id, message.text,
                                       time.ctime(time.time()), error_text))
    except Exception as send_error_error:
        log('Ошибка в функции send_error:\nСообщение: {0}\nТекст ошибки: {1}'.format(message.text, send_error_error))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции send_error:\nСообщение: {0}\nТекст ошибки:\n{1}'.format(message.text, send_error_error))


# Запись событий в файл log.txt
def log(text):
    try:
        with open(constants.log_file, 'a') as log_file:
            log_file.write(time.ctime(time.time()) + ' - ' + text + '\n')
    except Exception as log_error:
        bot.send_message(secret.apple_id, '❌ Ошибка при записи лога\nТекст ошибки:\n' + str(log_error))


# Вызов информации о сервере и пересылка сообщения в Шоблу (доступно только Аполу)
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.from_user.id == secret.apple_id:  # Это Апол
            try:
                if message.text == '/s':
                    bot.send_message(secret.apple_id, '🤖 RAM free: {0}% из 512Мбайт'.format(psutil.virtual_memory()[2]))
                    log('Отправка статуса памяти сервера')
                else:
                    bot.send_message(secret.tg_chat_id, message.text[3:len(message.text)])
            except Exception as ram_error:
                log('{0}\nТекст ошибки: {1}'.format(constants.errors[21], ram_error))
                send_error(message, 21, ram_error)
        else:
            log('вызов команды /s\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as server_info_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[5], server_info_error))
        send_error(message, 5, server_info_error)


# # # # # # Доступные команды # # # # # #
# Вызов команды для задания вопросов
@bot.message_handler(commands=['yapoznaumir'])
def yapoznaumir(message):
    try:
        update_activity('yapoznaumir')
        log('вызов команды /yapoznaumir by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
        bot.send_message(message.chat.id, constants.enter_question_gpt, reply_to_message_id=message.message_id, reply_markup=telebot.types.ForceReply(True))
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as yapoznaumir_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[32], yapoznaumir_error))
        send_error(message, 32, yapoznaumir_error)


# Вызов стартового сообщения / справки
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:  # Это Шобла или человек из Шоблы
            log('вызов команды {0} by {1}'.format(message.text, constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_message(message.chat.id, constants.help_text, reply_markup=constants.help_keyboard, parse_mode='Markdown')
            update_activity(message.text[1:])
        else:
            log('вызов команды {0}\n{1}: User ID - {2}, user_name - @{3}'.format(message.text, constants.errors[0 if message.text == '/start' else 1],
                                                                                 message.from_user.id, message.from_user.username))
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
    except Exception as handle_start_help_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[0 if message.text == '/start' else 1], handle_start_help_error))
        send_error(message, 0 if message.text == '/start' else 1, handle_start_help_error)


# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        update_activity('who')
        if message.chat.id == secret.tg_chat_id:  # Это Шобла
            log('вызов команды /who by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_message(secret.tg_chat_id, constants.enter_question_new, reply_to_message_id=message.message_id, reply_markup=telebot.types.ForceReply(True))
            bot.delete_message(secret.tg_chat_id, message.message_id)
        elif message.chat.id in constants.tg_ids:
            bot.send_message(message.chat.id, '❌ Опрос создается только в [Шобле](https://t.me/c/1126587083/)', parse_mode='Markdown')
    except Exception as who_will_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[7], who_will_error))
        send_error(message, 7, who_will_error)


# Отправка скидок
@bot.message_handler(commands=['discount'])
def send_discount(message):
    try:
        if message.from_user.id in constants.tg_ids:
            log('вызов команды /discount by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            i = 0
            keyboard_start = telebot.types.InlineKeyboardMarkup(row_width=2)
            while i < len(constants.buttons[0]) - 1:
                keyboard_start.add(telebot.types.InlineKeyboardButton(text=constants.buttons[0][i + 1], callback_data=constants.buttons[1][i + 1]),
                                   telebot.types.InlineKeyboardButton(text=constants.buttons[0][i + 2], callback_data=constants.buttons[1][i + 2]))
                i += 2
            bot.send_message(message.chat.id, constants.buttons[2][0], reply_markup=keyboard_start, parse_mode='Markdown')
            update_activity('discount')
    except Exception as send_discount_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[8], send_discount_error))
        send_error(message, 8, send_discount_error)


# Вызов статистики
@bot.message_handler(commands=['stat'])
def statistics(message):
    global activity_count
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:  # Это Шобла или человек из Шоблы
            now_time = datetime.datetime.now()
            cur_month = str(now_time.year) + '.' + str(now_time.month)
            if os.path.isfile(constants.activity_file):  # Загружаем данные из файла activity_count
                with open(constants.activity_file, 'r') as activity_file:
                    activity_count = json.loads(activity_file.read())
            month_statistics = constants.month_statistics.format(activity_count[cur_month]['opros'], activity_count[cur_month]['discount'],
                                                                 activity_count[cur_month]['car_girl'], activity_count[cur_month]['hey_doc'],
                                                                 activity_count[cur_month]['pin'], activity_count[cur_month]['rapid_new'],
                                                                 activity_count[cur_month]['cyk'], activity_count[cur_month]['russia'],
                                                                 activity_count[cur_month]['team'], activity_count[cur_month]['start'],
                                                                 activity_count[cur_month]['help'], activity_count[cur_month]['who'],
                                                                 activity_count[cur_month]['rapid'], activity_count[cur_month]['/29'],
                                                                 activity_count[cur_month]['kirov'], activity_count[cur_month]['damage'],
                                                                 activity_count[cur_month]['meeting'], activity_count[cur_month]['transl'],
                                                                 activity_count[cur_month]['mamma'], activity_count[cur_month]['usd'],
                                                                 activity_count[cur_month]['yapoznaumir'])
            bot.send_message(message.chat.id, month_statistics.replace('прошлый', 'текущий'), parse_mode='Markdown')
        else:
            log('вызов команды /stat\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6],
                                                                                   message.from_user.id,
                                                                                   message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as statistics_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[4], statistics_error))
        send_error(message, 4, statistics_error)


# Запрос отправки логов по боту
@bot.message_handler(commands=['log'])
def share_log(message):
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:  # Это Шобла или человек из Шоблы
            try:
                log('вызов команды /log by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
                bot.send_document(message.chat.id, open(constants.log_file, 'rb'), caption='🤖📋')
            except Exception as upload_log_error:
                send_error(message, 23, upload_log_error)
        else:
            log('вызов команды /log\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as share_log_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[24], share_log_error))
        send_error(message, 24, share_log_error)


# Запрос на ссылку созвона
@bot.message_handler(commands=['meeting'])
def meeting(message):
    try:
        if message.from_user.id in constants.tg_ids:  # Это человек из Шоблы
            log('вызов команды /meeting by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_photo(message.chat.id, constants.meeting_pic, caption='🤖 *Го созвон*\n' + constants.meeting_link, parse_mode='Markdown')
            update_activity('meeting')
    except Exception as meeting_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[28], meeting_error))
        send_error(message, 28, meeting_error)


# Запрос курса рубля
@bot.message_handler(commands=['usd'])
def usd(message):
    try:
        if message.from_user.id in constants.tg_ids:  # Это человек из Шоблы
            dollar, euro, lari, tenge = cbr.getUSD("USD"), cbr.getUSD("EUR"), cbr.getUSD("GEL"), cbr.getUSD("KZT")
            float_dol = f"{float(dollar.replace(',', '.')):.{2}f}"
            float_eur = f"{float(euro.replace(',', '.')):.{2}f}"
            float_lar = f"{float(lari.replace(',', '.')):.{2}f}"
            float_ten = f"{float(tenge.replace(',', '.')):.{2}f}"
            bot.send_photo(message.chat.id, constants.usd_pic[random.randint(0, len(constants.usd_pic) - 1)],
                           caption="💵 *Курс рубля по данным сайта [ЦБР](https://www.cbr.ru/currency_base/daily/)*:\n"
                                   "`1$ = {0}₽`\n`1€ = {1}₽`\n`1₾ = {2}₽`\n`100₸ = {3}₽`".format(float_dol, float_eur, float_lar, float_ten), parse_mode='Markdown')
            update_activity('usd')
    except Exception as usd_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[31], usd_error))
        send_error(message, 31, usd_error)


# # # # # # Обработка текста # # # # # #
# Обработка девки за рулем
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace('a', '').replace('а', '') == '' and message.chat.id == secret.tg_chat_id)
def aaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Девка за рулём') if len(message.text) > 2 else bot.send_message(secret.tg_chat_id, 'Двк з рлм')
        update_activity('car_girl')
    except Exception as aaa_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[9], aaa_error))
        send_error(message, 9, aaa_error)


# Обработка Emotional damage
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.damage and message.chat.id == secret.tg_chat_id)
def damage(message):
    try:
        bot.send_voice(secret.tg_chat_id, constants.emotional_daaamage)
        update_activity('damage')
    except Exception as damage_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[10], damage_error))
        send_error(message, 10, damage_error)


# Обработка mamma mia
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.mammamia and message.chat.id == secret.tg_chat_id)
def mamma_mia(message):
    try:
        audio = open(constants.mamma_audio_path, 'rb')
        bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)
        update_activity('mamma')
    except Exception as mamma_mia_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[30], mamma_mia_error))
        send_error(message, 30, mamma_mia_error)


# Обработка РАСИЯ
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.russia and message.chat.id == secret.tg_chat_id)
def russia(message):
    try:
        bot.send_voice(secret.tg_chat_id, constants.anthem, '🫡')
        update_activity('russia')
    except Exception as russia_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[11], russia_error))
        send_error(message, 11, russia_error)


# Обработка врача
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.hey_doc and message.chat.id == secret.tg_chat_id)
def hey_doc(message):
    try:
        bot.send_document(secret.tg_chat_id, 'CgADAgADRgIAAkbDcEn-Ox-uqrgsHgI', caption='@oxy_genium')
        update_activity('hey_doc')
    except Exception as hey_doc_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[12], hey_doc_error))
        send_error(message, 12, hey_doc_error)


# Обработка @team
@bot.message_handler(func=lambda message: message.text and constants.team in message.text.lower() and message.chat.id == secret.tg_chat_id)
def team(message):
    try:
        bot.send_message(chat_id=secret.tg_chat_id, disable_notification=False, reply_to_message_id=message.message_id,
                         text=constants.team_text, disable_web_page_preview=True, parse_mode='Markdown')
        update_activity('team')
    except Exception as team_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[14], team_error))
        send_error(message, 14, team_error)


# Обработка @rapid
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(constants.rapid) and message.chat.id == secret.tg_chat_id)
def rapid(message):
    value = ''
    try:
        update_activity('rapid')
        log('вызов команды /rapid by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
        # Сплитуем строку выпилив предварительно ненужные пробелы по бокам
        data = message.text.lower().strip().split(" ")

        # Получаем количество элементов сплитованой строки
        # и если тока 1 элемент то значит аргумент не передали
        # следовательно help по дефолту
        size = len(data)
        value = 'help' if size == 1 else data[1]

        # Ну тут почти без изменений, тока data[1] became value
        response = urllib2.urlopen(
            'https://rapid.zhuykovkb.ru/rapid?data=' + quote(value) + '&memberid=' + str(message.from_user.id))
        answer = json.loads(str(response.read(), 'utf-8'))
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤗 Обязательно учту этот Рапид, ||пусечка|| премиумная',
                             parse_mode='Markdown')
        bot.send_message(secret.tg_chat_id, answer['message'], parse_mode='Markdown')
        if answer['message'] == 'Номер успешно добавлен':
            log('добавлен новый номер Рапида by {0}'.format(
                constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            update_activity('rapid_new')
    except Exception as rapid_error:
        bot.send_message(secret.zhuykovkb_apple_id, 'Ошибка в функции rapid:\n\nДанные ' + quote(value) + '\n\nТекст ошибки ' + str(rapid_error))
        log('Ошибка в функции rapid:\nДанные: {0}\nТекст ошибки: {1}'.format(quote(value), rapid_error))
        send_error(message, 15, rapid_error)


# Обработка барсука
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.suk and message.chat.id == secret.tg_chat_id)
def badger(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсук')
        update_activity('cyk')
    except Exception as badger_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[16], badger_error))
        send_error(message, 16, badger_error)


# Обработка барсюка
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.syuk and message.chat.id == secret.tg_chat_id)
def another_badger(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсюк')
        update_activity('cyk')
    except Exception as another_badger_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[17], another_badger_error))
        send_error(message, 17, another_badger_error)


# Обработка каждого сообщения на гея/лешу
@bot.message_handler(func=lambda m: True)
def faggot_func(message):
    try:
        if random.random() < 0.3:
            eu_country = faggot.getFaggotEUCountryRequest(message.text, ['гей', 'пидор', 'пидр', 'педик', 'гомо', 'гомосек', 'глиномес',
                                                                         'пидераст', 'леша', 'путин', 'путен', 'путейн', 'маргарин', 'путена'])
            if eu_country[0]:
                location = eu_country[1]['coords']
                bot.reply_to(message, 'Ты что то сказал про гея? Держи...')
                bot.send_location(message.chat.id, location['lat'], location['lng'])
        kirov(message)
    except Exception as faggot_func_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[25], faggot_func_error))
        send_error(message, 25, faggot_func_error)


# Обработка Кирова
@bot.message_handler(func=lambda m: True)
def kirov(message):
    try:
        if find_words.wordInMessage(message.text, constants.kirov):
            audio = open(constants.kirov_audio_path, 'rb')
            bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)
            update_activity('kirov')
        send_text(message)
    except Exception as kirov_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[27], kirov_error))
        send_error(message, 27, kirov_error)


# # # # # # Обработка опросов # # # # # #
@bot.poll_handler(func=lambda poll: True)
def poll_results(poll):
    try:
        if poll.is_closed == 1 and str(poll.id) == curr_meeting_poll['poll_id'] and poll.total_voter_count > 1:
            i = 0
            for item in poll.options:
                meeting_results[i] = int(item.voter_count)
                i += 1
            max_date = meeting_results[0:4].index(max(meeting_results[0:4]))
            max_time = meeting_results[4:].index(max(meeting_results[4:])) + 4
            curr_meeting_poll['max_date'], curr_meeting_poll['max_time'] = max_date, max_time
            with open(constants.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
                meeting_file.write(json.dumps(curr_meeting_poll))
            log('Приглашение на общий созвон будет отправлено' + constants.meeting_options[max_time] + constants.meeting_options[max_date][4:])
            poll_results_msg = bot.send_message(secret.tg_chat_id,
                                                'Шоблятки, созвон на этой неделе будет в' + constants.meeting_options[max_date][4:] + ' ' + constants.meeting_options[max_time],
                                                parse_mode='Markdown')
            bot.pin_chat_message(secret.tg_chat_id, poll_results_msg.message_id, disable_notification=False)
    except Exception as poll_results_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[29], poll_results_error))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции poll_results:\nСообщение: *{0}\nТекст ошибки:\n{1}'.format(poll, poll_results_error))


# # # # # # Получаение file_id медиа файлов # # # # # #
@bot.message_handler(content_types=['photo', 'voice', 'document', 'animation'])
def send_media_id(message):
    try:
        if message.chat.id == secret.apple_id:
            if message.photo:
                bot.send_message(secret.apple_id, message.photo[2].file_id)
            elif message.voice:
                bot.send_message(secret.apple_id, message.voice.file_id)
            elif message.document:
                bot.send_message(secret.apple_id, message.document.file_id)
            elif message.animation:
                bot.send_message(secret.apple_id, message.animation.file_id)
    except Exception as send_media_id_error:
        bot.send_message(secret.apple_id, '❌ Ошибка в функции send_media_id:\nСообщение: {0}\nТекст ошибки:\n{1}'.format(message, send_media_id_error))


# # # # # # Обработка текста реплаев и # # # # # #
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        text = message.text
        match = re.search(r'(instagram\.com/reel/\S+)', message.text)
        if translitsky.isTranslitsky(text) and text[0:4] != 'http':
            answer = translitsky.doTranslitskyRollback(text)
            bot.send_message(message.chat.id, "`{}`".format(answer), parse_mode='Markdown', reply_to_message_id=message.message_id)
            update_activity('transl')
        # Если это попытка запинить сообщение
        if message.reply_to_message is not None and text == '@shoblabot' and message.chat.id == secret.tg_chat_id:
            try:
                bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id, disable_notification=False)
                log('пин сообщения by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
                update_activity('pin')
            except Exception as pin_error:
                log('{0}\nТекст ошибки: {1}'.format(constants.errors[26], pin_error))
                send_error(message, 26, pin_error)
        # Если это реплай на сообщение бота
        elif message.reply_to_message is not None and message.reply_to_message.from_user.id == secret.bot_id:
            # Если вводится текст для опроса
            if message.reply_to_message.text == constants.enter_question_new or message.reply_to_message.text == constants.too_large_question:
                try:
                    if len(text) <= 291:
                        poll_text = constants.tg_names[constants.tg_ids.index(message.from_user.id)] + ': ' + text
                        poll = bot.send_poll(secret.tg_chat_id, poll_text, constants.poll_options, is_anonymous=False, allows_multiple_answers=False)
                        stop_button = telebot.types.InlineKeyboardButton(text='Остановить опрос 🚫',
                                                                         callback_data='stop_{0}_{1}'.format(poll.message_id, message.from_user.id))
                        keyboard_opros_stop = telebot.types.InlineKeyboardMarkup(row_width=1)
                        keyboard_opros_stop.add(stop_button)
                        bot.delete_message(secret.tg_chat_id, message.reply_to_message.message_id)
                        bot.edit_message_reply_markup(secret.tg_chat_id, poll.message_id, reply_markup=keyboard_opros_stop)
                        bot.delete_message(secret.tg_chat_id, message.message_id)
                        bot.pin_chat_message(secret.tg_chat_id, poll.message_id, disable_notification=False)
                        log('создан опрос by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
                        update_activity('opros')
                    else:
                        force_reply = telebot.types.ForceReply(True)
                        bot.delete_message(secret.tg_chat_id, message.reply_to_message.message_id)
                        bot.send_message(message.chat.id, constants.too_large_question, reply_to_message_id=message.message_id, reply_markup=force_reply)
                except Exception as poll_reply_error:
                    log('{0}\nТекст ошибки: {1}'.format(constants.errors[19], poll_reply_error))
                    send_error(message, 19, poll_reply_error)
            # Если вводится вопрос к нейронке
            elif message.reply_to_message.text == constants.enter_question_gpt:
                try:
                    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo-16k', messages=[{"role": "user", "content": message.text}], stream=False)
                    bot.send_message(message.chat.id, response, parse_mode='Markdown')
                except Exception as g4f_error:
                    log('{0}\nТекст ошибки: {1}'.format(constants.errors[32], g4f_error))
                    send_error(message, 32, g4f_error)
        # Если это ссылка из Instagram
        elif match:
            new_url = re.sub(r'instagram\.com', 'ddinstagram.com', match.group(1))  # Заменяем домен на ddinstagram.com
            bot.send_message(message.chat.id, new_url, reply_to_message_id=message.message_id)  # Отправляем сообщение с новой ссылкой
    except Exception as send_text_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[20], send_text_error))
        send_error(message, 20, send_text_error)


# # # # # # Обработчик Call Back Data # # # # # #
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    try:
        # Кнопка остановки опроса
        if call.data[0:4] == 'stop':
            message_id = int(call.data.split('_')[1])
            user_id = int(call.data.split('_')[2])
            try:
                bot.stop_poll(secret.tg_chat_id, message_id) if call.from_user.id == user_id else bot.answer_callback_query(call.id, constants.wrong_stop, show_alert=True)
            except Exception as stop_opros_error:
                log('{0}\nТекст ошибки: {1}'.format(constants.errors[22], stop_opros_error))
                send_error(call.message, 22, stop_opros_error)
        # Обработка запроса скидок
        elif call.data[0:4] == 'disc':
            discount_id = int(call.data.split('_')[1])
            buttons_text = constants.buttons[0][0:discount_id] + constants.buttons[0][discount_id + 1:len(constants.buttons[0])]
            buttons_callback_data = constants.buttons[1][0:discount_id] + constants.buttons[1][discount_id + 1:len(constants.buttons[1])]
            keyboard_update = telebot.types.InlineKeyboardMarkup(row_width=2)
            i = 0
            while i < len(constants.buttons[0]) - 2:
                keyboard_update.add(telebot.types.InlineKeyboardButton(text=buttons_text[i], callback_data=buttons_callback_data[i]),
                                    telebot.types.InlineKeyboardButton(text=buttons_text[i + 1], callback_data=buttons_callback_data[i + 1]))
                i += 2
            # keyboard_update.add(constants.discounts, constants.channel)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=constants.buttons[2][discount_id],
                                  parse_mode='Markdown', reply_markup=keyboard_update)
    except Exception as callback_buttons_error:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[3], callback_buttons_error))
        send_error(call.message, 3, callback_buttons_error)


# # # # # # Отправка запланированных сообщений # # # # # #
def sdr():
    global curr_meeting_poll
    global activity_count
    try:
        threading.Timer(3600, sdr).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
        # Отправка предупреждения о загрузке оперативной памяти
        if psutil.virtual_memory()[2] > 80:
            bot.send_message(secret.apple_id, '‼️ Oh shit, attention ‼️\n💾 Used RAM: {0}%'.format(psutil.virtual_memory()[2]), parse_mode='Markdown')
        # Отправка статистики 1ого чиса месяца
        now_time = datetime.datetime.now()
        dr = str(now_time.day) + '.' + str(now_time.month)
        i = 0
        if os.path.isfile(constants.meeting_file):
            with open(constants.meeting_file, 'r') as meeting_file:
                curr_meeting_poll = json.loads(meeting_file.read())
        if now_time.hour != 9:
            if now_time.weekday() - 3 == curr_meeting_poll['max_date'] and now_time.hour - 13 == curr_meeting_poll['max_time'] and curr_meeting_poll['first_poll'] == 1:
                reminder = bot.send_message(secret.tg_chat_id, 'Сегодня шоблосозвон будет через час. Ожидайте ссылку.', parse_mode='Markdown')
                bot.pin_chat_message(secret.tg_chat_id, reminder.message_id, disable_notification=False)
                log('Отправлено напоминание на общий созвон')
            if now_time.weekday() - 3 == curr_meeting_poll['max_date'] and now_time.hour - 14 == curr_meeting_poll['max_time'] and curr_meeting_poll['first_poll'] == 1:
                photo = bot.send_photo(secret.tg_chat_id, constants.meeting_pic, caption='*Го созвон: *' + constants.meeting_link, parse_mode='Markdown')
                bot.pin_chat_message(secret.tg_chat_id, photo.message_id, disable_notification=False)
                curr_meeting_poll['first_poll'] = 0  # Флаг, что это первый опрос в этом месяце
                with open(constants.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
                    meeting_file.write(json.dumps(curr_meeting_poll))
                log('Отправлено приглашение на общий созвон')
            return
        else:
            if now_time.weekday() == 3 and now_time.day <= 7:  # День (четверг) для отправки опроса о принятии участия в созвоне
                meeting_poll = bot.send_poll(secret.tg_chat_id, constants.opros, constants.meeting_options, is_anonymous=False, allows_multiple_answers=True)
                bot.pin_chat_message(secret.tg_chat_id, meeting_poll.message_id, disable_notification=False)
                curr_meeting_poll['msg_id'] = meeting_poll.id
                curr_meeting_poll['poll_id'] = meeting_poll.poll.id
                curr_meeting_poll['max_date'] = 10
                curr_meeting_poll['max_time'] = 10
                curr_meeting_poll['first_poll'] = 1  # Флаг, что это первый опрос в этом месяце
                with open(constants.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
                    meeting_file.write(json.dumps(curr_meeting_poll))
            if now_time.weekday() == 4 and now_time.day <= 7:  # День (пятница) для остановки опроса о принятии участия в созвоне
                if os.path.isfile(constants.meeting_file):
                    with open(constants.meeting_file, 'r') as meeting_file:
                        curr_meeting_poll = json.loads(meeting_file.read())
                try:
                    bot.stop_poll(secret.tg_chat_id, curr_meeting_poll['msg_id'])
                except Exception as stop_poll_error:
                    log('Ошибка при закрытии опроса в sdr:\nТекст ошибки: ' + str(stop_poll_error))
                    bot.send_message(secret.apple_id, '❌ Ошибка при закрытии опроса в sdr\nТекст ошибки:\n' + str(stop_poll_error))
            if now_time.day == 1:  # День для статистики по боту выкладывания фоток за месяц Месечная десятка челлендж
                # Загружаем данные из файла activity_count
                cur_month = str(now_time.year - 1) + '.12' if now_time.month == 1 else str(now_time.year) + '.' + str(now_time.month - 1)
                if os.path.isfile(constants.activity_file):
                    with open(constants.activity_file, 'r') as activity_file:
                        activity_count = json.loads(activity_file.read())
                month_statistics = constants.month_statistics.format(activity_count[cur_month]['opros'], activity_count[cur_month]['discount'],
                                                                     activity_count[cur_month]['car_girl'], activity_count[cur_month]['hey_doc'],
                                                                     activity_count[cur_month]['pin'], activity_count[cur_month]['rapid_new'],
                                                                     activity_count[cur_month]['cyk'], activity_count[cur_month]['russia'],
                                                                     activity_count[cur_month]['team'], activity_count[cur_month]['start'],
                                                                     activity_count[cur_month]['help'], activity_count[cur_month]['who'],
                                                                     activity_count[cur_month]['rapid'], activity_count[cur_month]['/29'],
                                                                     activity_count[cur_month]['kirov'], activity_count[cur_month]['damage'],
                                                                     activity_count[cur_month]['meeting'], activity_count[cur_month]['transl'],
                                                                     activity_count[cur_month]['mamma'], activity_count[cur_month]['usd'],
                                                                     activity_count[cur_month]['yapoznaumir'])
                bot.send_message(secret.tg_chat_id, month_statistics, parse_mode='Markdown')
                # Рассылка по 10челлендж
                challenge = bot.send_message(secret.tg_chat_id, '📸 Шоблятки, время для #10челлендж и ваших фоточек за месяц!', parse_mode='Markdown')
                bot.pin_chat_message(secret.tg_chat_id, challenge.message_id, disable_notification=False)
            if dr == str(28.5):  # День Баяна в Шобле отмечается 28 мая
                bot.send_photo(secret.tg_chat_id, 'AgACAgIAAxkBAAJFzWLeYTbQ2ENcXEwoPOrRZprGCCUUAALHuTEb6BT4ShJZvIDQxNjZAQADAgADcwADKQQ', caption='🪗 Шобла, поздравляю с Днём Баяна!')
            if dr == str(24.11):  # День Рождения бота
                bot.send_message(secret.tg_chat_id, '🥳 Сегодня ботику уже *{0} лет*!'.format(now_time.year - 2016), parse_mode='Markdown')
            # Отправка поздравлений с ДР
            for item in constants.tg_drs:
                if item[:-5] == dr and now_time.hour == 9:
                    if (now_time.year - int(item[-4:])) % 10 == 0:
                        bot.send_message(secret.tg_chat_id, '🥳 [{0}](tg://user?id={1}), с др!\nДобро пожаловать в клуб кому '
                                                            'за {2} 😏'.format(constants.tg_names[i], constants.tg_ids[i], now_time.year - int(item[-4:])),
                                         parse_mode='Markdown')
                    else:
                        bot.send_message(secret.tg_chat_id, '🥳 [{0}](tg://user?id={1}), с др!'.format(constants.tg_names[i], constants.tg_ids[i]), parse_mode='Markdown')
                i += 1
    except Exception as sdr_error:
        log('Ошибка в функции отправки поздравления в Шоблу sdr:\nТекст ошибки: ' + str(sdr_error))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции отправки поздравления в Шоблу sdr\nТекст ошибки:\n' + str(sdr_error))


# # # # # # Запуск функций # # # # # #
try:
    sdr()
except Exception as e:
    log('Ошибка при запуске sdr:\nТекст ошибки: ' + str(e))
    bot.send_message(secret.apple_id, '❌ Ошибка при запуске sdr\nТекст ошибки:\n' + str(e))

try:
    log('Попытка запуска bot.infinity_polling()')
    bot.infinity_polling()
except Exception as e:
    with open(constants.log_file, 'a') as log_file_stream:
        traceback.print_exc(file=log_file_stream)
    log('Ошибка при запуске bot.polling:\nТекст ошибки: ' + str(e))
    bot.send_message(secret.apple_id, '❌ Ошибка при запуске bot.polling\nТекст ошибки:\n' + str(e))

try:
    with open(constants.log_file, 'a') as log_file_flow:
        log_file_flow.write('\nSTART\n' + time.ctime(time.time()) + ' - время запуска бота\n')
except Exception as e:
    bot.send_message(secret.apple_id, '❌ Ошибка при логировании start_time:\nТекст ошибки:\n' + str(e))
