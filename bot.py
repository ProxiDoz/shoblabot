#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# # # # # # Импортозамещение # # # # # #
import telebot  # Библиотека piTelegramBotAPI
import json  # Представляет словарь в строку
from datetime import datetime  # Для представления времени в читаемом формате
import random  # Присвятой рандом
import urllib.request  # Для Кирюхиного Rapid'a
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
from helpers.service_func import handler_error  # Импорт декоратора ошибок
import os  # Для прокси


# # # # # # Инициализация # # # # # #
def apply_socks_proxy():
    """Configure SOCKS5 proxy for the whole process via env."""
    use_proxy = os.getenv("PROXY_SOCKS5_USE", "false").lower() == "true"
    if not use_proxy:
        return

    host = 'shackoor.fvds.ru'
    port = '52308'

    if not host or not port:
        print("Proxy enabled but PROXY_SOCKS5_HOST/PORT not set")
        return

    proxy = f"socks5h://{host}:{port}"

    os.environ["ALL_PROXY"] = proxy
    os.environ["HTTP_PROXY"] = proxy
    os.environ["HTTPS_PROXY"] = proxy

    print(f"[Proxy] SOCKS5 {host}:{port} enabled")


apply_socks_proxy()
bot = telebot.TeleBot(secret.bot_token)  # Token бота
bot.set_my_commands([
    telebot.types.BotCommand('/discount', '🤑Скидки'),
    telebot.types.BotCommand('/usd', '💵 Курс рубля'),
    telebot.types.BotCommand('/who', '✅❌Создать опрос'),
    telebot.types.BotCommand('/rapid', '✅ Зеленый Rapid'),
    telebot.types.BotCommand('/meeting', '🎧Ссылка шоблодискорда'),
    telebot.types.BotCommand('/help', '❓Полезная информация')
])


# Это человек из Шоблы или чат Шоблы
def is_shobla_member(message):
    return message.from_user.id in secret.shobla_member


def is_shobla_chat(message):
    return message.chat.id == secret.shobla_id


# Сокращаем сообщение
def normalize(text):
    return text.lower().replace(' ', '').replace('\n', '')


# # # # # # Доступные команды # # # # # #
# Вызов информации о сервере и пересылка сообщения в Шоблу (доступно только Аполу)
@bot.message_handler(commands=['s'])
@handler_error(0)
def server_info(message):
    if message.from_user.id == secret.apol_id:  # Это Апол
        service_func.server_status(bot, message)


# Вызов стартового сообщения / справки
@bot.message_handler(commands=['start', 'help'])
@handler_error(1)
def handle_start_help(message):
    if is_shobla_chat(message) or is_shobla_member(message):  # Это Шобла или человек из Шоблы
        service_func.log(bot, message, f'вызов команды {message.text}')
        bot.send_message(message.chat.id, constants.help_text, reply_markup=keyboards.help_keyboard, parse_mode='Markdown')
    else:
        service_func.start_log(bot, f'вызов команды {message.text}\n{constants.errors[0 if len(message.text) == 6 else 1]}: '
                                    f'User ID - {message.from_user.id}, user_name - @{message.from_user.username}')


# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
@handler_error(2)
def who_will(message):
    if is_shobla_chat(message):  # Это Шобла
        service_func.log(bot, message, 'вызов команды /who')
        bot.send_message(secret.shobla_id, constants.enter_question_new, reply_to_message_id=message.message_id, reply_markup=telebot.types.ForceReply(True))
        bot.delete_message(secret.shobla_id, message.message_id)
    elif message.from_user.id in secret.shobla_member:  # Это человек из Шоблы
        bot.send_message(message.chat.id, '❌ Опрос создается только в Шобле', parse_mode='Markdown')


# Отправка скидок
@bot.message_handler(commands=['discount'])
@handler_error(3)
def send_discount(message):
    if is_shobla_member(message):  # Это человек из Шоблы
        service_func.log(bot, message, 'вызов команды /discount')
        bot.send_message(message.chat.id, keyboards.buttons[2][2], reply_markup=keyboards.keyboard_start, parse_mode='Markdown')


# Запрос отправки логов по боту
@bot.message_handler(commands=['log'])
@handler_error(4)
def share_log(message):
    if is_shobla_member(message):  # Это человек из Шоблы
        service_func.log(bot, message, 'вызов команды /log')
        bot.send_document(message.chat.id, open(secret.log_file, 'rb'), caption='🤖📋 Log file')


