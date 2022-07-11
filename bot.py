#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import os  # Для проверки на существование файла
import json  # Представляет словарь в строку
import glob
import time  # Для представления времени в читаемом формате
import psutil
import random
import telebot
import cherrypy
import datetime
import constants
import secret
import threading
import subprocess
from io import BytesIO  # Для отправки фотографий из Telegram в Шоблу
from datetime import timedelta
import urllib.request as urllib2  # Для отправки фотографий из Telegram в Шоблу
from urllib.parse import quote
import json
from telebot import apihelper

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
keyboard_okey = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_bushe = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_dosta = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_pyatera = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_perik = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_lenta = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_domovoi = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_ikea = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_diksi = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_karusel = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_stolichki = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_podr = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_sephora = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_prisma = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_lime = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_ulibka = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_letual = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_ozerki = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_magnit = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_ashan = telebot.types.InlineKeyboardMarkup(row_width=2)

okey = telebot.types.InlineKeyboardButton(text='О\'КЕЙ 🛒', callback_data='okey')
bushe = telebot.types.InlineKeyboardButton(text='Буше 🥐', callback_data='bushe')
dosta = telebot.types.InlineKeyboardButton(text='Достаевский 🍕', callback_data='dosta')
pyatera = telebot.types.InlineKeyboardButton(text='Пятерочка 🛒', callback_data='pyatera')
perik = telebot.types.InlineKeyboardButton(text='Перекресток 🛒', callback_data='perik')
lenta = telebot.types.InlineKeyboardButton(text='Лента 🛒', callback_data='lenta')
domovoi = telebot.types.InlineKeyboardButton(text='Домовой 🛠', callback_data='domovoi')
ikea = telebot.types.InlineKeyboardButton(text='Икеа 🛋', callback_data='ikea')
diksi = telebot.types.InlineKeyboardButton(text='Дикси 🛒', callback_data='diksi')
stolichki = telebot.types.InlineKeyboardButton(text='Столички 💊', callback_data='stolichki')
karusel = telebot.types.InlineKeyboardButton(text='Карусель 🛒', callback_data='karusel')
podr = telebot.types.InlineKeyboardButton(text='Подружка 💅', callback_data='podr')
sephora = telebot.types.InlineKeyboardButton(text='Sephora 🖤', callback_data='sephora')
prisma = telebot.types.InlineKeyboardButton(text='Prisma 🛒', callback_data='prisma')
lime = telebot.types.InlineKeyboardButton(text='Лайм 🛒', callback_data='lime')
ulibka = telebot.types.InlineKeyboardButton(text='Улыбка 🌈', callback_data='ulibka')
letual = telebot.types.InlineKeyboardButton(text='Л\'этуль 💛', callback_data='letual')
ozerki = telebot.types.InlineKeyboardButton(text='Озерки 💊', callback_data='ozerki')
magnit = telebot.types.InlineKeyboardButton(text='Магнит 🛒', callback_data='magnit')
ashan =  telebot.types.InlineKeyboardButton(text='Ашан 🛒', callback_data='ashan')
discounts = telebot.types.InlineKeyboardButton(text='Все скидки 💰', url='https://photos.app.goo.gl/Xu4UQWqhSTcBVwt27')
channel = telebot.types.InlineKeyboardButton(text='Канал 💳', url='https://t.me/joinchat/AAAAAEk6NVud6BKc7YzZ2g')

