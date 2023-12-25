#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
# # # # # # Импортозамещение # # # # # #
import telebot                              # Библиотека piTelegramBotAPI
import re                                   # Для поиска ссылки в тексте
import g4f                                  # Для работы с нейронкой
import json                                 # Представляет словарь в строку
import time                                 # Для представления времени в читаемом формате
import datetime                             # ---//---
import random                               # Присвятой рандом
import threading                            # Для отсчета времени для отправки сообщений
import urllib.request as urllib2            # Для Кирюхиного Rapid'a
from urllib.parse import quote              # ---//---
import traceback                            # Для записи в лог файл при траблах бота
import constants                            # Файл с константами
import secret                               # Файл с токенами
import helpers.keyboards as keyboards       # Файл с клавиатурами
import helpers.service_func as service_func  # Файл со служебными функциями
import helpers.faggot as faggot             # Файл для функции faggot handler
import helpers.find_words as find_words     # Файл для функции kirov
import helpers.translitsky as translitsky   # Файл для функции транслитского
import helpers.cbr as cbr                   # Файл для команды запросв курса рубля

# # # # # # Инициализация # # # # # #
bot = telebot.TeleBot(secret.bot_token)  # Token бота
bot.set_my_commands([
    telebot.types.BotCommand('/discount', '🤑Скидки'),
    telebot.types.BotCommand('/usd', '💵 Курс рубля'),
    telebot.types.BotCommand('/who', '✅❌Создать опрос'),
    telebot.types.BotCommand('/help', '❓Полезная информация'),
    telebot.types.BotCommand('/meeting', '🎧Ссылка шоблосозвона'),
    telebot.types.BotCommand('/log', '📋Вывод логов бота'),
    telebot.types.BotCommand('/stat', '🤖Статистика по использованию бота'),
    telebot.types.BotCommand('/rapid', '✅ Зеленый Rapid'),
    telebot.types.BotCommand('/yapoznaumir', '🧐 Задай вопрос')
])
activity_count = {}  # Переменная для сбора статистики по командам
with open(constants.meeting_file, 'r') as lang:  # Переменная curr_meeting_poll для сбора данных по опросу
    curr_meeting_poll = json.loads(lang.read())


# # # # # # Доступные команды # # # # # #
# Вызов информации о сервере и пересылка сообщения в Шоблу (доступно только Аполу)
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.from_user.id == secret.apol_id:  # Это Апол
            service_func.server_status(bot, message)
        else:
            service_func.send_error(bot, message, 6, 'Вызов команды /s')
    except Exception as server_info_error:
        service_func.send_error(bot, message, 5, server_info_error)


# Вызов команды для задания вопросов
@bot.message_handler(commands=['yapoznaumir'])
def yapoznaumir(message):
    try:
        service_func.log(bot, f'вызов команды /yapoznaumir by {constants.shobla_member[message.from_user.id]["name"]}')
        bot.send_message(message.chat.id, constants.enter_question_gpt, reply_to_message_id=message.message_id, reply_markup=telebot.types.ForceReply(True))
        bot.delete_message(message.chat.id, message.message_id)
        service_func.update_activity(bot, 'yapoznaumir')
    except Exception as yapoznaumir_error:
        service_func.send_error(bot, message, 32, yapoznaumir_error)


# Вызов стартового сообщения / справки
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    try:
        if message.chat.id == secret.shobla_id or message.from_user.id in constants.shobla_member:  # Это Шобла или человек из Шоблы
            service_func.log(bot, f'вызов команды {message.text} by {constants.shobla_member[message.from_user.id]["name"]}')
            bot.send_message(message.chat.id, constants.help_text, reply_markup=keyboards.help_keyboard, parse_mode='Markdown')
            service_func.update_activity(bot, message.text[1:])
        else:
            service_func.log(bot, f'вызов команды {message.text}\n{constants.errors[0 if len(message.text) == 6 else 1]}: '
                             f'User ID - {message.from_user.id}, user_name - @{message.from_user.username}')
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
    except Exception as handle_start_help_error:
        service_func.send_error(bot, message, 0 if message.text == '/start' else 1, handle_start_help_error)


# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        if message.chat.id == secret.shobla_id:  # Это Шобла
            service_func.log(bot, f'вызов команды /who by {constants.shobla_member[message.from_user.id]["name"]}')
            bot.send_message(secret.shobla_id, constants.enter_question_new, reply_to_message_id=message.message_id, reply_markup=telebot.types.ForceReply(True))
            bot.delete_message(secret.shobla_id, message.message_id)
            service_func.update_activity(bot, 'who')
        elif message.chat.id in constants.shobla_member:
            bot.send_message(message.chat.id, '❌ Опрос создается только в [Шобле](t.me/c/1126587083/)', parse_mode='Markdown')
    except Exception as who_will_error:
        service_func.send_error(bot, message, 7, who_will_error)


# Отправка скидок
@bot.message_handler(commands=['discount'])
def send_discount(message):
    try:
        if message.from_user.id in constants.shobla_member:
            service_func.log(bot, f'вызов команды /discount by {constants.shobla_member[message.from_user.id]["name"]}')
            bot.send_message(message.chat.id, keyboards.buttons[2][0], reply_markup=keyboards.keyboard_start, parse_mode='Markdown')
            service_func.update_activity(bot, 'discount')
    except Exception as send_discount_error:
        service_func.send_error(bot, message, 8, send_discount_error)


# Вызов статистики
@bot.message_handler(commands=['stat'])
def statistics(message):
    global activity_count
    try:
        if message.chat.id == secret.shobla_id or message.from_user.id in constants.shobla_member:  # Это Шобла или человек из Шоблы
            now_time = datetime.datetime.now()
            cur_month = f'{now_time.year}.{now_time.month}'
            with open(constants.activity_file, 'r') as activity_file:  # Загружаем данные из файла activity_count
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
            service_func.send_error(bot, message, 6, 'вызов команды /stat')
    except Exception as statistics_error:
        service_func.send_error(bot, message, 4, statistics_error)


# Запрос отправки логов по боту
@bot.message_handler(commands=['log'])
def share_log(message):
    try:
        if message.chat.id == secret.shobla_id or message.from_user.id in constants.shobla_member:  # Это Шобла или человек из Шоблы
            try:
                service_func.log(bot, f'вызов команды /log by {constants.shobla_member[message.from_user.id]["name"]}')
                bot.send_document(message.chat.id, open(constants.log_file, 'rb'), caption='🤖📋 Log file')
            except Exception as upload_log_error:
                service_func.send_error(bot, message, 23, upload_log_error)
        else:
            service_func.send_error(bot, message, 6, 'вызов команды /log')
    except Exception as share_log_error:
        service_func.send_error(bot, message, 24, share_log_error)


# Запрос на ссылку созвона
@bot.message_handler(commands=['meeting'])
def meeting(message):
    try:
        if message.from_user.id in constants.shobla_member:  # Это человек из Шоблы
            service_func.log(bot, f'вызов команды /meeting by {constants.shobla_member[message.from_user.id]["name"]}')
            bot.send_photo(message.chat.id, constants.meeting_pic, caption=f'🤖 *Го созвон*\n{constants.meeting_link}', parse_mode='Markdown')
            service_func.update_activity(bot, 'meeting')
    except Exception as meeting_error:
        service_func.send_error(bot, message, 28, meeting_error)


