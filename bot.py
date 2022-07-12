#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import os  # Для проверки на существование файла
import json  # Представляет словарь в строку
import time  # Для представления времени в читаемом формате
import psutil
import telebot
import datetime
import constants
import secret
# import cherry
import threading
import subprocess
import urllib.request as urllib2  # Для отправки фотографий из Telegram в Шоблу
from urllib.parse import quote


# # # # # # # # # # # Инициализация # # # # # # # # # # #
# Token бота
bot = telebot.TeleBot(secret.tg_token)

# Переменные для опроса
who_opros = {}
who_count = len(constants.who_will[0])
who_odd = who_count % 2

# Переменная для сбора статистики по командам
activity_count = {}

# Клавиатуры для скидок
disc_count = len(constants.buttons[0])
discounts = telebot.types.InlineKeyboardButton(text='Все скидки 💰', url='https://photos.app.goo.gl/Xu4UQWqhSTcBVwt27')
channel = telebot.types.InlineKeyboardButton(text='Канал 💳', url='https://t.me/joinchat/AAAAAEk6NVud6BKc7YzZ2g')


# # # # # # # # # # # Тело бота # # # # # # # # # # #
# Начальное сообщение
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        update_activity('start')
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:
            bot.send_message(secret.tg_requests_chat_id, '🕹 [start](tg://user?id={0})'.format(str(message.from_user.id)), parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, disable_web_page_preview=True, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
    except Exception as e:
        send_error(message, 0, e)


# Вызов справки
@bot.message_handler(commands=['help'])
def handle_help(message):
    try:
        update_activity('help')
        if message.chat.id == secret.tg_chat_id or message.from_user.id in constants.tg_ids:
            bot.send_message(secret.tg_requests_chat_id, '❓ [help](tg://user?id={0})'.format(str(message.from_user.id)), parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, reply_markup=constants.help_keyboard, parse_mode='Markdown')
    except Exception as e:
        send_error(message, 1, e)


# # # # # # Служебные функции и команды
# Функция отправки времени старта запуска бота
# def send_start_time():
#     try:
#         bot.send_message(secret.apple_id, '⏳ *Время запуска бота:* _{0}_'.format(time.ctime(time.time())), parse_mode='Markdown')
#     except Exception as e:
#         bot.send_message(secret.apple_id, '❌ Ошибка в функции send_start_time:\n*Ошибка:*\n' + str(e))


# Функция сбора статистики по командам и функциям
def update_activity(field):
    try:
        now_time = datetime.datetime.now()
        cur_mnth = str(now_time.year) + '.' + str(now_time.month)
        # Загружаем данные из файла activity_count
        if os.path.isfile('/root/router/shoblabot/activity_count'):
            with open('/root/router/shoblabot/activity_count', 'r') as lang:
                activity_count = json.loads(lang.read())
        activity_count[cur_mnth][field] += 1
        # Записываем данные в файл activity_count
        with open('/root/router/shoblabot/activity_count', 'w') as lang:
            lang.write(json.dumps(activity_count))
    except Exception as e:
        bot.send_message(secret.apple_id, '❌ Ошибка в функции udate_activity:\n*Поле: *{0}\n*Ошибка:*\n{1}'.format(field, e))
        

# Функция отправки ошибки
def send_error(message, error_id, error):
    try:
        bot.send_message(secret.apple_id,
                         '❌ *{0}\nОт:* {1} {2}\n*Username:* {3}\n*Чат:* {4} {5} {6}\n*id:* {7}\n*Сообщение:* {8}\n'
                         '*Время:* _{9}_\n*Ошибка:* _{10}_'.format(constants.errors[error_id], str(message.from_user.first_name),
                                                 str(message.from_user.last_name), str(message.from_user.username),
                                                 str(message.chat.title), str(message.chat.first_name),
                                                 str(message.chat.last_name), str(message.chat.id), message.text, time.ctime(time.time()), error),
                         parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, '❌ Ошибка в функции send_error:\n*Сообщение: *{0}\n*Ошибка:*\n{1}'.format(message.text, e))

        
# Вызов статистики
@bot.message_handler(commands=['stat'])
def statistics(message):
    try:
        now_time = datetime.datetime.now()
        cur_mnth = str(now_time.year) + '.' + str(now_time.month)
        # Загружаем данные из файла activity_count
        if os.path.isfile('/root/router/shoblabot/activity_count'):
            with open('/root/router/shoblabot/activity_count', 'r') as lang:
                activity_count = json.loads(lang.read())
        month_statistics = constants.month_statistics.format(activity_count[cur_mnth]['opros'], activity_count[cur_mnth]['discount'],
                                                       activity_count[cur_mnth]['devka'], activity_count[cur_mnth]['vracha'],
                                                       activity_count[cur_mnth]['pin'], activity_count[cur_mnth]['rapid_new'],
                                                       activity_count[cur_mnth]['cyk'], activity_count[cur_mnth]['russia'],
                                                       activity_count[cur_mnth]['team'], activity_count[cur_mnth]['start'],
                                                       activity_count[cur_mnth]['help'], activity_count[cur_mnth]['who'], activity_count[cur_mnth]['rapid'])
        bot.send_message(secret.apple_id, month_statistics, parse_mode='Markdown')
    except Exception as e:
        send_error(message, 4, e)

          
# Вызов информации о сервере
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.chat.id == secret.apple_id:
            try:
                if message.text == '/s':
                    ram = psutil.virtual_memory()
                    bot.send_message(message.chat.id, '💾 Free RAM: {0}%'.format(ram[2]))
                else:
                    bot.send_message(secret.tg_chat_id, message.text[3:len(message.text)])
                    bot.send_message(secret.apple_id, '✅ Сообщение отправлено')
            except Exception as e:
                send_error(message, 21, e)
        else:
            send_error(message, 6, 'N/A')
    except Exception as e:
        send_error(message, 5, e)


# # # # # # Общие команды
# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        update_activity('who')
        if message.chat.id == secret.tg_chat_id:
            bot.send_message(secret.tg_requests_chat_id, '✅❌ [who](tg://user?id={0})'.format(str(message.from_user.id)), parse_mode='Markdown')
            force_reply = telebot.types.ForceReply(True)
            bot.send_message(secret.tg_chat_id, constants.enter_question_new, reply_to_message_id=message.message_id, reply_markup=force_reply)
            bot.delete_message(secret.tg_chat_id, message.message_id)
        elif message.chat.id in constants.tg_ids:
            bot.send_message(message.chat.id, '❌ Опрос создается только в [Шобле](https://t.me/c/1126587083/)', parse_mode='Markdown')
    except Exception as e:
        send_error(message, 7, e)


# Отправка скидок
@bot.message_handler(commands=['discount'])
def send_discount(message):
    try:
        if message.from_user.id in constants.tg_ids:
            i = 0
            keyboard_start = telebot.types.InlineKeyboardMarkup(row_width=2)
            while i < disc_count - 1:
                keyboard_start.add(telebot.types.InlineKeyboardButton(text=constants.buttons[0][i+1], callback_data=constants.buttons[1][i+1]),
                                   telebot.types.InlineKeyboardButton(text=constants.buttons[0][i+2], callback_data=constants.buttons[1][i+2]))
                i += 2
            keyboard_start.add(discounts, channel)
            bot.send_message(message.chat.id, constants.buttons[2][0], reply_markup=keyboard_start, parse_mode='Markdown')
            update_activity('discount')
    except Exception as e:
        send_error(message, 8, e)


# # # # # # Обработка данных
# Обработка девки за рулем
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.dvk and message.chat.id == secret.tg_chat_id)
def aaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Двк з рлм')
        update_activity('devka')
    except Exception as e:
        send_error(message, 9, e)


