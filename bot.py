#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
# # # # # # Импортозамещение # # # # # #
import telebot  # Библиотека piTelegramBotAPI
import re  # Для поиска ссылки в тексте
import json  # Представляет словарь в строку
import time  # Для представления времени в читаемом формате
import random  # Присвятой рандом
import urllib.request as urllib2  # Для Кирюхиного Rapid'a
from urllib.parse import quote  # ---//---
import traceback  # Для записи в лог файл при траблах бота
import constants  # Файл с константами
import secret  # Файл с токенами
import helpers.keyboards as keyboards  # Файл с клавиатурами
import helpers.service_func as service_func  # Файл со служебными функциями
import helpers.faggot as faggot  # Файл для функции faggot handler
import helpers.find_words as find_words  # Файл для функции kirov
import helpers.cbr as cbr  # Файл для команды запросв курса рубля
import helpers.scheduled_messages as scheduled_messages  # Файл для функции отправки сообщений по расписанию
import ffmpeg  # Для .mov to .webm конвертора


# # # # # # Инициализация # # # # # #
bot = telebot.TeleBot(secret.bot_token)  # Token бота
bot.set_my_commands([
    telebot.types.BotCommand('/discount', '🤑Скидки'),
    telebot.types.BotCommand('/usd', '💵 Курс рубля'),
    telebot.types.BotCommand('/who', '✅❌Создать опрос'),
    telebot.types.BotCommand('/rapid', '✅ Зеленый Rapid'),
    telebot.types.BotCommand('/meeting', '🎧Ссылка шоблодискорда'),
    telebot.types.BotCommand('/help', '❓Полезная информация')
])


# # # # # # Доступные команды # # # # # #
# Вызов информации о сервере и пересылка сообщения в Шоблу (доступно только Аполу)
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.from_user.id == secret.apol_id:  # Это Апол
            service_func.server_status(bot, message)
        else:
            service_func.log(bot, f'вызов команды {message.text}\n{constants.errors[4]}: '
                                  f'User ID - {message.from_user.id}, user_name - @{message.from_user.username}')
    except Exception as server_info_error:
        service_func.send_error(bot, message, 4, server_info_error)


# Вызов стартового сообщения / справки
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    try:
        if message.chat.id == secret.shobla_id or message.from_user.id in secret.shobla_member:  # Это Шобла или человек из Шоблы
            service_func.log(bot, f'вызов команды {message.text} by {secret.shobla_member[message.from_user.id]["name"]}')
            bot.send_message(message.chat.id, constants.help_text, reply_markup=keyboards.help_keyboard, parse_mode='Markdown')
        else:
            service_func.log(bot, f'вызов команды {message.text}\n{constants.errors[0 if len(message.text) == 6 else 1]}: '
                                  f'User ID - {message.from_user.id}, user_name - @{message.from_user.username}')
    except Exception as handle_start_help_error:
        service_func.send_error(bot, message, 0 if message.text == '/start' else 1, handle_start_help_error)


# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        if message.chat.id == secret.shobla_id:  # Это Шобла
            service_func.log(bot, f'вызов команды /who by {secret.shobla_member[message.from_user.id]["name"]}')
            bot.send_message(secret.shobla_id, constants.enter_question_new, reply_to_message_id=message.message_id, reply_markup=telebot.types.ForceReply(True))
            bot.delete_message(secret.shobla_id, message.message_id)
        elif message.from_user.id in secret.shobla_member:  # Это человек из Шоблы
            bot.send_message(message.chat.id, '❌ Опрос создается только в Шобле', parse_mode='Markdown')
    except Exception as who_will_error:
        service_func.send_error(bot, message, 7, who_will_error)


# Отправка скидок
@bot.message_handler(commands=['discount'])
def send_discount(message):
    try:
        if message.from_user.id in secret.shobla_member:  # Это человек из Шоблы
            service_func.log(bot, f'вызов команды /discount by {secret.shobla_member[message.from_user.id]["name"]}')
            bot.send_message(message.chat.id, keyboards.buttons[2][1], reply_markup=keyboards.keyboard_start, parse_mode='Markdown')
    except Exception as send_discount_error:
        service_func.send_error(bot, message, 8, send_discount_error)