# Запрос курса рубля
@bot.message_handler(commands=['usd'])
def usd(message):
    try:
        if message.from_user.id in constants.shobla_member:  # Это человек из Шоблы
            try:
                service_func.log(bot, f'вызов команды /usd by {constants.shobla_member[message.from_user.id]["name"]}')
                usa_dol, eur, geo_lar, kaz_ten, date = cbr.get_exchange_rates()
                bot.send_photo(message.chat.id, constants.usd_pic[random.randint(0, len(constants.usd_pic) - 1)],
                               caption=(f'💵 *Курс рубля по данным сайта* [ЦБР](https://www.cbr.ru/currency_base/daily/) *на {date}*:\n'
                                        f'`1$ = {usa_dol}₽`\n`1€ = {eur}₽`\n`1₾ = {geo_lar}₽`\n`100₸ = {kaz_ten}₽`'), parse_mode='Markdown')
                service_func.update_activity(bot, 'usd')
            except Exception as cbr_parse_error:
                service_func.send_error(bot, message, 18, f'{cbr.get_exchange_rates()}\n\n{cbr_parse_error}')
    except Exception as usd_error:
        service_func.send_error(bot, message, 31, usd_error)


# # # # # # Обработка текста # # # # # #
# Обработка девки за рулем
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace('a', '').replace('а', '') == '' and message.chat.id == secret.shobla_id)
def aaa(message):
    try:
        bot.send_message(secret.shobla_id, 'Девка за рулём') if len(message.text) > 2 else bot.send_message(secret.shobla_id, 'Двк з рлм')
        service_func.update_activity(bot, 'car_girl')
    except Exception as aaa_error:
        service_func.send_error(bot, message, 9, aaa_error)


# Обработка Emotional damage
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.damage and message.chat.id == secret.shobla_id)
def damage(message):
    try:
        bot.send_voice(secret.shobla_id, constants.emotional_damage_voice_id)
        service_func.update_activity(bot, 'damage')
    except Exception as damage_error:
        service_func.send_error(bot, message, 10, damage_error)


# Обработка mamma mia
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.mammamia and message.chat.id == secret.shobla_id)
def mamma_mia(message):
    try:
        audio = open(constants.mamma_audio_path, 'rb')
        bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)
        service_func.update_activity(bot, 'mamma')
    except Exception as mamma_mia_error:
        service_func.send_error(bot, message, 30, mamma_mia_error)


# Обработка РАСИЯ
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.russia and message.chat.id == secret.shobla_id)
def russia(message):
    try:
        bot.send_voice(secret.shobla_id, constants.anthem, '🫡')
        service_func.update_activity(bot, 'russia')
    except Exception as russia_error:
        service_func.send_error(bot, message, 11, russia_error)


# Обработка врача
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.hey_doc and message.chat.id == secret.shobla_id)
def hey_doc(message):
    try:
        bot.send_document(secret.shobla_id, constants.hey_doc_gif_id, caption='@oxy_genium')
        service_func.update_activity(bot, 'hey_doc')
    except Exception as hey_doc_error:
        service_func.send_error(bot, message, 12, hey_doc_error)


# Обработка @team
@bot.message_handler(func=lambda message: message.text and constants.team in message.text.lower() and message.chat.id == secret.shobla_id)
def team(message):
    try:
        bot.send_message(chat_id=secret.shobla_id, disable_notification=False, reply_to_message_id=message.message_id,
                         text=constants.team_text, disable_web_page_preview=True, parse_mode='Markdown')
        service_func.update_activity(bot, 'team')
    except Exception as team_error:
        service_func.send_error(bot, message, 14, team_error)


# Обработка @rapid
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(constants.rapid) and message.chat.id == secret.shobla_id)
def rapid(message):
    value = ''
    try:
        service_func.update_activity(bot, 'rapid')
        service_func.log(bot, f'вызов команды /rapid by {constants.shobla_member[message.from_user.id]["name"]}')
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
        service_func.log(bot, f'добавлен новый номер Рапида by {constants.shobla_member[message.from_user.id]["name"]}')
        if answer['message'] == 'Номер успешно добавлен':
            service_func.update_activity(bot, 'rapid_new')
    except Exception as rapid_error:
        bot.send_message(secret.zhuykovkb_id, f'Ошибка в функции rapid:\n\nДанные: {quote(value)}\n\nТекст ошибки {rapid_error}')
        service_func.send_error(bot, message, 15, f'{rapid_error}\nДанные: {quote(value)}')


