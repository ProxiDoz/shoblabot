#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-

# # # # # # Импортозамещение # # # # # #
import os  # Для проверки на существование файла
import json  # Представляет словарь в строку
import time  # Для представления времени в читаемом формате
import psutil
import telebot
import datetime
import constants
import secret
import random
import threading
import urllib.request as urllib2
from urllib.parse import quote
import traceback
import helpers.faggot as faggot  # faggot handler
import helpers.find_words as find_words
import helpers.translitsky as translitsky

# # # # # # Инициализация # # # # # #
bot = telebot.TeleBot(secret.tg_token)  # Token бота
activity_count = {}  # Переменная для сбора статистики по командам
curr_sozvon_poll = {}
if os.path.isfile(constants.sozvon_file):  # Загружаем данные из файла sozvon_file
    with open(constants.sozvon_file, 'r') as lang:
        curr_sozvon_poll = json.loads(lang.read())
sozvon_results = [0, 0, 0, 0, 0, 0, 0, 0]


# # # # # # Доступные команды # # # # # #
# Вызов стартового сообщения / справки
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:
            log('вызов команды {0} by {1}'.format(message.text, constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_message(message.chat.id, constants.help_text, reply_markup=constants.help_keyboard, parse_mode='Markdown')
            if message.from_user.is_premium and random.random() < 0.3:
                bot.send_message(message.chat.id, '🤡 Ебать ты команду выбрал, ||псина|| премиумная', parse_mode='MarkdownV2')
            update_activity('start') if message.text == '/start' else update_activity('help')
        else:
            log('вызов команды {0}\n{1}: User ID - {2}, user_name - @{3}'.format(message.text, constants.errors[6], message.from_user.id, message.from_user.username))
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[0 if message.text == '/start' else 1], e))
        send_error(message, 0 if message.text == '/start' else 1, e)


# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        update_activity('who')
        if message.chat.id == secret.tg_chat_id:
            log('вызов команды /who by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            force_reply = telebot.types.ForceReply(True)
            bot.send_message(secret.tg_chat_id, constants.enter_question_new, reply_to_message_id=message.message_id, reply_markup=force_reply)
            bot.delete_message(secret.tg_chat_id, message.message_id)
        elif message.chat.id in constants.tg_ids:
            bot.send_message(message.chat.id, '❌ Опрос создается только в [Шобле](https://t.me/c/1126587083/)', parse_mode='Markdown')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[7], e))
        send_error(message, 7, e)


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
            # keyboard_start.add(constants.discounts, constants.channel)
            bot.send_message(message.chat.id, constants.buttons[2][0], reply_markup=keyboard_start, parse_mode='MarkdownV2')
            # if message.from_user.is_premium and random.random() < 0.3:
            #     bot.send_message(message.chat.id, '🤡 Сэкономить решил, ||псина|| премиумная?', parse_mode='MarkdownV2')
            update_activity('discount')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[8], e))
        send_error(message, 8, e)


# # # # # # Служебные функции и команды # # # # # #
# Функция сбора статистики по командам и функциям
def update_activity(field):
    try:
        now_time = datetime.datetime.now()
        current_month = str(now_time.year) + '.' + str(now_time.month)
        if os.path.isfile(constants.activity_file):  # Загружаем данные из файла activity_count
            with open(constants.activity_file, 'r') as lang:
                activity_count = json.loads(lang.read())
        activity_count[current_month][field] += 1
        with open(constants.activity_file, 'w') as lang:  # Записываем данные в файл activity_count
            lang.write(json.dumps(activity_count))
    except Exception as e:
        log('Ошибка в функции update_activity:\nПоле: {0}\nТекст ошибки: {1}'.format(field, e))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции update_activity:\n*Поле: *{0}\n*Текст ошибки:*\n{1}'.format(field, e), parse_mode='MarkdownV2')


# Функция отправки ошибки
def send_error(message, error_id, error):
    try:
        bot.send_message(secret.apple_id,
                         '❌ *{0}\nОт:* {1} {2}\n*Username:* @{3}\n*Чат:* {4} {5} {6}\n*id:* {7}\n*Сообщение:* {8}\n*Время:* _{9}_\n*Текст ошибки:* '
                         '_{10}_'.format(constants.errors[error_id], message.from_user.first_name, message.from_user.last_name, message.from_user.username,
                                         message.chat.title, message.chat.first_name, message.chat.last_name, message.chat.id, message.text,
                                         time.ctime(time.time()), error), parse_mode='Markdown')
    except Exception as e:
        log('Ошибка в функции send_error:\nСообщение: {0}\nТекст ошибки: {1}'.format(message.text, e))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции send_error:\n*Сообщение: *{0}\n*Текст ошибки:*\n{1}'.format(message.text, e), parse_mode='MarkdownV2')