# Запрос отправки логов по боту
@bot.message_handler(commands=['log'])
def share_log(message):
    try:
        if message.from_user.id in secret.shobla_member:  # Это человек из Шоблы
            service_func.log(bot, f'вызов команды /log by {secret.shobla_member[message.from_user.id]["name"]}')
            bot.send_document(message.chat.id, open(secret.log_file, 'rb'), caption='🤖📋 Log file')
    except Exception as share_log_error:
        service_func.send_error(bot, message, 24, share_log_error)


# Запрос на ссылку созвона
@bot.message_handler(commands=['meeting'])
def meeting(message):
    try:
        if message.from_user.id in secret.shobla_member:  # Это человек из Шоблы
            service_func.log(bot, f'вызов команды /meeting by {secret.shobla_member[message.from_user.id]["name"]}')
            bot.send_photo(message.chat.id, constants.meeting_pic, caption=f'🤖 *Го созвон*\n{constants.meeting_link}', parse_mode='Markdown')
    except Exception as meeting_error:
        service_func.send_error(bot, message, 28, meeting_error)


# Запрос курса рубля
@bot.message_handler(commands=['usd'])
def usd(message):
    try:
        if message.from_user.id in secret.shobla_member:  # Это человек из Шоблы
            service_func.log(bot, f'вызов команды /usd by {secret.shobla_member[message.from_user.id]["name"]}')
            usa_dol, eur, geo_lar, kaz_ten, date = cbr.get_exchange_rates()
            bot.send_photo(message.chat.id, constants.usd_pic[random.randint(0, len(constants.usd_pic) - 1)],
                           caption=(f'💵 *Курс рубля по данным сайта* [ЦБР](https://www.cbr.ru/currency_base/daily/) *на {date}*:\n'
                                    f'`🇺🇸 1$ = {usa_dol}₽`\n`🇪🇺 1€ = {eur}₽`\n`🇬🇪 1₾ = {geo_lar}₽`\n`🇰🇿 100₸ = {kaz_ten}₽`'), parse_mode='Markdown')
    except Exception as usd_error:
        service_func.send_error(bot, message, 31, usd_error)


# Команда на анпин сообщения в шобле
@bot.message_handler(commands=['unpin'])
def unpin(message):
    try:
        if message.reply_to_message is not None and message.from_user.id in secret.shobla_member:  # Это человек из Шоблы
            bot.unpin_chat_message(chat_id=secret.shobla_id, message_id=message.reply_to_message.message_id)
            bot.delete_message(secret.shobla_id, message.message_id)
    except Exception as unpin_error:
        service_func.send_error(bot, message, 32, unpin_error)


# # # # # # Обработка текста # # # # # #
# Обработка девки за рулем
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace('a', '').replace('а', '') == '' and message.chat.id == secret.shobla_id)
def aaa(message):
    try:
        bot.send_message(secret.shobla_id, 'Девка за рулём') if len(message.text) > 2 else bot.send_message(secret.shobla_id, 'Двк з рлм')
    except Exception as aaa_error:
        service_func.send_error(bot, message, 9, aaa_error)


# Обработка Emotional damage
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.damage and message.chat.id == secret.shobla_id)
def damage(message):
    try:
        bot.send_voice(secret.shobla_id, constants.emotional_damage_voice_id)
    except Exception as damage_error:
        service_func.send_error(bot, message, 10, damage_error)


# Обработка mamma mia
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.mammamia and message.chat.id == secret.shobla_id)
def mamma_mia(message):
    try:
        audio = open(secret.mamma_audio_path, 'rb')
        bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)
    except Exception as mamma_mia_error:
        service_func.send_error(bot, message, 30, mamma_mia_error)


# Обработка РАСИЯ
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.russia and message.chat.id == secret.shobla_id)
def russia(message):
    try:
        bot.send_voice(secret.shobla_id, constants.anthem, '🫡')
    except Exception as russia_error:
        service_func.send_error(bot, message, 11, russia_error)


# Обработка врача
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.hey_doc and message.chat.id == secret.shobla_id)
def hey_doc(message):
    try:
        bot.send_document(secret.shobla_id, constants.hey_doc_gif_id, caption='@oxy_genium')
    except Exception as hey_doc_error:
        service_func.send_error(bot, message, 12, hey_doc_error)


# Обработка @team
@bot.message_handler(func=lambda message: message.text and constants.team in message.text.lower() and message.chat.id == secret.shobla_id)
def team(message):
    try:
        bot.send_message(chat_id=secret.shobla_id, disable_notification=False, reply_to_message_id=message.message_id,
                         text=constants.team_text, disable_web_page_preview=True, parse_mode='Markdown')
    except Exception as team_error:
        service_func.send_error(bot, message, 14, team_error)


