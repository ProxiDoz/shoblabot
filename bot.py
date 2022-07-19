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
# import cherry
import threading
import urllib.request as urllib2  # Для отправки фотографий из Telegram в Шоблу
from urllib.parse import quote

# # # # # # Инициализация # # # # # #
bot = telebot.TeleBot(secret.tg_token)  # Token бота
activity_count = {}  # Переменная для сбора статистики по командам


# # # # # # Доступные команды # # # # # #
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:
            log('вызов команды /start by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_message(secret.tg_requests_chat_id, '🕹 [start](tg://user?id={0})'.format(message.from_user.id), parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, disable_web_page_preview=True, parse_mode='Markdown')
            if message.from_user.is_premium and random.random() < 0.3:
                bot.send_message(message.chat.id, '🤡 Ебать ты команду выбрал, ||псина|| премиумная', parse_mode='MarkdownV2')
            update_activity('start')
        else:
            log('вызов команды /start\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='MarkdownV2')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[0], e))
        send_error(message, 0, e)


# Вызов справки
@bot.message_handler(commands=['help'])
def handle_help(message):
    try:
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:
            log('вызов команды /help by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_message(secret.tg_requests_chat_id, '❓ [help](tg://user?id={0})'.format(message.from_user.id), parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, reply_markup=constants.help_keyboard, parse_mode='Markdown')
            if message.from_user.is_premium and random.random() < 0.3:
                bot.send_message(message.chat.id, '🤡 Тебе ничего не поможет, ||псина|| премиумная', parse_mode='MarkdownV2')
            update_activity('help')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[1], e))
        send_error(message, 1, e)


# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        update_activity('who')
        if message.chat.id == secret.tg_chat_id:
            log('вызов команды /who by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            bot.send_message(secret.tg_requests_chat_id, '✅❌ [who](tg://user?id={0})'.format(str(message.from_user.id)), parse_mode='Markdown')
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
            keyboard_start.add(constants.discounts, constants.channel)
            bot.send_message(message.chat.id, constants.buttons[2][0], reply_markup=keyboard_start, parse_mode='MarkdownV2')
            if message.from_user.is_premium and random.random() < 0.3:
                bot.send_message(message.chat.id, '🤡 Сэкономить решил, ||псина|| премиумная?', parse_mode='MarkdownV2')
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
        # Загружаем данные из файла activity_count
        if os.path.isfile(constants.activity_file):
            with open(constants.activity_file, 'r') as lang:
                activity_count = json.loads(lang.read())
        activity_count[current_month][field] += 1
        # Записываем данные в файл activity_count
        with open(constants.activity_file, 'w') as lang:
            lang.write(json.dumps(activity_count))
    except Exception as e:
        log('Ошибка в функции update_activity:\nПоле: {0}\nТекст ошибки: {1}'.format(field, e))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции update_activity:\n*Поле: *{0}\n*Текст ошибки:*\n{1}'.format(field, e),
                         parse_mode='MarkdownV2')


# Функция отправки ошибки
def send_error(message, error_id, error):
    try:
        bot.send_message(secret.apple_id,
                         '❌ *{0}\nОт:* {1} {2}\n*Username:* @{3}\n*Чат:* {4} {5} {6}\n*id:* {7}\n*Сообщение:* {8}\n'
                         '*Время:* _{9}_\n*Текст ошибки:* _{10}_'.format(constants.errors[error_id], str(message.from_user.first_name),
                                                                   str(message.from_user.last_name), str(message.from_user.username),
                                                                   str(message.chat.title), str(message.chat.first_name),
                                                                   str(message.chat.last_name), str(message.chat.id), message.text,
                                                                   time.ctime(time.time()), error),
                         parse_mode='Markdown')
    except Exception as e:
        log('Ошибка в функции send_error:\nСообщение: {0}\nТекст ошибки: {1}'.format(message.text, e))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции send_error:\n*Сообщение: *{0}\n*Текст ошибки:*\n{1}'.format(message.text, e),
                         parse_mode='MarkdownV2')


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
        now_time = datetime.datetime.now()
        current_month = str(now_time.year) + '.' + str(now_time.month)
        # Загружаем данные из файла activity_count
        if os.path.isfile(constants.activity_file):
            with open(constants.activity_file, 'r') as lang:
                activity_count = json.loads(lang.read())
        month_statistics = constants.month_statistics.format(activity_count[current_month]['opros'], activity_count[current_month]['discount'],
                                                             activity_count[current_month]['devka'], activity_count[current_month]['vracha'],
                                                             activity_count[current_month]['pin'], activity_count[current_month]['rapid_new'],
                                                             activity_count[current_month]['cyk'], activity_count[current_month]['russia'],
                                                             activity_count[current_month]['team'], activity_count[current_month]['start'],
                                                             activity_count[current_month]['help'], activity_count[current_month]['who'],
                                                             activity_count[current_month]['rapid'], activity_count[current_month]['/29'])
        bot.send_message(secret.apple_id, month_statistics, parse_mode='MarkdownV2')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[4], e))
        send_error(message, 4, e)


# Вызов информации о сервере
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.chat.id == secret.apple_id:
            try:
                log('отправка статуса RAM памяти сервера')
                bot.send_message(message.chat.id, '💿 Used RAM: {0}%\n💾 Used disk: {1}%'.format(psutil.virtual_memory()[2], psutil.disk_usage('/')[3])) if message.text == '/s' else bot.send_message(secret.tg_chat_id, message.text[3:len(message.text)])
            except Exception as e:
                log('{0}\nТекст ошибки: {1}'.format(constants.errors[21], e))
                send_error(message, 21, e)
        else:
            log('вызов команды /s\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[5], e))
        send_error(message, 5, e)


# Запрос отправки логов в личку
@bot.message_handler(commands=['log'])
def share_log(message):
    try:
        if message.chat.id == secret.apple_id:
            try:
                log('вызов команды /log by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
                bot.send_document(secret.apple_id, open(constants.log_file, 'rb'))
            except Exception as e:
                send_error(message, 23, e)
        else:
            log('вызов команды /log\n{0}: User ID - {1}, user_name - @{2}'.format(constants.errors[6], message.from_user.id, message.from_user.username))
            send_error(message, 6, 'N/A')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[24], e))
        send_error(message, 24, e)


# # # # # # Обработка текста # # # # # #
# Обработка девок за рулем
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.dvk and message.chat.id == secret.tg_chat_id)
def aaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Двк з рлм')
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Получай свою девку, ||псина|| премиумная', parse_mode='MarkdownV2')
        update_activity('devka')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[9], e))
        send_error(message, 9, e)