# Запись лога в файл log.txt
def log(text):
    try:
        with open(constants.log_file, 'a') as log_file:
            log_file.write(time.ctime(time.time()) + ' - ' + text + '\n')
    except Exception as e:
        bot.send_message(secret.apple_id, '❌ Ошибка при записи лога\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')


# Вызов статистики
@bot.message_handler(commands=['stat'])
def statistics(message):
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:  # Это Шобла или человек из Шоблы
            if message.from_user.id == secret.apple_id or message.from_user.is_premium:  # Это Апол или премиумный пользователь
                now_time = datetime.datetime.now()
                cur_mnth = str(now_time.year) + '.' + str(now_time.month)
                if os.path.isfile(constants.activity_file):  # Загружаем данные из файла activity_count
                    with open(constants.activity_file, 'r') as lang:
                        activity_count = json.loads(lang.read())
                month_statistics = constants.month_statistics.format(activity_count[cur_mnth]['opros'], activity_count[cur_mnth]['discount'],
                                                                     activity_count[cur_mnth]['devka'], activity_count[cur_mnth]['vracha'],
                                                                     activity_count[cur_mnth]['pin'], activity_count[cur_mnth]['rapid_new'],
                                                                     activity_count[cur_mnth]['cyk'], activity_count[cur_mnth]['russia'],
                                                                     activity_count[cur_mnth]['team'], activity_count[cur_mnth]['start'],
                                                                     activity_count[cur_mnth]['help'], activity_count[cur_mnth]['who'],
                                                                     activity_count[cur_mnth]['rapid'], activity_count[cur_mnth]['/29'],
                                                                     activity_count[cur_mnth]['kirov'], activity_count[cur_mnth]['damage'],
                                                                     activity_count[cur_mnth]['sozvon'], activity_count[cur_mnth]['transl'])
                bot.send_message(message.chat.id, month_statistics.replace('прошлый', 'текущий'), parse_mode='MarkdownV2')
            else:
                bot.send_message(message.chat.id, '⭐ У вас нет премиум подписки для использования данной команды')
        else:
            log('вызов команды /stat\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[4], e))
        send_error(message, 4, e)


# Запрос отправки логов по боту
@bot.message_handler(commands=['log'])
def share_log(message):
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:  # Это Шобла или человек из Шоблы
            if message.from_user.id == secret.apple_id or message.from_user.is_premium:  # Это Апол или премиумный пользователь
                try:
                    log('вызов команды /log by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
                    bot.send_document(message.chat.id, open(constants.log_file, 'rb'), caption='🤖📋')
                except Exception as e:
                    send_error(message, 23, e)
            else:
                bot.send_message(message.chat.id, '⭐ У вас нет премиум подписки для использования данной команды')
        else:
            log('вызов команды /log\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[24], e))
        send_error(message, 24, e)


# Запрос на ссылку созвона
@bot.message_handler(commands=['sozvon'])
def sozvon(message):
    try:
        if message.from_user.id in constants.tg_ids:
            log('вызов команды /sozvon by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_photo(message.chat.id, constants.sozvon_pic, caption='🤖 *Го созвон: *' + constants.sozvon_link, parse_mode='Markdown')
            update_activity('sozvon')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[28], e))
        send_error(message, 28, e)


# Вызов информации о сервере
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.from_user.id == secret.apple_id:
            try:
                log('отправка статуса памяти сервера')
                bot.send_message(message.chat.id, '🤖 RAM: {0}% из 512Мбайт'.format(psutil.virtual_memory()[2])) if message.text == '/s' else bot.send_message(secret.tg_chat_id,
                                                                                                                                                               message.text[
                                                                                                                                                               3:len(message.text)])
            except Exception as e:
                log('{0}\nТекст ошибки: {1}'.format(constants.errors[21], e))
                send_error(message, 21, e)
        else:
            log('вызов команды /s\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[5], e))
        send_error(message, 5, e)


# # # # # # Обработка текста # # # # # #
# Обработка девки за рулем
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace('a', '').replace('а', '') == '' and message.chat.id == secret.tg_chat_id)
def aaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Девка за рулём') if len(message.text) > 2 else bot.send_message(secret.tg_chat_id, 'Двк з рлм')
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Получай свою девку, ||псина|| премиумная', parse_mode='MarkdownV2')
        update_activity('devka')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[9], e))
        send_error(message, 9, e)