@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.devka and message.chat.id == secret.tg_chat_id)
def aaaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Девка за рулём')
        update_activity('devka')
    except Exception as e:
        send_error(message, 10, e)

        
# Обработка РАСИЯ
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.russia and message.chat.id == secret.tg_chat_id)
def russia(message):
    try:
        bot.send_voice(secret.tg_chat_id, 'AwACAgIAAxkBAAJDIWLGyK15Ym3bMc0u5PU9YXtDDxHnAALtHAACbJI4SiCUtXmDfvoxKQQ', '🫡')
        update_activity('russia')
    except Exception as e:
        send_error(message, 11, e)

        
# Обработка врача
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.vracha and message.chat.id == secret.tg_chat_id)
def vracha(message):
    try:
        bot.send_document(secret.tg_chat_id, 'CgADAgADRgIAAkbDcEn-Ox-uqrgsHgI', caption='@oxy_genium')
        update_activity('vracha')
    except Exception as e:
        send_error(message, 12, e)


# Обработка гита
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.git2 and message.chat.id == secret.tg_chat_id)
def git(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Хуит')
        update_activity('git')
    except Exception as e:
        send_error(message, 13, e)

        
# Обработка @team
@bot.message_handler(func=lambda message: message.text and constants.team in message.text.lower() and message.chat.id == secret.tg_chat_id)
def team(message):
    try:
        bot.send_message(chat_id=secret.tg_chat_id, disable_notification=False, reply_to_message_id=message.message_id, text='⚠️ *Внимание, Шобла*\n\n[Тарс](t.me/shackoor), [Апол](t.me/apoll), [Ивановский](t.me/ivanovmm), [Конатик](t.me/KanatoF), [Кир](t.me/zhuykovkb), [Катя](tg://user?id=434756061), [Максон](t.me/MrGogu), [Носик](tg://user?id=51994109), [Окз](t.me/oxy_genium), [Паузеньк](t.me/Pausenk), [НТЩ](t.me/ntshch), [Толяновский](t.me/toliyansky), [Виктор](t.me/FrelVick), [Морго](t.me/margoiv_a), [Мишаня](t.me/Mich37), [Ксю](t.me/ksenia_boorda), [Ромолэ](t.me/Roman_Kazitskiy), [Эльтос](t.me/elvira_aes), [Аня](t.me/kebushka), [Деннис](tg://user?id=503404575)', disable_web_page_preview=True, parse_mode="MarkdownV2")
        update_activity('team')
    except Exception as e:
        send_error(message, 14, e)

        
# Обработка @rapid
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(constants.rapid) and message.chat.id == secret.tg_chat_id)
def rapid(message):
    try:
        update_activity('rapid')
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
        bot.send_message(secret.tg_chat_id, answer['message'], parse_mode='Markdown')
        if answer['message'] == 'Номер успешно добавлен':
            update_activity('rapid_new')
    except Exception as e:
        bot.send_message(secret.zhuykovkb_apple_id, 'Ошибка в функции rapid:\n\nДанные ' + quote(value) + '\n\nТекст ошибки ' + str(e))
        send_error(message, 15, e)

        