# okey, lenta, perik, karusel, pyatera, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, discounts
keyboard_okey.add(lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_lenta.add(okey, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_perik.add(okey, lenta, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_karusel.add(okey, lenta, perik, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_pyatera.add(okey, lenta, perik, karusel, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_magnit.add(okey, lenta, perik, karusel, pyatera, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_diksi.add(okey, lenta, perik, karusel, pyatera, magnit, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_prisma.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_lime.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_ashan.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_ulibka.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_dosta.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_bushe.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_domovoi.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, podr, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_podr.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, letual, sephora, ozerki, stolichki, discounts, channel)
keyboard_letual.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, sephora, ozerki, stolichki, discounts, channel)
keyboard_sephora.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, ozerki, stolichki, discounts, channel)
keyboard_ozerki.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, stolichki, discounts, channel)
keyboard_stolichki.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, discounts, channel)
# keyboard_ikea.add(okey, lenta, perik, karusel, pyatera, magnit, diksi, prisma, lime, ashan, ulibka, dosta, bushe, domovoi, podr, letual, sephora, ozerki, stolichki, discounts, channel)


# # # # # # # # # # # Тело бота # # # # # # # # # # #
# Начальное сообщение
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        try:
            tg_user_id = constants.tg_ids.index(message.chat.id)
        except:
            tg_user_id = 0
        update_activity('start')
        if message.chat.id == secret.tg_chat_id or message.chat.id == constants.tg_ids[tg_user_id]:
            bot.send_message(secret.tg_requests_chat_id, '🕹 */start* от [{0}](tg://user?id={1})\n'
                                                            '*Чат:* {2}'.format(constants.tg_names[tg_user_id],
                                                                                str(message.from_user.id),
                                                                                str(message.chat.id)),
                             parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, disable_web_page_preview=True, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в команде /start:\n\n' + str(e))


# Вызов справки
@bot.message_handler(commands=['help'])
def handle_help(message):
    try:
        try:
            tg_user_id = constants.tg_ids.index(message.from_user.id)
        except:
            tg_user_id = 0
        update_activity('help')
        if message.chat.id == secret.tg_chat_id or message.chat.id == constants.tg_ids[tg_user_id]:
            bot.send_message(secret.tg_requests_chat_id, '❓ */help* от [{0}](tg://user?id={1})\n'
                                                            '*Чат:* {2}'.format(constants.tg_names[tg_user_id],
                                                                                str(message.from_user.id),
                                                                                str(message.chat.id)),
                             parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, disable_web_page_preview=True, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в команде /help:\n\n' + str(e))


# # # # # # Служебные функции и команды
# Функция отправки времени старта запуска бота
def send_start_time():
    try:
        date = time.time() + 10800
        bot.send_message(secret.apple_id,
                         '*Время запуска бота: *_{0}_'.format(time.strftime('%d.%m.%y %X', time.gmtime(date))),
                         parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_start_time:\n\n' + str(e))


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
        bot.send_message(secret.apple_id, 'Ошибка в функции update_activity:\n\n' + str(e))
        
        
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
        month_statistics = '🤖 Статистика по боту за прошлый месяц:\n\n' \
                           '✅❌ Создано опросов: *{0} шт*\n' \
                           '🛍  Запрошено скидок: *{1} раз*\n' \
                           '💁‍♀️🚗 Обнаружено девок за рулём: *{2} шт*\n' \
                           '👩🏻‍⚕️ Врача вызывали: *{3} раз*\n' \
                           '✅️ Сохранено номеров Рапидов: *{4} шт*\n' \
                           '🦡 Отправлено барсуков: *{5} раз*\n' \
                           '🫡🇷🇺 Спето российских гимнов: *{6} раз*\n' \
                           '👥 Вызваны все участники Шоблы: *{7} раз*\n\n' \
                           'А так же отправлено следующих команд:\n\n' \
                           '/start: *{8} раз*\n' \
                           '/help: *{9} раз*\n' \
                           '/who: *{10} раз*\n' \
                           '/rapid: *{11} раз*'.format(activity_count[cur_mnth]['opros'],
                                                    activity_count[cur_mnth]['discount'],
                                                    activity_count[cur_mnth]['devka'],
                                                    activity_count[cur_mnth]['vracha'],
                                                    activity_count[cur_mnth]['rapid_new'],
                                                    activity_count[cur_mnth]['cyk'],
                                                    activity_count[cur_mnth]['russia'],
                                                    activity_count[cur_mnth]['team'],
                                                    activity_count[cur_mnth]['start'],
                                                    activity_count[cur_mnth]['help'],
                                                    activity_count[cur_mnth]['who'],
                                                    activity_count[cur_mnth]['rapid'])
        bot.send_message(secret.apple_id, month_statistics, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в команде /statistics:\n\n' + str(e))

        
# Функция отправки ошибки
def send_error(message, error_id):
    try:
        date = time.strftime('%d.%m.%y %X', time.gmtime(message.date + 10800))
        bot.send_message(secret.apple_id,
                         '*{0}\nОт:* {1} {2}\n*Username:* {3}\n*Чат:* {4} {5} {6} id: {7}\n*Сообщение:* {8}\n'
                         '*Время:* _{9}_'.format(constants.errors[error_id], str(message.from_user.first_name),
                                                 str(message.from_user.last_name), str(message.from_user.username),
                                                 str(message.chat.title), str(message.chat.first_name),
                                                 str(message.chat.last_name), str(message.chat.id), message.text, date),
                         parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_error:\n\n' + str(e))

        
# Вызов информации о сервере
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.chat.id == secret.apple_id:
            try:
                if message.text == '/s':
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    server = telebot.types.InlineKeyboardButton(text='💾', callback_data='adm_si')
                    keyboard.add(server)
                    bot.send_message(message.chat.id, '👑 Admin panel', reply_markup=keyboard)
                else:
                    bot.send_message(secret.tg_chat_id, message.text[3:-1])
                    bot.send_message(secret.apple_id, '✅ Сообщение отправлено')
            except:
                send_error(message, 3)
        else:
            send_error(message, 2)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции server_info:\n\n' + str(e))


# # # # # # Общие команды
# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        try:
            update_activity('who')
            if message.chat.id == secret.tg_chat_id:
                user_id = constants.tg_ids.index(message.from_user.id)
                if user_id is not None:
                    bot.send_message(secret.tg_requests_chat_id, '✅ */who* от [{0}](tg://user?id={1})'.format(constants.tg_names[user_id],
                                                                                        str(message.from_user.id)), parse_mode='Markdown')
                    force_reply = telebot.types.ForceReply(True)
                    bot.send_message(secret.tg_chat_id, constants.enter_question_new, reply_to_message_id=message.message_id,
                                     reply_markup=force_reply)
                    bot.delete_message(secret.tg_chat_id, message.message_id)
            else:
                bot.send_message(message.chat.id, '❌ Опрос создается только в Шобле')
        except:
            send_error(message, 2)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции who_will:\n\n' + str(e))


# Отправка скидок
@bot.message_handler(commands=['discount'])
def send_discount(message):
    try:
        if message.from_user.id in constants.tg_ids:
            bot.send_message(message.chat.id, '🛒 [О\'КЕЙ](https://i.imgur.com/TZV4nCd.jpg)', reply_markup=keyboard_okey,
                                 parse_mode='Markdown')
            update_activity('discount')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_discount:\n\n' + str(e))


# # # # # # Обработка данных
# Обработка девки за рулем
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.dvk and message.chat.id == secret.tg_chat_id)
def aaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Двк з рлм')
        update_activity('devka')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции aaa:\n\n' + str(e))


@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.devka and message.chat.id == secret.tg_chat_id)
def aaaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Девка за рулём')
        update_activity('devka')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции aaaa:\n\n' + str(e))

        
# Обработка РАСИЯ
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.russia and message.chat.id == secret.tg_chat_id)
def russia(message):
    try:
        bot.send_voice(secret.tg_chat_id, 'AwACAgIAAxkBAAJDIWLGyK15Ym3bMc0u5PU9YXtDDxHnAALtHAACbJI4SiCUtXmDfvoxKQQ', '🫡')
        update_activity('russia')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции russia:\n\n' + str(e))

        
# Обработка врача
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.vracha and message.chat.id == secret.tg_chat_id)
def vracha(message):
    try:
        bot.send_document(secret.tg_chat_id, 'CgADAgADRgIAAkbDcEn-Ox-uqrgsHgI', caption='@oxy_genium')
        update_activity('vracha')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции vracha:\n\n' + str(e))


# Обработка гита
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.git2 and message.chat.id == secret.tg_chat_id)
def git(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Хуит')
        update_activity('git')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции git:\n\n' + str(e))

        
# Обработка @team
@bot.message_handler(func=lambda
        message: message.text and constants.team in message.text.lower() and message.chat.id == secret.tg_chat_id)
def team(message):
    try:
        bot.send_message(chat_id=secret.tg_chat_id, disable_notification=False, reply_to_message_id=message.message_id , text='⚠️ *Внимание, Шобла*\n\n[Тарс](t.me/shackoor), [Апол](t.me/apoll), [Ивановский](t.me/ivanovmm), [Конатик](t.me/KanatoF), [Кир](t.me/zhuykovkb), [Катя](tg://user?id=434756061), [Максон](t.me/MrGogu), [Носик](tg://user?id=51994109), [Окз](t.me/oxy_genium), [Паузеньк](t.me/Pausenk), [НТЩ](t.me/ntshch), [Толяновский](t.me/toliyansky), [Виктор](t.me/FrelVick), [Морго](t.me/margoiv_a), [Мишаня](t.me/Mich37), [Ксю](t.me/ksenia_boorda), [Ромолэ](t.me/Roman_Kazitskiy), [Эльтос](t.me/elvira_aes), [Аня](t.me/kebushka), [Деннис](tg://user?id=503404575)', disable_web_page_preview=True, parse_mode="MarkdownV2")
        update_activity('team')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции team:\n\n' + str(e))

        
# Обработка @rapid
@bot.message_handler(func=lambda
        message: message.text and message.text.lower().startswith(constants.rapid) and message.chat.id == secret.tg_chat_id)
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
        bot.send_message(secret.apple_id, 'Ошибка в функции rapid:\n\nДанные ' + quote(value) + '\n\nТекст ошибки ' + str(e))

        
# Обработка барсука
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.suk and message.chat.id == secret.tg_chat_id)
def barsuk(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсук')
        update_activity('cyk')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции barsuk:\n\n' + str(e))
        

# Обработка барсюка
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.syuk and message.chat.id == secret.tg_chat_id)
def barsyuk(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсюк')
        update_activity('cyk')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции barsyuk:\n\n' + str(e))
        

# Обработка IPv6
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.ip_block and message.chat.id == secret.tg_chat_id)
def block(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Значит так, - сразу нахуй!')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции block:\n\n' + str(e))

    
# Обработчик текста
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        # Если это реплай на сообщение бота
        if message.reply_to_message is not None and message.reply_to_message.from_user.id == secret.bot_id:
            # Запрос внесения опроса (нового)
            if message.reply_to_message.text == constants.enter_question_new or message.reply_to_message.text == constants.too_large_question:
                try:
                    if len(message.text) <= 293:
                        opros = 'Опрос: ' + message.text
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
                    bot.send_message(message.chat.id, constants.errors[14] + '\nНовый опросник\n' + str(e))
                    send_error(message, 14)      
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
                except:
                    bot.send_message(message.chat.id, constants.errors[14])
                    send_error(message, 14)
            elif message.text == '@shoblabot':
                bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                     disable_notification=False)
        elif message.reply_to_message is not None and message.text == '@shoblabot':
            bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                 disable_notification=False)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в обработчике текста send_text:\n\n' + str(e) + '\n\n' + message.text)

        