# Обработка emotional daaamage
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.damage and message.chat.id == secret.tg_chat_id)
def damage(message):
    try:
        bot.send_voice(secret.tg_chat_id, constants.emotional_daaamage)
        update_activity('damage')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[10], e))
        send_error(message, 10, e)


# Обработка РАСИЯ
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.russia and message.chat.id == secret.tg_chat_id)
def russia(message):
    try:
        bot.send_voice(secret.tg_chat_id, constants.anthem, '🫡 Ебать ты патриот, ||псина|| премиумная',
                       parse_mode='MarkdownV2') if message.from_user.is_premium and random.random() < 0.3 else bot.send_voice(secret.tg_chat_id, constants.anthem, '🫡')
        update_activity('russia')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[11], e))
        send_error(message, 11, e)


# Обработка врача
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.vracha and message.chat.id == secret.tg_chat_id)
def vracha(message):
    try:
        bot.send_document(secret.tg_chat_id, 'CgADAgADRgIAAkbDcEn-Ox-uqrgsHgI', caption='@oxy_genium')
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 А что подписка не лечит от всех болезней, ||псина|| премиумная?', parse_mode='MarkdownV2')
        update_activity('vracha')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[12], e))
        send_error(message, 12, e)


# Обработка гита
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.git and message.chat.id == secret.tg_chat_id)
def git(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Хуит')
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Ебать ты програмес, ||псина|| премиумная', parse_mode='MarkdownV2')
        update_activity('git')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[13], e))
        send_error(message, 13, e)


# Обработка @team
@bot.message_handler(func=lambda message: message.text and constants.team in message.text.lower() and message.chat.id == secret.tg_chat_id)
def team(message):
    try:
        bot.send_message(chat_id=secret.tg_chat_id, disable_notification=False, reply_to_message_id=message.message_id, text=constants.team_text, disable_web_page_preview=True,
                         parse_mode='Markdown')
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Ты тут никому не упёрся, ||псина|| премиумная', parse_mode='MarkdownV2')
        update_activity('team')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[14], e))
        send_error(message, 14, e)


# Обработка @rapid
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(constants.rapid) and message.chat.id == secret.tg_chat_id)
def rapid(message):
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
        response = urllib2.urlopen('https://rapid.zhuykovkb.ru/rapid?data=' + quote(value) + '&memberid=' + str(message.from_user.id))
        answer = json.loads(str(response.read(), 'utf-8'))
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Да вот тебе не насрать на рапиды, ||псина|| премиумная?', parse_mode='MarkdownV2')
        bot.send_message(secret.tg_chat_id, answer['message'], parse_mode='Markdown')
        if answer['message'] == 'Номер успешно добавлен':
            log('добавлен новый номер Рапида by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            update_activity('rapid_new')
    except Exception as e:
        bot.send_message(secret.zhuykovkb_apple_id, 'Ошибка в функции rapid:\n\nДанные ' + quote(value) + '\n\nТекст ошибки ' + str(e))
        log('Ошибка в функции rapid:\nДанные: {0}\nТекст ошибки: {1}'.format(quote(value), e))
        send_error(message, 15, e)


# Обработка барсука
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.suk and message.chat.id == secret.tg_chat_id)
def barsuk(message):
    try:
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Хуй тебе, а не барсука, ||псина|| премиумная', parse_mode='MarkdownV2')
        else:
            bot.send_message(secret.tg_chat_id, 'Барсук')
            update_activity('cyk')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[16], e))
        send_error(message, 16, e)


# Обработка барсюка
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.syuk and message.chat.id == secret.tg_chat_id)
def barsyuk(message):
    try:
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Хуй тебе, а не барсюка, ||псина|| премиумная', parse_mode='MarkdownV2')
        else:
            bot.send_message(secret.tg_chat_id, 'Барсюк')
            update_activity('cyk')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[17], e))
        send_error(message, 17, e)