# Обработка барсука
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.suk and message.chat.id == secret.tg_chat_id)
def barsuk(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсук')
        update_activity('cyk')
    except Exception as e:
        send_error(message, 16, e)
        

# Обработка барсюка
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.syuk and message.chat.id == secret.tg_chat_id)
def barsyuk(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсюк')
        update_activity('cyk')
    except Exception as e:
        send_error(message, 17, e)
        

# Обработка IPv6
@bot.message_handler(func=lambda message: message.text and message.text.lower() in constants.ip_block and message.chat.id == secret.tg_chat_id)
def block(message):
    try:
        bot.send_message(secret.tg_chat_id, '*Значит так, - сразу нахуй!*', parse_mode='Markdown')
    except Exception as e:
        send_error(message, 18, e)

    
# Обработчик текста
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
                        bot.delete_message(secret.tg_chat_id, message.reply_to_message.message_id)
                        bot.edit_message_reply_markup(secret.tg_chat_id, poll.message_id, reply_markup=keyboard_opros_stop)
                        bot.delete_message(secret.tg_chat_id, message.message_id)
                        bot.pin_chat_message(secret.tg_chat_id, poll.message_id, disable_notification=False)
                        update_activity('opros')
                    else:
                        force_reply = telebot.types.ForceReply(True)
                        bot.delete_message(secret.tg_chat_id, message.reply_to_message.message_id)
                        bot.send_message(message.chat.id, constants.too_large_question, reply_to_message_id=message.message_id, reply_markup=force_reply)                       
                except Exception as e:
                    # bot.send_message(message.chat.id, constants.errors[14] + '\nНовый опросник\n' + str(e))
                    send_error(message, 19, e)      
            # Запрос внесения опроса
            elif message.reply_to_message.text == constants.enter_question:
                try:
                    date = str(time.time() + 10800)
                    date = date.split('.')[0]
                    # Копирование пустого опроса в who
                    bashCopy = "cp /root/router/shoblabot/opros /root/router/shoblabot/who"
                    processC = subprocess.Popen(bashCopy.split(), stdout=subprocess.PIPE)
                    time.sleep(1)
                    # Переименование опроса в date
                    bashRename = 'mv /root/router/shoblabot/who/opros /root/router/shoblabot/who/{0}'.format(date)
                    processR = subprocess.Popen(bashRename.split(), stdout=subprocess.PIPE)
                    opros = '*Опрос:* ' + message.text
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                    # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                    button = [None] * who_count
                    i = 0
                    while i < who_count - 1:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                       callback_data='opr_' + str(i) + '_' + date)
                        button[i + 1] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i + 1],
                                                                           callback_data='opr_' + str(i + 1) + '_' + date)
                        keyboard.add(button[i], button[i + 1])
                        i += 2
                    if 1 == who_count % 2:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                       callback_data='opr_' + str(i) + '_' + date)
                        keyboard.add(button[i])
                    bot.send_message(secret.tg_chat_id, opros, reply_markup=keyboard, parse_mode='Markdown')
                    bot.send_message(secret.tg_requests_chat_id, date, parse_mode='Markdown')
                    bot.delete_message(secret.tg_chat_id, message.reply_to_message.message_id)
                    bot.delete_message(secret.tg_chat_id, message.message_id)
                    update_activity('opros')
                except Exception as e:
                    send_error(message, 19, e)
            elif message.text == '@shoblabot':
                bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                     disable_notification=False)
                update_activity('pin')
        elif message.reply_to_message is not None and message.text == '@shoblabot':
            bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                 disable_notification=False)
            update_activity('pin')
    except Exception as e:
        send_error(message, 20, e)

        