# Обработка @rapid
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith('/rapid') and message.chat.id == secret.shobla_id)
def rapid(message):
    value = ''
    try:
        service_func.log(bot, f'вызов команды /rapid by {secret.shobla_member[message.from_user.id]["name"]}')
        # Сплитуем строку выпилив предварительно ненужные пробелы по бокам
        data = message.text.lower().strip().split(' ')
        '''Получаем количество элементов сплитованой строки
        и если тока 1 элемент то значит аргумент не передали
        следовательно help по дефолту '''
        size = len(data)
        value = 'help' if size == 1 else data[1]
        # Ну тут почти без изменений, тока data[1] became value
        response = urllib2.urlopen(f'https://rapid.zhuykovkb.ru/rapid?data={quote(value)}&memberid={message.from_user.id}')
        answer = json.loads(str(response.read(), 'utf-8'))
        bot.send_message(secret.shobla_id, answer['message'], parse_mode='Markdown')
        service_func.log(bot, f'добавлен новый номер Рапида by {secret.shobla_member[message.from_user.id]["name"]}')
    except Exception as rapid_error:
        bot.send_message(secret.zhuykovkb_id, f'Ошибка в функции rapid:\n\nДанные: {quote(value)}\n\nТекст ошибки {rapid_error}')
        service_func.send_error(bot, message, 15, f'{rapid_error}\nДанные: {quote(value)}')


# Обработка барсука
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.suk and message.chat.id == secret.shobla_id)
def badger(message):
    try:
        bot.send_message(secret.shobla_id, 'Бар'+message.text.lower())
    except Exception as badger_error:
        service_func.send_error(bot, message, 16, badger_error)


# Обработка каждого сообщения на гея/лешу
@bot.message_handler(func=lambda message: True and find_words.word_in_message(message.text, constants.faggot_list))
def faggot_func(message):
    try:
        if random.random() < 0.3:
            eu_country = faggot.getFaggotEUCountryRequest(message.text, constants.faggot_list)
            if eu_country[0]:
                location = eu_country[1]['coords']
                bot.reply_to(message, 'Ты что то сказал про гея? Держи...')
                bot.send_location(message.chat.id, location['lat'], location['lng'])
    except Exception as faggot_func_error:
        service_func.send_error(bot, message, 25, faggot_func_error)


# Обработка Кирова
@bot.message_handler(func=lambda message: True and find_words.word_in_message(message.text, constants.kirov))
def kirov(message):
    try:
        audio = open(secret.kirov_audio_path, 'rb')
        bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)
    except Exception as kirov_error:
        service_func.send_error(bot, message, 27, kirov_error)


# Обработка Аня_кек
@bot.message_handler(func=lambda message: True and find_words.word_in_message(message.text, constants.annet_kek))
def annet(message):
    try:
        bot.send_video(secret.shobla_id, constants.annet_video, reply_to_message_id=message.message_id)
    except Exception as annet_error:
        service_func.send_error(bot, message, 37, annet_error)


# # # # # # Получаение file_id медиа файлов # # # # # #
@bot.message_handler(content_types=['photo', 'voice', 'document', 'animation', 'video'])
def send_media_id(message):
    try:
        if message.chat.id == secret.apol_id:
            if message.photo:
                bot.send_message(secret.apol_id, message.photo[2].file_id)
            elif message.voice:
                bot.send_message(secret.apol_id, message.voice.file_id)
            elif message.document:
                bot.send_message(secret.apol_id, message.document.file_id)
                bit_rate = '1M'
                if message.caption:
                    bit_rate = message.caption
                if '.MP4' or '.MOV' in message.document.file_name:
                    file_path = bot.get_file(message.document.file_id).file_path
                    file = bot.download_file(file_path)
                    with open(secret.input_file, 'wb+') as file_flow:
                        file_flow.write(file)
                    ffmpeg.input(secret.input_file).output(secret.output_file, vcodec='libvpx-vp9', vf='scale=512:-2', b=bit_rate, an=None, loglevel="quiet").run(overwrite_output=True)
                    output_file = open(secret.output_file, 'rb')
                    bot.send_document(message.chat.id, output_file)
            elif message.animation:
                bot.send_message(secret.apol_id, message.animation.file_id)
            elif message.video:
                bot.send_message(secret.apol_id, message.video.file_id)
    except Exception as send_media_id_error:
        service_func.send_error(bot, message, 33, send_media_id_error)