# Обработка IPv6
@bot.message_handler(func=lambda message: message.text and message.text.lower() == constants.ip_block and message.chat.id == secret.tg_chat_id)
def block(message):
    try:
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Значит так, \- сразу нахуй, ||псина|| премиумная', parse_mode='MarkdownV2')
        else:
            bot.send_message(secret.tg_chat_id, '*Значит так, \- сразу ||нахуй||\!*', parse_mode='MarkdownV2')
        update_activity('/29')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[18], e))
        send_error(message, 18, e)


# Обработка каждого сообщения на гея/лешу
@bot.message_handler(func=lambda m: True)
def faggot_func(message):
    try:
        if random.random() < 0.3:
            faggotEUCountry = faggot.getFaggotEUCountryRequest(message.text,
                                                               ['гей', 'пидор', 'пидр', 'педик', 'гомо', 'гомосек', 'глиномес', 'пидераст', 'леша', 'путин', 'путен', 'путейн', 'маргарин', 'путена'])
            if faggotEUCountry[0]:
                location = faggotEUCountry[1]['coords']
                bot.reply_to(message, 'Ты что то сказал про гея? Держи...')
                bot.send_location(message.chat.id, location['lat'], location['lng'])
        kirov(message)
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[25], e))
        send_error(message, 25, e)


# Обработка Кирова
@bot.message_handler(func=lambda m: True)
def kirov(message):
    try:
        if find_words.wordInMessage(message.text, constants.kirov):
            audio = open(constants.kirov_audio_path, 'rb')
            bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)
            update_activity('kirov')
        send_text(message)
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[27], e))
        send_error(message, 27, e)


# # # # # # Обработка опросов # # # # # #
@bot.poll_handler(func=lambda poll: True)
def poll_results(poll):
    try:
        if poll.is_closed == 1 and str(poll.id) == curr_sozvon_poll['poll_id'] and poll.total_voter_count > 1:
            i = 0
            for item in poll.options:
                sozvon_results[i] = int(item.voter_count)
                i += 1
            max_date = sozvon_results[0:4].index(max(sozvon_results[0:4]))
            max_time = sozvon_results[4:].index(max(sozvon_results[4:])) + 4
            curr_sozvon_poll['max_date'] = max_date
            curr_sozvon_poll['max_time'] = max_time
            with open(constants.sozvon_file, 'w') as lang:  # Записываем данные в файл sozvon_file
                lang.write(json.dumps(curr_sozvon_poll))
            log('Приглашение на общий созвон будет отправлено в ' + constants.sozvon_options[max_time] + ' ' + constants.sozvon_options[max_date][4:])
            poll_results = bot.send_message(secret.tg_chat_id, 'Шоблятки, созвон на этой неделе будет в ' + constants.sozvon_options[max_date][4:] + ' ' + constants.sozvon_options[max_time], parse_mode='Markdown')
            bot.pin_chat_message(secret.tg_chat_id, poll_results.message_id, disable_notification=False)
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[29], e))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции poll_results:\n*Сообщение: *{0}\n*Текст ошибки:*\n{1}'.format(poll, e), parse_mode='MarkdownV2')


# # # # # # Обработка реплаев # # # # # #
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        text = message.text
        if translitsky.isTranslitsky(text) and text[0:4] != 'http':
            answer = translitsky.doTranslitskyRollback(text)
            bot.send_message(message.chat.id, "`{}`".format(answer), parse_mode='MarkdownV2', reply_to_message_id=message.message_id)
            update_activity('transl')
        # Если это попытка запинить сообщение
        if message.reply_to_message is not None and text == '@shoblabot' and message.chat.id == secret.tg_chat_id:
            try:
                if message.from_user.is_premium and random.random() < 0.3:
                    bot.send_message(message.chat.id, '🤡 Жопу себе запинь, ||псина|| премиумная', parse_mode='MarkdownV2')
                bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id, disable_notification=False)
                log('пин сообщения by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
                update_activity('pin')
            except Exception as e:
                log('{0}\nТекст ошибки: {1}'.format(constants.errors[26], e))
                send_error(message, 26, e)
        # Если это реплай на сообщение бота
        elif message.reply_to_message is not None and message.reply_to_message.from_user.id == secret.bot_id:
            # Запрос внесения опроса
            if message.reply_to_message.text == constants.enter_question_new or message.reply_to_message.text == constants.too_large_question:
                try:
                    if len(text) <= 291:
                        opros = constants.tg_names[constants.tg_ids.index(message.from_user.id)] + ': ' + text
                        poll = bot.send_poll(secret.tg_chat_id, opros, constants.poll_options, is_anonymous=False, allows_multiple_answers=False)
                        stop_button = telebot.types.InlineKeyboardButton(text='Остановить опрос 🚫',
                                                                         callback_data='stop_{0}_{1}'.format(
                                                                             poll.message_id, message.from_user.id))
                        keyboard_opros_stop = telebot.types.InlineKeyboardMarkup(row_width=1)
                        keyboard_opros_stop.add(stop_button)
                        if message.from_user.is_premium and random.random() < 0.3:
                            bot.send_message(message.chat.id, '🤡 Да всем насрать на твой опрос, ||псина|| премиумная', parse_mode='MarkdownV2')
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
                except Exception as e:
                    log('{0}\nТекст ошибки: {1}'.format(constants.errors[19], e))
                    send_error(message, 19, e)
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[20], e))
        send_error(message, 20, e)


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
            except Exception as e:
                log('{0}\nТекст ошибки: {1}'.format(constants.errors[22], e))
                send_error(call.message, 22, e)
        # Обработка запроса скидок
        elif call.data[0:4] == 'disc':
            if call.from_user.is_premium and random.random() < 0.3:
                bot.answer_callback_query(call.id, '🤡 Псина премиумная')
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
                                  parse_mode='MarkdownV2', reply_markup=keyboard_update)
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[3], e))
        send_error(call.message, 3, e)