# Запрос на ссылку созвона
@bot.message_handler(commands=['meeting'])
@handler_error(5)
def meeting(message):
    if is_shobla_member(message):  # Это человек из Шоблы
        service_func.log(bot, message, 'вызов команды /meeting')
        bot.send_photo(message.chat.id, constants.meeting_pic, caption=f'🤖 *Го созвон*\n{constants.meeting_link}', parse_mode='Markdown')


# Запрос курса рубля
@bot.message_handler(commands=['usd'])
@handler_error(6)
def usd(message):
    if is_shobla_member(message):  # Это человек из Шоблы
        service_func.log(bot, message, 'вызов команды /usd')
        usa_dol, eur, geo_lar, kaz_ten, date = cbr.get_exchange_rates()
        bot.send_photo(message.chat.id, random.choice(constants.usd_pic),
                       caption=(f'💵 *Курс рубля по данным сайта* [ЦБР](https://www.cbr.ru/currency_base/daily/) *на {date}*:\n'
                                f'`🇺🇸 1$ = {usa_dol}₽`\n`🇪🇺 1€ = {eur}₽`\n`🇬🇪 1₾ = {geo_lar}₽`\n`🇰🇿 100₸ = {kaz_ten}₽`'), parse_mode='Markdown')


# Команда на анпин сообщения в шобле
@bot.message_handler(commands=['unpin'])
@handler_error(7)
def unpin(message):
    if message.reply_to_message is not None and is_shobla_member(message):  # Это человек из Шоблы
        bot.unpin_chat_message(chat_id=secret.shobla_id, message_id=message.reply_to_message.message_id)
        bot.delete_message(secret.shobla_id, message.message_id)


# # # # # # Обработка текста # # # # # #
# Обработка девки за рулем
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace('a', '').replace('а', '') == '' and is_shobla_chat(message))
@handler_error(8)
def aaa(message):
    bot.send_message(secret.shobla_id, 'Девка за рулём') if len(message.text) > 2 else bot.send_message(secret.shobla_id, 'Двк з рлм')


# Обработка Emotional damage
@bot.message_handler(func=lambda message: message.text and normalize(message.text) in constants.damage and is_shobla_chat(message))
@handler_error(9)
def damage(message):
    bot.send_voice(secret.shobla_id, constants.emotional_damage_voice_id)


# Обработка mamma mia
@bot.message_handler(func=lambda message: message.text and normalize(message.text) in constants.mammamia and is_shobla_chat(message))
@handler_error(10)
def mamma_mia(message):
    with open(secret.mamma_audio_path, 'rb') as audio:
        bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)


# Обработка РАСИЯ
@bot.message_handler(func=lambda message: message.text and normalize(message.text) in constants.russia and is_shobla_chat(message))
@handler_error(11)
def russia(message):
    bot.send_voice(secret.shobla_id, constants.anthem, '🫡')


# Обработка врача
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.hey_doc and is_shobla_chat(message))
@handler_error(12)
def hey_doc(message):
    bot.send_document(secret.shobla_id, constants.hey_doc_gif_id, caption='@oxy_genium')


# Обработка барсука
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.suk and is_shobla_chat(message))
@handler_error(13)
def badger(message):
    bot.send_message(secret.shobla_id, 'Бар'+message.text.lower())


# Обработка @team
@bot.message_handler(func=lambda message: message.text and constants.team in message.text.lower() and is_shobla_chat(message))
@handler_error(14)
def team(message):
    bot.send_message(chat_id=secret.shobla_id, disable_notification=False, reply_to_message_id=message.message_id,
                     text=constants.team_text, disable_web_page_preview=True, parse_mode='Markdown')


# Обработка @rapid
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith('/rapid') and is_shobla_chat(message))
def rapid(message):
    value = ''
    try:
        service_func.log(bot, message, 'вызов команды /rapid')
        # Сплитуем строку выпилив предварительно ненужные пробелы по бокам
        data = message.text.lower().strip().split(' ')
        '''Получаем количество элементов сплитованой строки и если тока 1 элемент то значит аргумент не передали
        следовательно help по дефолту '''
        value = data[1] if len(data) > 1 else 'help'
        # Ну тут почти без изменений, тока data[1] became value
        response = urllib.request.urlopen(f'https://rapid.zhuykovkb.ru/rapid?data={quote(value)}&memberid={message.from_user.id}')
        answer = json.loads(str(response.read(), 'utf-8'))
        if answer['message'] == 'Номер успешно добавлен':
            bot.send_document(secret.shobla_id, constants.artyomed, caption=answer['message'])
        elif answer['message'] == 'Номер уже присутствует в базе':
            bot.send_document(secret.shobla_id, constants.not_artyomed, caption=answer['message'])
        else:
            bot.send_message(secret.shobla_id, answer['message'], parse_mode='Markdown')
        service_func.log(bot, message, 'добавлен новый номер Рапида')
    except Exception as rapid_error:
        bot.send_message(secret.zhuykovkb_id, f'Ошибка в функции rapid:\n\nДанные: {quote(value)}\n\nТекст ошибки {rapid_error}')
        service_func.send_error(bot, message, 15, f'{rapid_error}\nДанные: {quote(value)}')