# # # # # # Обработчик Call Back Data # # # # # #
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    try:
        keyboards.button_func(bot, call)
    except Exception as callback_buttons_error:
        service_func.send_error(bot, call.message, 3, callback_buttons_error)


# # # # # # Обработка текста реплаев и # # # # # #
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        text = message.text
        match = re.search(r'(instagram\.com/\S+)', message.text)
        # Если это попытка запинить сообщение
        if message.reply_to_message is not None and text == '@shoblabot' and message.chat.id == secret.shobla_id:
            try:
                bot.pin_chat_message(chat_id=secret.shobla_id, message_id=message.reply_to_message.message_id, disable_notification=False)
                service_func.log(bot, f'пин сообщения by {secret.shobla_member[message.from_user.id]["name"]}')
            except Exception as pin_error:
                service_func.send_error(bot, message, 26, pin_error)
        # Если это реплай на сообщение бота
        elif message.reply_to_message is not None and message.reply_to_message.from_user.id == secret.bot_id:
            # Если вводится текст для опроса
            if message.reply_to_message.text == constants.enter_question_new or message.reply_to_message.text == constants.too_large_question:
                try:
                    if len(text) <= 291:
                        poll_text = f'{secret.shobla_member[message.from_user.id]["name"]}: {text}'
                        poll = bot.send_poll(secret.shobla_id, poll_text, constants.poll_options, is_anonymous=False, allows_multiple_answers=False)
                        stop_button = telebot.types.InlineKeyboardButton(text='Остановить опрос 🚫', callback_data=f'stop_{poll.message_id}_{message.from_user.id}')
                        keyboard_opros_stop = telebot.types.InlineKeyboardMarkup(row_width=1)
                        keyboard_opros_stop.add(stop_button)
                        bot.delete_message(secret.shobla_id, message.reply_to_message.message_id)
                        bot.edit_message_reply_markup(secret.shobla_id, poll.message_id, reply_markup=keyboard_opros_stop)
                        bot.delete_message(secret.shobla_id, message.message_id)
                        bot.pin_chat_message(secret.shobla_id, poll.message_id, disable_notification=False)
                        service_func.log(bot, f'создан опрос by {secret.shobla_member[message.from_user.id]["name"]}')
                    else:
                        force_reply = telebot.types.ForceReply(True)
                        bot.delete_message(secret.shobla_id, message.reply_to_message.message_id)
                        bot.send_message(message.chat.id, constants.too_large_question, reply_to_message_id=message.message_id, reply_markup=force_reply)
                except Exception as poll_reply_error:
                    service_func.send_error(bot, message, 19, poll_reply_error)
        # Если это ссылка из Instagram
        elif match:
            new_url = re.sub(r'instagram\.com', 'ddinstagram.com', match.group(1))  # Заменяем домен на ddinstagram.com
            bot.send_message(message.chat.id, new_url, reply_to_message_id=message.message_id)  # Отправляем сообщение с новой ссылкой
    except Exception as send_text_error:
        service_func.send_error(bot, message, 20, send_text_error)


# # # # # # Запуск функций # # # # # #
try:
    scheduled_messages.send_message(bot)
except Exception as e:
    bot.send_message(secret.apol_id, f'❌ Ошибка при запуске scheduled_messages.send_message\nТекст ошибки:\n{e}')
    service_func.log(bot, f'❌ Ошибка при запуске scheduled_messages.send_message\nТекст ошибки:\n{e}')

try:
    service_func.log(bot, 'Попытка запуска bot.infinity_polling()')
    bot.infinity_polling()
except Exception as e:
    service_func.log(bot, f'Ошибка при запуске bot.polling:\nТекст ошибки:\n{e}')
    with open(secret.log_file, 'a') as log_file_stream:
        traceback.print_exc(file=log_file_stream)
    bot.send_message(secret.apol_id, f'❌ Ошибка при запуске bot.polling:\nТекст ошибки:\n{e}')

try:
    with open(secret.log_file, 'a') as log_file_flow:
        log_file_flow.write(f'\nSTART\n{time.ctime(time.time())} - время запуска бота\n')
except Exception as e:
    bot.send_message(secret.apol_id, f'❌ Ошибка при логировании start_time:\nТекст ошибки:\n{e}')