# Обработка барсука
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.suk and message.chat.id == secret.shobla_id)
def badger(message):
    try:
        bot.send_message(secret.shobla_id, 'Барсук')
        service_func.update_activity(bot, 'cyk')
    except Exception as badger_error:
        service_func.send_error(bot, message, 16, badger_error)


# Обработка барсюка
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.syuk and message.chat.id == secret.shobla_id)
def another_badger(message):
    try:
        bot.send_message(secret.shobla_id, 'Барсюк')
        service_func.update_activity(bot, 'cyk')
    except Exception as another_badger_error:
        service_func.send_error(bot, message, 17, another_badger_error)


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
        audio = open(constants.kirov_audio_path, 'rb')
        bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)
        service_func.update_activity(bot, 'kirov')
    except Exception as kirov_error:
        service_func.send_error(bot, message, 27, kirov_error)


# # # # # # Получаение file_id медиа файлов # # # # # #
@bot.message_handler(content_types=['photo', 'voice', 'document', 'animation'])
def send_media_id(message):
    try:
        if message.chat.id == secret.apol_id:
            if message.photo:
                bot.send_message(secret.apol_id, message.photo[2].file_id)
            elif message.voice:
                bot.send_message(secret.apol_id, message.voice.file_id)
            elif message.document:
                bot.send_message(secret.apol_id, message.document.file_id)
            elif message.animation:
                bot.send_message(secret.apol_id, message.animation.file_id)
    except Exception as send_media_id_error:
        service_func.send_error(bot, message, 33, send_media_id_error)


# # # # # # Обработчик Call Back Data # # # # # #
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    try:
        keyboards.button_func(bot, call)
    except Exception as callback_buttons_error:
        service_func.send_error(bot, call.message, 3, callback_buttons_error)