# Обработка каждого сообщения на гея/лешу
@bot.message_handler(func=lambda message: find_words.word_in_message(message.text, constants.faggot_list) and is_shobla_chat(message))
@handler_error(16)
def faggot_func(message):
    if random.random() < 0.3:
        eu_country = faggot.getFaggotEUCountryRequest(message.text, constants.faggot_list)
        if eu_country[0]:
            location = eu_country[1]['coords']
            bot.reply_to(message, 'Ты что то сказал про гея? Держи...')
            bot.send_location(message.chat.id, location['lat'], location['lng'])


# Обработка Кирова
@bot.message_handler(func=lambda message: find_words.word_in_message(message.text, constants.kirov) and is_shobla_chat(message))
@handler_error(17)
def kirov(message):
    with open(secret.kirov_audio_path, 'rb') as audio:
        bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)


# Обработка Аня_кек
@bot.message_handler(func=lambda message: find_words.word_in_message(message.text, constants.annet_kek) and is_shobla_chat(message))
@handler_error(18)
def annet(message):
    bot.send_video(message.chat.id, constants.annet_video, reply_to_message_id=message.message_id)


# # # # # # Получаение file_id медиа файлов # # # # # #
@bot.message_handler(content_types=['photo', 'voice', 'document', 'animation', 'video'])
@handler_error(19)
def send_media_id(message):
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
            if message.document.file_name.lower().endswith(('.mp4', '.mov')):
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


# # # # # # Обработчик Call Back Data # # # # # #
@bot.callback_query_handler(func=lambda call: True)
@handler_error(20)
def callback_buttons(call):
    keyboards.button_func(bot, call)


# # # # # # Обработка текста реплаев и # # # # # #
@bot.message_handler(content_types=['text'])
@handler_error(21)
def send_text(message):
    text = message.text
    # Если это попытка запинить сообщение
    if message.reply_to_message is not None and text == '@shoblabot' and is_shobla_chat(message):
        try:
            bot.pin_chat_message(chat_id=secret.shobla_id, message_id=message.reply_to_message.message_id, disable_notification=False)
            service_func.log(bot, message, 'пин сообщения')
        except Exception as pin_error:
            service_func.send_error(bot, message, 22, pin_error)
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
                    service_func.log(bot, message, 'создан опрос')
                else:
                    force_reply = telebot.types.ForceReply(True)
                    bot.delete_message(secret.shobla_id, message.reply_to_message.message_id)
                    bot.send_message(message.chat.id, constants.too_large_question, reply_to_message_id=message.message_id, reply_markup=force_reply)
            except Exception as poll_reply_error:
                service_func.send_error(bot, message, 23, poll_reply_error)


# # # # # # Запуск функций # # # # # #
try:
    scheduled_messages.send_message(bot)
except Exception as e:
    bot.send_message(secret.apol_id, f'❌ Ошибка при запуске scheduled_messages.send_message\nТекст ошибки:\n{e}')
    service_func.start_log(bot, f'❌ Ошибка при запуске scheduled_messages.send_message\nТекст ошибки:\n{e}')

try:
    service_func.start_log(bot, 'Попытка запуска bot.infinity_polling()')
    bot.infinity_polling(timeout=30, long_polling_timeout=30, allowed_updates=None)
except Exception as e:
    service_func.start_log(bot, f'Ошибка при запуске bot.polling:\nТекст ошибки:\n{e}')
    with open(secret.log_file, 'a') as log_file_stream:
        traceback.print_exc(file=log_file_stream)
    bot.send_message(secret.apol_id, f'❌ Ошибка при запуске bot.polling:\nТекст ошибки:\n{e}')

try:
    with open(secret.log_file, 'a') as log_file_flow:
        log_file_flow.write(f'\nSTART\n{datetime.now()} - время запуска бота\n')
except Exception as e:
    bot.send_message(secret.apol_id, f'❌ Ошибка при логировании start_time:\nТекст ошибки:\n{e}')