@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.devka and message.chat.id == secret.tg_chat_id)
def aaaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Девка за рулём')
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Получай свою девку, ||псина|| премиумная', parse_mode='MarkdownV2')
        update_activity('devka')
    except Exception as e:
        log('{0}\nТекст ошибки: {1}'.format(constants.errors[10], e))
        send_error(message, 10, e)


# Обработка РАСИЯ
@bot.message_handler(func=lambda message: message.text and message.text.lower().replace(' ', '').replace('\n', '') in constants.russia and message.chat.id == secret.tg_chat_id)
def russia(message):
    try:
        bot.send_voice(secret.tg_chat_id, constants.anthem, '🫡')
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Ебать ты патриот, ||псина|| премиумная', parse_mode='MarkdownV2')
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
        bot.send_message(chat_id=secret.tg_chat_id, disable_notification=False, reply_to_message_id=message.message_id, text=constants.team_text,
                         disable_web_page_preview=True, parse_mode='Markdown')
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
        response = urllib2.urlopen('https://bot.zhuykovkb.ru:81/rapid?data=' + quote(value) + '&memberid=' + str(message.from_user.id))
        answer = json.loads(str(response.read(), 'utf-8'))
        if message.from_user.is_premium and random.random() < 0.3:
            bot.send_message(message.chat.id, '🤡 Да вот тебе не настрать на рапиды, ||псина|| премиумная?', parse_mode='MarkdownV2')
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
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.ip_block and message.chat.id == secret.tg_chat_id)
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