# # # # # # Отправка запланированных сообщений # # # # # #
def sdr():
    try:
        threading.Timer(3600, sdr).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
        # Отправка предупреждения о загрузке оперативной памяти
        if psutil.virtual_memory()[2] > 80:
            bot.send_message(secret.apple_id, '‼️ Oh shit, attention ‼️\n💾 Used RAM: {0}%'.format(psutil.virtual_memory()[2]), parse_mode='MarkdownV2')
        # Отправка статистики 1ого чиса месяца
        now_time = datetime.datetime.now()
        dr = str(now_time.day) + '.' + str(now_time.month)
        i = 0
        if os.path.isfile(constants.sozvon_file):
            with open(constants.sozvon_file, 'r') as lang:
                curr_sozvon_poll = json.loads(lang.read())
        if now_time.hour != 9:
            if now_time.weekday() - 3 == curr_sozvon_poll['max_date'] and now_time.hour - 13 == curr_sozvon_poll['max_time']:
                reminder = bot.send_message(secret.tg_chat_id, 'Сегодня шоблосозвон будет через час. Ожидайте ссылку.', parse_mode='Markdown')
                bot.pin_chat_message(secret.tg_chat_id, reminder.message_id, disable_notification=False)
                log('Отправлено напоминание на общий созвон')
            if now_time.weekday() - 3 == curr_sozvon_poll['max_date'] and now_time.hour - 14 == curr_sozvon_poll['max_time']:
                photo = bot.send_photo(secret.tg_chat_id, constants.sozvon_pic, caption='*Го созвон: *' + constants.sozvon_link, parse_mode='Markdown')
                bot.pin_chat_message(secret.tg_chat_id, photo.message_id, disable_notification=False)
                log('Отправлено приглашение на общий созвон')
            return
        if now_time.weekday() == 3:  # День (четверг) для отправки опроса о принятии участия в созвоне
            opros = 'Когда проведём шоблосозвон? Выбирайте день и ниже укажите время (относительно 🇷🇺: 🇫🇷-2, 🇬🇪+1, 🇰🇿+3). Опрос закроется через сутки'
            sozvon_poll = bot.send_poll(secret.tg_chat_id, opros, constants.sozvon_options, is_anonymous=False, allows_multiple_answers=True)
            bot.pin_chat_message(secret.tg_chat_id, sozvon_poll.message_id, disable_notification=False)
            curr_sozvon_poll['msg_id'] = sozvon_poll.id
            curr_sozvon_poll['poll_id'] = sozvon_poll.poll.id
            curr_sozvon_poll['max_date'] = 10
            curr_sozvon_poll['max_time'] = 10
            with open(constants.sozvon_file, 'w') as lang:  # Записываем данные в файл sozvon_file
                lang.write(json.dumps(curr_sozvon_poll))
        if now_time.weekday() == 4:  # День (пятница) для остановки опроса о принятии участия в созвоне
            if os.path.isfile(constants.sozvon_file):
                with open(constants.sozvon_file, 'r') as lang:
                    curr_sozvon_poll = json.loads(lang.read())
            bot.stop_poll(secret.tg_chat_id, curr_sozvon_poll['msg_id'])
        if now_time.day == 1:  # День для статистики по боту выкладывания фоток за месяц Месечная десятка челлендж
            cur_mnth = str(now_time.year - 1) + '.12' if now_time.month == 1 else str(now_time.year) + '.' + str(now_time.month - 1)
            # Загружаем данные из файла activity_count
            if os.path.isfile(constants.activity_file):
                with open(constants.activity_file, 'r') as lang:
                    activity_count = json.loads(lang.read())
            month_statistics = constants.month_statistics.format(activity_count[cur_mnth]['opros'], activity_count[cur_mnth]['discount'],
                                                                 activity_count[cur_mnth]['devka'], activity_count[cur_mnth]['vracha'],
                                                                 activity_count[cur_mnth]['pin'], activity_count[cur_mnth]['rapid_new'],
                                                                 activity_count[cur_mnth]['cyk'], activity_count[cur_mnth]['russia'],
                                                                 activity_count[cur_mnth]['team'], activity_count[cur_mnth]['start'],
                                                                 activity_count[cur_mnth]['help'], activity_count[cur_mnth]['who'],
                                                                 activity_count[cur_mnth]['rapid'], activity_count[cur_mnth]['/29'],
                                                                 activity_count[cur_mnth]['kirov'], activity_count[cur_mnth]['damage'],
                                                                 activity_count[cur_mnth]['sozvon'], activity_count[cur_mnth]['transl'])
            bot.send_message(secret.tg_chat_id, month_statistics, parse_mode='Markdown')
            # Рассылка по 10челлендж
            challenge = bot.send_message(secret.tg_chat_id, '📸 Шоблятки, время для #10челлендж и ваших фоточек за месяц!', parse_mode='Markdown')
            bot.pin_chat_message(secret.tg_chat_id, challenge.message_id, disable_notification=False)
        # День Баяна в Шобле отмечается 28 мая
        if dr == str(28.5):
            bot.send_photo(secret.tg_chat_id, 'AgACAgIAAxkBAAJFzWLeYTbQ2ENcXEwoPOrRZprGCCUUAALHuTEb6BT4ShJZvIDQxNjZAQADAgADcwADKQQ', caption='🪗 Шобла, поздравляю с Днём Баяна!')
        # Отправка поздравлений с ДР
        for item in constants.tg_drs:
            if item[:-5] == dr:
                if (now_time.year - int(item[-4:])) % 10 == 0:
                    bot.send_message(secret.tg_chat_id, '🥳 [{0}](tg://user?id={1}), с др\!\nДобро пожаловать в клуб кому '
                                                        'за {2} 😏'.format(constants.tg_names[i], constants.tg_ids[i], now_time.year - int(item[-4:])),
                                     parse_mode='MarkdownV2')
                else:
                    bot.send_message(secret.tg_chat_id, '🥳 [{0}](tg://user?id={1}), с др\!'.format(constants.tg_names[i], constants.tg_ids[i]), parse_mode='MarkdownV2')
            i += 1
    except Exception as e:
        log('Ошибка в функции отправки поздравления в Шоблу sdr:\nТекст ошибки: ' + str(e))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции отправки поздравления в Шоблу sdr\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')


# # # # # # Запуск функций # # # # # #
# try:
#     bot.remove_webhook()
# except Exception as e:
#     log('Ошибка в функции функции bot.remove_webhook:\nТекст ошибки: ' + str(e))
#     bot.send_message(secret.apple_id, '❌ Ошибка в функции bot.remove_webhook\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')

try:
    sdr()
except Exception as e:
    log('Ошибка при запуске sdr:\nТекст ошибки: ' + str(e))
    bot.send_message(secret.apple_id, '❌ Ошибка при запуске sdr\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')

try:
    with open(constants.log_file, 'a') as log_file:
        log_file.write('\nSTART\n' + time.ctime(time.time()) + ' - время запуска бота\n')
except Exception as e:
    bot.send_message(secret.apple_id, '❌ Ошибка при логировании start_time:\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')

try:
    log('попытка запуска bot.infinity_polling()')
    bot.infinity_polling()
except Exception as e:
    with open(constants.log_file, 'a') as log_file:
        traceback.print_exc(file=log_file)
    log('Ошибка при запуске bot.polling:\nТекст ошибки: ' + str(e))
    bot.send_message(secret.apple_id, '❌ Ошибка при запуске bot.polling\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')