# Обработчик Call Back Data
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    try:
        # Кнопка остановки опроса
        if call.data[0:4] == 'stop':
            message_id = int(call.data.split('_')[1])
            user_id = int(call.data.split('_')[2])
            try:
                if call.from_user.id == user_id:
                    bot.stop_poll(secret.tg_chat_id, message_id)
                else:
                    bot.answer_callback_query(call.id, constants.wrong_stop, show_alert=True)
            except Exception as e:
                send_error(call.message, 22, e)
        # Обработка кнопок опроса (старого)
        elif call.data[0:2] == 'op':
            user_id = int(call.data.split('_')[1])
            try:
                date = call.data.split('_')[2]
                if call.from_user.id == constants.who_will_ids[user_id]:
                    # Загружаем данные из файла date
                    if os.path.isfile('/root/router/shoblabot/who/{0}'.format(date)):
                        with open('/root/router/shoblabot/who/{0}'.format(date), 'r') as lang:
                            who_opros = json.loads(lang.read())
                    who_opros[str(call.from_user.id)] = (who_opros[str(call.from_user.id)] + 1) % 3 + 1
                    # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                    button = [None] * who_count
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                    i = 0
                    while i < who_count - 1:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[who_opros[str(constants.who_will_ids[i])]][i],callback_data='opr_' + str(i) + '_' + date)
                        button[i + 1] = telebot.types.InlineKeyboardButton(text=constants.who_will[who_opros[str(constants.who_will_ids[i + 1])]][i + 1],callback_data='opr_' + str(i + 1) + '_' + date)
                        keyboard.add(button[i], button[i + 1])
                        i += 2
                    if 1 == who_count % 2:
                        button[i] = telebot.types.InlineKeyboardButton(
                            text=constants.who_will[who_opros[str(constants.who_will_ids[i])]][i],
                            callback_data='opr_' + str(i) + '_' + date)
                        keyboard.add(button[i])
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=keyboard)
                    if who_opros[str(1)] == 0:
                        who_opros[str(1)] = 1
                        bot.pin_chat_message(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             disable_notification=False)
                    # Записываем данные в файл
                    with open('/root/router/shoblabot/who/{0}'.format(date), 'w') as lang:
                        lang.write(json.dumps(who_opros))
            except Exception as e:
                send_error(call.message, 2, e)
        # Обработка запроса скидок
        elif call.data[0:4] == 'disc':
            discount_id = int(call.data.split('_')[1])
            buttons_text = constants.buttons[0][0:discount_id] + constants.buttons[0][discount_id+1:len(constants.buttons[0])]
            buttons_callback_data = constants.buttons[1][0:discount_id] + constants.buttons[1][discount_id+1:len(constants.buttons[1])]
            keyboard_update = telebot.types.InlineKeyboardMarkup(row_width=2)
            i = 0
            while i < disc_count-2:
                keyboard_update.add(telebot.types.InlineKeyboardButton(text=buttons_text[i], callback_data=buttons_callback_data[i]),
                                    telebot.types.InlineKeyboardButton(text=buttons_text[i+1], callback_data=buttons_callback_data[i+1]))
                i += 2
            keyboard_update.add(discounts, channel)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=constants.buttons[2][discount_id], parse_mode='Markdown',
                                  reply_markup=keyboard_update)
    except Exception as e:
        send_error(call.message, 3, e)