# # # # # # Обработка реплаев # # # # # #
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        # Если это реплай на сообщение бота
        if message.reply_to_message is not None and message.reply_to_message.from_user.id == secret.bot_id:
            # Запрос внесения опроса (нового)
            if message.reply_to_message.text == constants.enter_question_new or message.reply_to_message.text == constants.too_large_question:
                try:
                    if len(message.text) <= 291:
                        opros = constants.tg_names[constants.tg_ids.index(message.from_user.id)] + ': ' + message.text
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
                        bot.send_message(message.chat.id, constants.too_large_question, reply_to_message_id=message.message_id,
                                         reply_markup=force_reply)
                except Exception as e:
                    log('{0}\nТекст ошибки: {1}'.format(constants.errors[19], e))
                    send_error(message, 19, e)
            # Если это попытка запинить сообщение
            elif message.text == '@shoblabot':
                bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                     disable_notification=False)
                if message.from_user.is_premium and random.random() < 0.3:
                    bot.send_message(message.chat.id, '🤡 Жопу себе запинь, ||псина|| премиумная', parse_mode='MarkdownV2')
                log('пин сообщения by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
                update_activity('pin')
        elif message.reply_to_message is not None and message.text == '@shoblabot':
            bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                 disable_notification=False)
            if message.from_user.is_premium and random.random() < 0.3:
                bot.send_message(message.chat.id, '🤡 Жопу себе запинь, ||псина|| премиумная', parse_mode='MarkdownV2')
            log('пин сообщения by {0}'.format(constants.tg_names[constants.tg_ids.index(message.from_user.id)]))
            update_activity('pin')
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
                bot.stop_poll(secret.tg_chat_id, message_id) if call.from_user.id == user_id else bot.answer_callback_query(call.id,
                                                                                                                            constants.wrong_stop,
                                                                                                                            show_alert=True)
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
            keyboard_update.add(constants.discounts, constants.channel)
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
            bot.send_message(secret.apple_id, '‼️ Oh shit, attention ‼️\n💾 Used RAM: {0}%'.format(psutil.virtual_memory()[2]),
                             parse_mode='MarkdownV2')
        # Отправка статистики 1ого чиса месяца
        now_time = datetime.datetime.now()
        dr = str(now_time.day) + '.' + str(now_time.month)
        i = 0
        if now_time.hour != 10:
            return
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
                                                                 activity_count[cur_mnth]['rapid'], activity_count[cur_mnth]['/29'])
            bot.send_message(secret.tg_chat_id, month_statistics, parse_mode='Markdown')
            # Рассылка по 10челлендж
            challenge = bot.send_message(secret.tg_chat_id, '📸 Шоблятки, время для #10челлендж и выших фоточек за месяц!', parse_mode='MarkdownV2')
            bot.pin_chat_message(secret.tg_chat_id, challenge.message_id, disable_notification=False)
        # День Баяна в Шобле отмечается 28 мая
        if dr == str(28.5):
            bot.send_message(secret.tg_chat_id, '🪗 Шобла, поздравляю с Днём Баяна!')
        # Отправка поздравлений с ДР
        for item in constants.tg_drs:
            if item == dr:
                bot.send_message(secret.tg_chat_id,
                                 '🥳 [{0}](tg://user?id={1}), с др\!'.format(constants.tg_names[i], constants.tg_ids[i]), parse_mode='MarkdownV2')
            i += 1
    except Exception as e:
        log('Ошибка в функции отправки поздравления в Шоблу sdr:\nТекст ошибки: ' + str(e))
        bot.send_message(secret.apple_id, '❌ Ошибка в функции отправки поздравления в Шоблу sdr\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')


# # # # # # Запуск функций # # # # # #
try:
    bot.remove_webhook()
except Exception as e:
    log('Ошибка в функции функции bot.remove_webhook:\nТекст ошибки: ' + str(e))
    bot.send_message(secret.apple_id, '❌ Ошибка в функции bot.remove_webhook\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')

try:
    sdr()
except Exception as e:
    log('Ошибка при запуске sdr:\nТекст ошибки: ' + str(e))
    bot.send_message(secret.apple_id, '❌ Ошибка при запуске sdr\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')

try:
    with open(constants.log_file, 'a') as log_file:
        log_file.write('\nSTART\n' + time.ctime(time.time()) + ' - время запуска бота\n')
    # bot.send_message(secret.tg_test_chat_id, '⏳ *Время запуска бота:* _{0}_'.format(time.ctime(time.time())), parse_mode='MarkdownV2')
except Exception as e:
    bot.send_message(secret.apple_id, '❌ Ошибка при логировании start_time:\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')

try:
    log('попытка запуска bot.infinity_polling()')
    bot.infinity_polling()
except Exception as e:
    log('Ошибка при запуске bot.polling:\nТекст ошибки: ' + str(e))
    bot.send_message(secret.apple_id, '❌ Ошибка при запуске bot.polling\n*Текст ошибки:*\n' + str(e), parse_mode='MarkdownV2')


# class WebhookServer(object):
#     # index равнозначно /, т.к. отсутствию части после ip-адреса (грубо говоря)
#     @cherrypy.expose
#     def index(self):
#         length = int(cherrypy.request.headers['content-length'])
#         json_string = cherrypy.request.body.read(length).decode("utf-8")
#         update = telebot.types.Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#
# if __name__ == '__main__':
#     cherrypy.config.update({
#         'server.socket_host': '127.0.0.1',
#         'server.socket_port': 7771,
#         'engine.autoreload.on': False
#     })
#     cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