# # # # # # Обработка опросов # # # # # #
@bot.poll_handler(func=lambda poll: True and poll.is_closed == 1 and str(poll.id) == curr_meeting_poll['poll_id'] and poll.total_voter_count > 1)
def poll_results(poll):
    global curr_meeting_poll
    try:
        meeting_results = []
        for item in poll.options:
            meeting_results.append(item.voter_count)
        max_date = meeting_results[0:4].index(max(meeting_results[0:4]))
        max_time = meeting_results[4:].index(max(meeting_results[4:])) + 4
        curr_meeting_poll['max_date'], curr_meeting_poll['max_time'] = max_date, max_time
        with open(constants.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
            meeting_file.write(json.dumps(curr_meeting_poll))
        service_func.log(bot, f'Приглашение на общий созвон будет отправлено{constants.meeting_options[max_time]}{constants.meeting_options[max_date][4:]}')
        poll_results_msg = bot.send_message(secret.shobla_id, f'Шоблятки, созвон на этой неделе будет в{constants.meeting_options[max_date][4:]} {constants.meeting_options[max_time]}',
                                            parse_mode='Markdown')
        bot.pin_chat_message(secret.shobla_id, poll_results_msg.message_id, disable_notification=False)
    except Exception as poll_results_error:
        service_func.log(bot, f'{constants.errors[29]}\nТекст ошибки: {poll_results_error}')
        bot.send_message(secret.apol_id, f'❌ Ошибка в функции poll_results:\nСообщение: {poll}\nТекст ошибки:\n{poll_results_error}')


# # # # # # Обработка текста реплаев и # # # # # #
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        text = message.text
        match = re.search(r'(instagram\.com/\S+)', message.text)
        # if translitsky.isTranslitsky(text) and text[0:4] != 'http':
        #     answer = translitsky.doTranslitskyRollback(text)
        #     bot.send_message(message.chat.id, f'`{answer}`', parse_mode='Markdown', reply_to_message_id=message.message_id)
        #     service_func.update_activity(bot, 'transl')
        # Если это попытка запинить сообщение
        if message.reply_to_message is not None and text == '@shoblabot' and message.chat.id == secret.shobla_id:
            try:
                bot.pin_chat_message(chat_id=secret.shobla_id, message_id=message.reply_to_message.message_id, disable_notification=False)
                service_func.log(bot, f'пин сообщения by {constants.shobla_member[message.from_user.id]["name"]}')
                service_func.update_activity(bot, 'pin')
            except Exception as pin_error:
                service_func.send_error(bot, message, 26, pin_error)
        # Если это реплай на сообщение бота
        elif message.reply_to_message is not None and message.reply_to_message.from_user.id == secret.bot_id:
            # Если вводится текст для опроса
            if message.reply_to_message.text == constants.enter_question_new or message.reply_to_message.text == constants.too_large_question:
                try:
                    if len(text) <= 291:
                        poll_text = f'{constants.shobla_member[message.from_user.id]["name"]}: {text}'
                        poll = bot.send_poll(secret.shobla_id, poll_text, constants.poll_options, is_anonymous=False, allows_multiple_answers=False)
                        stop_button = telebot.types.InlineKeyboardButton(text='Остановить опрос 🚫',
                                                                         callback_data=f'stop_{poll.message_id}_{message.from_user.id}')
                        keyboard_opros_stop = telebot.types.InlineKeyboardMarkup(row_width=1)
                        keyboard_opros_stop.add(stop_button)
                        bot.delete_message(secret.shobla_id, message.reply_to_message.message_id)
                        bot.edit_message_reply_markup(secret.shobla_id, poll.message_id, reply_markup=keyboard_opros_stop)
                        bot.delete_message(secret.shobla_id, message.message_id)
                        bot.pin_chat_message(secret.shobla_id, poll.message_id, disable_notification=False)
                        service_func.log(bot, f'создан опрос by {constants.shobla_member[message.from_user.id]["name"]}')
                        service_func.update_activity(bot, 'opros')
                    else:
                        force_reply = telebot.types.ForceReply(True)
                        bot.delete_message(secret.shobla_id, message.reply_to_message.message_id)
                        bot.send_message(message.chat.id, constants.too_large_question, reply_to_message_id=message.message_id, reply_markup=force_reply)
                except Exception as poll_reply_error:
                    service_func.send_error(bot, message, 19, poll_reply_error)
            # Если вводится вопрос к нейронке
            elif message.reply_to_message.text == constants.enter_question_gpt:
                try:
                    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo-16k', messages=[{"role": "user", "content": message.text}], stream=False)
                    bot.send_message(message.chat.id, response, reply_to_message_id=message.message_id, parse_mode='Markdown')
                except Exception as g4f_error:
                    service_func.send_error(bot, message, 32, g4f_error)
        # Если это ссылка из Instagram
        elif match:
            new_url = re.sub(r'instagram\.com', 'ddinstagram.com', match.group(1))  # Заменяем домен на ddinstagram.com
            bot.send_message(message.chat.id, new_url, reply_to_message_id=message.message_id)  # Отправляем сообщение с новой ссылкой
    except Exception as send_text_error:
        service_func.send_error(bot, message, 20, send_text_error)


# # # # # # Отправка запланированных сообщений # # # # # #
def sdr():
    global curr_meeting_poll
    global activity_count
    try:
        threading.Timer(3600, sdr).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
        now_time = datetime.datetime.now()
        with open(constants.meeting_file, 'r') as meeting_file:
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
                curr_meeting_poll['first_poll'] = 0  # Флаг, что это первый опрос в этом месяце
                with open(constants.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
                    meeting_file.write(json.dumps(curr_meeting_poll))
                service_func.log(bot, 'отправлено приглашение на общий созвон')
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
                with open(constants.meeting_file, 'w') as meeting_file:  # Записываем данные в файл meeting_file
                    meeting_file.write(json.dumps(curr_meeting_poll))
            if now_time.weekday() == 4 and now_time.day <= 8:  # День (пятница) для остановки опроса о принятии участия в созвоне
                with open(constants.meeting_file, 'r') as meeting_file:
                    curr_meeting_poll = json.loads(meeting_file.read())
                try:
                    bot.stop_poll(secret.shobla_id, curr_meeting_poll['msg_id'])
                except Exception as stop_poll_error:
                    service_func.log(bot, f'Ошибка при закрытии опроса в sdr:\nТекст ошибки:\n{stop_poll_error}')
                    bot.send_message(secret.apol_id, f'❌ Ошибка при закрытии опроса в sdr:\nТекст ошибки:\n{stop_poll_error}')
            if now_time.day == 1:  # День для статистики по боту выкладывания фоток за месяц и ежемесечной 10челлендж
                # Загружаем данные из файла activity_count
                cur_month = f'{now_time.year - 1}.12' if now_time.month == 1 else f'{now_time.year}.{now_time.month - 1}'
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
                bot.send_message(secret.shobla_id, month_statistics, parse_mode='Markdown')
                # Рассылка по 10челлендж
                challenge = bot.send_message(secret.shobla_id, '📸 Шоблятки, время для #10челлендж и ваших фоточек за месяц!', parse_mode='Markdown')
                bot.pin_chat_message(secret.shobla_id, challenge.message_id, disable_notification=False)
            # Отправка поздравлений с особым днём
            today = float(f'{now_time.day}.{now_time.month}')
            if today == 28.5:  # День Баяна в Шобле отмечается 28 мая
                bot.send_photo(secret.shobla_id, constants.bayan_day_pic, caption='🪗 Шобла, поздравляю с Днём Баяна!')
            if today == 24.11:  # День Рождения бота
                bot.send_message(secret.shobla_id, f'🥳 Сегодня ботику уже *{now_time.year - 2016} лет*!', parse_mode='Markdown')
            # Отправка поздравлений с ДР
            try:
                for user_id in constants.shobla_member:
                    age = now_time.year - constants.shobla_member[user_id]['year']
                    if constants.shobla_member[user_id]['dd_mm'] == today:
                        if age % 10 == 0:  # Если у человека юбилей
                            bot.send_message(secret.shobla_id, constants.happy_anniversary.format(constants.shobla_member[user_id]['name'], user_id, age), parse_mode='Markdown')
                        else:
                            bot.send_message(secret.shobla_id, f'🥳 [{constants.shobla_member[user_id]["name"]}](tg://user?id={user_id}), с др!', parse_mode='Markdown')
            except Exception as happy_bd_error:
                service_func.log(bot, f'{constants.errors[35]}:\nТекст ошибки:\n{happy_bd_error}')
                bot.send_message(secret.apol_id, f'❌ {constants.errors[35]}\nТекст ошибки:\n{happy_bd_error}')
    except Exception as sdr_error:
        service_func.log(bot, f'{constants.errors[34]}:\nТекст ошибки:\n{sdr_error}')
        bot.send_message(secret.apol_id, f'❌ {constants.errors[34]}\nТекст ошибки:\n{sdr_error}')


# # # # # # Запуск функций # # # # # #
try:
    sdr()
except Exception as e:
    bot.send_message(secret.apol_id, f'❌ Ошибка при запуске sdr\nТекст ошибки:\n{e}')
    service_func.log(bot, f'❌ Ошибка при запуске sdr\nТекст ошибки:\n{e}')

try:
    service_func.log(bot, 'Попытка запуска bot.infinity_polling()')
    bot.infinity_polling()
except Exception as e:
    service_func.log(bot, f'Ошибка при запуске bot.polling:\nТекст ошибки:\n{e}')
    with open(constants.log_file, 'a') as log_file_stream:
        traceback.print_exc(file=log_file_stream)
    bot.send_message(secret.apol_id, f'❌ Ошибка при запуске bot.polling:\nТекст ошибки:\n{e}')

try:
    with open(constants.log_file, 'a') as log_file_flow:
        log_file_flow.write(f'\nSTART\n{time.ctime(time.time())} - время запуска бота\n')
except Exception as e:
    bot.send_message(secret.apol_id, f'❌ Ошибка при логировании start_time:\nТекст ошибки:\n{e}')