# Обработчик Call Back Data
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    try:
        # Вызов панели администратора
        if call.data == 'adm_si':
            try:
                ram = psutil.virtual_memory()
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text='💽 RAM: {0}%'.format(ram[2]))
            except:
                send_error(call.message, 21)
        elif call.data[0:4] == 'stop':
            message_id = int(call.data.split('_')[1])
            user_id = int(call.data.split('_')[2])
            try:
                if call.from_user.id == user_id:
                    bot.stop_poll(secret.tg_chat_id, message_id)
                else:
                    bot.answer_callback_query(call.id, constants.wrong_stop, show_alert=True)
            except:
                send_error(call.message, 31)
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
            except:
                send_error(call.message, 24)
                bot.send_message(secret.apple_id, '*Ошибка от:* {0}'.format(constants.who_will[0][user_id]),
                                 parse_mode='Markdown')
        elif call.data == 'okey':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [О\'кей](https://i.imgur.com/TZV4nCd.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_okey)
        elif call.data == 'bushe':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🥐 [Буше](https://i.imgur.com/H6ins0K.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_bushe)
        elif call.data == 'dosta':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🍕 [Достаевский](https://i.imgur.com/LTx5ztX.jpg)\n*ТОЛЬКО ПРИ ЗАКАЗЕ ПО ТЕЛЕФОНУ*',
                                  parse_mode='Markdown', reply_markup=keyboard_dosta)
        elif call.data == 'pyatera':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Пятерочка](https://i.imgur.com/yTuhGWH.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_pyatera)
        elif call.data == 'perik':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Перекресток](https://i.imgur.com/my5Q8RF.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_perik)
        elif call.data == 'lenta':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Лента](https://i.imgur.com/PE9txx0.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_lenta)
        elif call.data == 'domovoi':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛠 [Домовой](https://i.imgur.com/Tnn5WTG.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_domovoi)
        elif call.data == 'ikea':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛋 [Икеа](https://i.imgur.com/ThL03zt.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_ikea)
        elif call.data == 'diksi':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Дикси](https://i.imgur.com/FIQdWAh.png)', parse_mode='Markdown',
                                  reply_markup=keyboard_diksi)
        elif call.data == 'karusel':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Карусель](https://i.imgur.com/vwY6SB3.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_karusel)
        elif call.data == 'stolichki':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='💊 [Столички](https://i.imgur.com/dhWmZdf.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_stolichki)
        elif call.data == 'podr':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='💅 [Подружка](https://i.imgur.com/0NGsUpZ.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_podr)
        elif call.data == 'sephora':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🖤 [Sephora](https://i.imgur.com/qm2RlMr.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_sephora)
        elif call.data == 'prisma':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Prisma](https://i.imgur.com/tcFfgho.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_prisma)
        elif call.data == 'lime':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Лайм](https://i.imgur.com/hq39niT.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_lime)
        elif call.data == 'ulibka':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='[Улыбка](https://i.imgur.com/bpcYZ2v.jpg) 🌈', parse_mode='Markdown',
                                  reply_markup=keyboard_ulibka)
        elif call.data == 'letual':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='💛 [Л\'этуль](https://i.imgur.com/CqWU2vj.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_letual)
        elif call.data == 'ozerki':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='💊 [Озерки](https://i.imgur.com/6bDnAK4.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_ozerki)
        elif call.data == 'magnit':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Магнит](https://i.imgur.com/Nmn5pTt.png)', parse_mode='Markdown',
                                  reply_markup=keyboard_magnit)
        elif call.data == 'ashan':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Ашан](https://i.imgur.com/iGsQ2Ds.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_ashan)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в обработчике Callback кнопок callback_buttons:\n\n' + str(e))


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
            month_statistics = '🤖 Статистика по боту за прошлый месяц:\n\n' \
                               '✅❌ Создано опросов: *{0} шт*\n' \
                               '🛍  Запрошено скидок: *{1} раз*\n' \
                               '💁‍♀️🚗 Обнаружено девок за рулём: *{2} шт*\n' \
                               '👩🏻‍⚕️ Врача вызывали: *{3} раз*\n' \
                               '✅️ Сохранено номеров Рапидов: *{4} шт*\n' \
                               '🦡 Отправлено барсуков: *{5} раз*\n' \
                               '🫡🇷🇺 Спето российских гимнов: *{6} раз*\n' \
                               '👥 Вызваны все участники Шоблы: *{7} раз*\n\n' \
                               'А так же отправлено следующих команд:\n\n' \
                               '/start: *{8} раз*\n' \
                               '/help: *{9} раз*\n' \
                               '/who: *{10} раз*\n' \
                               '/rapid: *{11} раз*'.format(activity_count[cur_mnth]['opros'],
                                                           activity_count[cur_mnth]['discount'],
                                                           activity_count[cur_mnth]['devka'],
                                                           activity_count[cur_mnth]['vracha'],
                                                           activity_count[cur_mnth]['rapid_new'],
                                                           activity_count[cur_mnth]['cyk'],
                                                           activity_count[cur_mnth]['russia'],
                                                           activity_count[cur_mnth]['team'],
                                                           activity_count[cur_mnth]['start'],
                                                           activity_count[cur_mnth]['help'],
                                                           activity_count[cur_mnth]['who'],
                                                           activity_count[cur_mnth]['rapid'])
            bot.send_message(secret.tg_chat_id, month_statistics, parse_mode='Markdown')
            # Рассылка по 10челлендж
            challenge = bot.send_message(secret.tg_chat_id, 'Шоблятки, время для #10челлендж и выших фоточек за месяц!📸', parse_mode='Markdown')
            bot.pin_chat_message(secret.tg_chat_id, challenge.message_id, disable_notification=False)
        if dr == str(28.5):  # День Баяна в Шобле отмечается 28 мая
            bot.send_message(secret.tg_chat_id, 'Шобла, поздравляю с Днём Баяна🪗!🕺💃🥳', parse_mode='Markdown')
        if dr == str(25.7):  # День Рождения Себа
            bot.send_message(secret.tg_chat_id, '[Seb](tg://user?id=959656923), HB!🥳🇲🇽\nFrom Shobla with love!', parse_mode='Markdown')
        for item in constants.tg_drs:
            if item == dr:
                bot.send_message(secret.tg_chat_id,
                                 '[{0}](tg://user?id={1}), с др!'.format(constants.tg_names[i], constants.tg_ids[i]),
                                 parse_mode='Markdown')
            i += 1
    except Exception as e:
        bot.send_message(secret.apple_id,
                         'Ошибка в функции отправки поздравления в Шоблу sdr():\n\n' + str(e))


# Запуск функций
try:
    bot.remove_webhook()
except Exception as e:
    bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\nremove_webjook()\n\n' + str(e))

# try:
#     send_start_time()
# except Exception as e:
#     bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\n\send_start_time()\n\n' + str(e))

try:
    sdr()
except Exception as e:
    bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\n\sdr()\n\n' + str(e))

try:
    bot.polling()
except Exception as e:
    bot.send_message(secret.apple_id, 'Ошибка при запуске bot.polling():\n\n' + str(e))

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