# Отправка поздравления с др в Шоблу
def sdr():
    try:
        threading.Timer(3600, sdr).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
        now_time = datetime.datetime.now()
        dr = str(now_time.day) + '.' + str(now_time.month)
        i = 0
        if now_time.hour is not 10:
            return
        if now_time.day == 1: # День для статистики по боту выкладывания фоток за месяц Месечная десятка челлендж
            if now_time.month == 1:
                cur_mnth = str(now_time.year-1) + '.12'
            else:
                cur_mnth = str(now_time.year) + '.' + str(now_time.month-1)
            # Загружаем данные из файла activity_count
            if os.path.isfile('/root/router/shoblabot/activity_count'):
                with open('/root/router/shoblabot/activity_count', 'r') as lang:
                    activity_count = json.loads(lang.read())
            month_statistics = constants.month_statistics.format(activity_count[cur_mnth]['opros'], activity_count[cur_mnth]['discount'],
                                                           activity_count[cur_mnth]['devka'], activity_count[cur_mnth]['vracha'],
                                                           activity_count[cur_mnth]['pin'], activity_count[cur_mnth]['rapid_new'],
                                                           activity_count[cur_mnth]['cyk'], activity_count[cur_mnth]['russia'],
                                                           activity_count[cur_mnth]['team'], activity_count[cur_mnth]['start'],
                                                           activity_count[cur_mnth]['help'], activity_count[cur_mnth]['who'], activity_count[cur_mnth]['rapid'])
            bot.send_message(secret.tg_chat_id, month_statistics, parse_mode='Markdown')
            # Рассылка по 10челлендж
            challenge = bot.send_message(secret.tg_chat_id, 'Шоблятки, время для #10челлендж и выших фоточек за месяц!📸', parse_mode='Markdown')
            bot.pin_chat_message(secret.tg_chat_id, challenge.message_id, disable_notification=False)
        if dr == str(28.5):  # День Баяна в Шобле отмечается 28 мая
            bot.send_message(secret.tg_chat_id, '🪗 Шобла, поздравляю с Днём Баяна!')
        if dr == str(25.7):  # День Рождения Себа
            bot.send_message(secret.tg_chat_id, '[Seb](tg://user?id=959656923), HB!🥳🇲🇽\nFrom Shobla with love!', parse_mode='Markdown')
        for item in constants.tg_drs:
            if item == dr:
                bot.send_message(secret.tg_chat_id,
                                 '[{0}](tg://user?id={1}), с др!🥳'.format(constants.tg_names[i], constants.tg_ids[i]), parse_mode='Markdown')
            i += 1
    except Exception as e:
       bot.send_message(secret.apple_id, '❌ ООшибка в функции отправки поздравления в Шоблу sdr():\n*Ошибка:*\n' + str(e))


# Запуск функций
try:
    bot.remove_webhook()
except Exception as e:
    bot.send_message(secret.apple_id, '❌ Ошибка в функции bot.remove_webhook():\n*Ошибка:*\n' + str(e))

# try:
#     bot.send_message(secret.apple_id, '⏳ *Время запуска бота:* _{0}_'.format(time.ctime(time.time())), parse_mode='Markdown')
# except Exception as e:
#     bot.send_message(secret.apple_id, '❌ Ошибка в функции send_start_time:\n*Ошибка:*\n' + str(e))

try:
    sdr()
except Exception as e:
    bot.send_message(secret.apple_id, '❌ Ошибка в запуске sdr():\n*Ошибка:*\n' + str(e))

try:
    bot.polling()
except Exception as e:
    bot.send_message(secret.apple_id, '❌ Ошибка при запуске bot.polling():\n*Ошибка:*\n' + str(e))
    
# class WebhookServer(object):
# index равнозначно /, т.к. отсутствию части после ip-адреса (грубо говоря)
#    @cherrypy.expose
#    def index(self):
#        length = int(cherrypy.request.headers['content-length'])
#        json_string = cherrypy.request.body.read(length).decode("utf-8")
#        update = telebot.types.Update.de_json(json_string)
#        bot.process_new_updates([update])
#        return ''

# if __name__ == '__main__':
#    cherrypy.config.update({
#        'server.socket_host': '127.0.0.1',
#        'server.socket_port': 7771,
#        'engine.autoreload.on': False
#    })
#    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
